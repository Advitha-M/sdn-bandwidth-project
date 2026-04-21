"""
Topology A — Linear Chain with Bottleneck
                                        
  h1 --(100Mbps)-- s1 --(10Mbps)--> s2 --(100Mbps)-- h2
                   |                                   |
                   h3                                 h4

The s1--s2 link is intentionally throttled to 10 Mbps.
This simulates a WAN bottleneck / slow inter-site link.
iperf from h1->h2 will be limited to ~10 Mbps even though
host-facing links are 100 Mbps.
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinearTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')

        # Host-facing links — high bandwidth
        self.addLink(h1, s1, bw=100, delay='2ms',  loss=0)
        self.addLink(h3, s1, bw=100, delay='2ms',  loss=0)
        self.addLink(h2, s2, bw=100, delay='2ms',  loss=0)
        self.addLink(h4, s2, bw=100, delay='2ms',  loss=0)

        # Inter-switch bottleneck link — intentionally slow
        self.addLink(s1, s2, bw=10,  delay='20ms', loss=0)


def run():
    topo = LinearTopo()
    net  = Mininet(
        topo=topo,
        controller=RemoteController('c0', ip='127.0.0.1', port=6633),
        link=TCLink
    )
    net.start()

    info("\n" + "="*55 + "\n")
    info("TOPOLOGY A — Linear Chain with Bottleneck\n")
    info("  h1(10.0.0.1) h3(10.0.0.3) --> s1\n")
    info("  s1 --[10 Mbps bottleneck]--> s2\n")
    info("  s2 --> h2(10.0.0.2) h4(10.0.0.4)\n")
    info("="*55 + "\n\n")
    info("SUGGESTED TESTS:\n")
    info("  Same-switch:   h1 <-> h3  (expect ~100 Mbps)\n")
    info("  Cross-switch:  h1 <-> h2  (expect ~10 Mbps)\n")
    info("  pingall to check connectivity first\n\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
