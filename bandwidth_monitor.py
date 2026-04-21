"""
POX SDN Controller — Bandwidth Monitor
- Learning switch with flow rule installation
- Per-port bandwidth tracking via periodic stats polling
- Logs throughput per port every 5 seconds
"""

from pox.core import core
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
import time

log = core.getLogger()


class BandwidthMonitor(object):
    """One instance per connected switch."""

    def __init__(self, connection):
        self.connection = connection
        self.dpid = connection.dpid
        self.mac_to_port = {}
        self.byte_counts = {}      # port -> cumulative bytes
        self.last_time = time.time()

        connection.addListeners(self)
        Timer(5, self._request_stats, recurring=True)
        log.info("Switch %s up", dpidToStr(self.dpid))

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def _request_stats(self):
        self.connection.send(
            of.ofp_stats_request(body=of.ofp_port_stats_request())
        )

    def _handle_PortStatsReceived(self, event):
        now = time.time()
        elapsed = max(now - self.last_time, 0.001)
        self.last_time = now

        log.info("=== BW Stats | Switch %s ===", dpidToStr(self.dpid))
        for s in event.stats:
            port = s.port_no
            if port >= 0xFF00:
                continue
            total_bytes = s.tx_bytes + s.rx_bytes
            prev        = self.byte_counts.get(port, total_bytes)
            delta       = total_bytes - prev
            self.byte_counts[port] = total_bytes

            bw_mbps = (delta * 8) / (elapsed * 1_000_000)
            log.info(
                "  Port %-3s | RX %10d B | TX %10d B | "
                "Delta %8d B | BW ~%.3f Mbps",
                port, s.rx_bytes, s.tx_bytes, delta, bw_mbps
            )

    # ------------------------------------------------------------------
    # Packet handling — learning switch
    # ------------------------------------------------------------------
    def _handle_PacketIn(self, event):
        pkt = event.parsed
        if not pkt.parsed:
            return

        src, dst = pkt.src, pkt.dst
        in_port  = event.port
        self.mac_to_port[src] = in_port

        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]
            self._install_flow(src, dst, in_port, out_port, event)
        else:
            self._flood(event)

    def _install_flow(self, src, dst, in_port, out_port, event):
        msg = of.ofp_flow_mod()
        msg.match           = of.ofp_match(in_port=in_port,
                                           dl_src=src, dl_dst=dst)
        msg.idle_timeout    = 30
        msg.hard_timeout    = 120
        msg.priority        = 10
        msg.data            = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)
        log.debug("Flow installed %s→%s out port %s", src, dst, out_port)

    def _flood(self, event):
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.data     = event.ofp
        msg.in_port  = event.port
        self.connection.send(msg)


class Launcher(object):
    def __init__(self):
        core.openflow.addListeners(self)
        log.info("Bandwidth Monitor ready — waiting for switches...")

    def _handle_ConnectionUp(self, event):
        BandwidthMonitor(event.connection)


def launch():
    core.registerNew(Launcher)
