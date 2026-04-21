from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class ParallelTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        self.addLink(h1, s1, bw=100, delay='2ms')
        self.addLink(h2, s2, bw=100, delay='2ms')
        self.addLink(h3, s3, bw=100, delay='2ms')
        self.addLink(h4, s3, bw=100, delay='2ms')
        self.addLink(s1, s2, bw=50, delay='5ms')
        self.addLink(s1, s3, bw=50, delay='5ms')
        self.addLink(s2, s3, bw=50, delay='5ms')

def run():
    topo = ParallelTopo()
    net  = Mininet(topo=topo,
                   controller=RemoteController('c0', ip='127.0.0.1', port=6633),
                   link=TCLink)
    net.start()
    info("\n=== Topology B: Triangle (Parallel Paths) ===\n")
    info("h1->s1, h2->s2, h3/h4->s3 | All inter-switch links: 50Mbps\n\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
