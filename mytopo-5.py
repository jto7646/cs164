"""
Custom Topology:

    +--------+   +--------+
    | client |---| server |
    +--------+   +--------+

"""

from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        # Add hosts
        client = self.addHost('client')
        server = self.addHost('server')

	# Add Link
        self.addLink(client, server)

topos = {'mytopo': (lambda: MyTopo())}
