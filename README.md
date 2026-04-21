# SDN Bandwidth Measurement and Analysis
**Course:** UE24CS252B — Computer Networks  
**Controller:** POX | **Emulator:** Mininet

---

## Problem Statement
Measure and compare TCP bandwidth across two different SDN network
topologies using Mininet and a POX learning switch controller.
Analyze how topology design (bottleneck vs parallel paths) affects
throughput and latency.

---

## Topologies

### Topology A — Linear Chain with Bottleneck
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


###Topology B — Parallel Paths
"""
Topology B — Triangle (Parallel Paths)

       h1         h2
        \         /
    s1-(50Mbps)-s2
     \          /
   (50Mbps)  (50Mbps)
       \      /
         s3
        /   \
      h3     h4

All links are equal bandwidth (50 Mbps).
The controller floods to both paths initially, then installs
a single shortest path. Compare total throughput vs Topo A.

Key comparison: Topo A had a 10 Mbps bottleneck on the
inter-switch link. Here all inter-switch links are 50 Mbps,
so h1->h2 should achieve ~50 Mbps (5x improvement).
"""
