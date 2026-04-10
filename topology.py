#!/usr/bin/env python3
"""
topology.py — Mininet Topology for Port Status Monitoring Tool
Creates a 2-switch, 4-host topology connected to an external Ryu controller.

Topology:
    h1 ── s1 ── s2 ── h3
           |         |
          h2        h4

Usage:
    sudo python3 topology.py
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


def build_topology():
    """Build and start the Mininet topology."""

    # Use RemoteController so Ryu handles all logic
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    info("*** Adding Controller (Ryu running on localhost:6633)\n")
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    info("*** Adding Switches\n")
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')

    info("*** Adding Hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

    info("*** Adding Links\n")
    # Host to switch links (100Mbps, 1ms delay)
    net.addLink(h1, s1, bw=100, delay='1ms')
    net.addLink(h2, s1, bw=100, delay='1ms')
    net.addLink(h3, s2, bw=100, delay='1ms')
    net.addLink(h4, s2, bw=100, delay='1ms')

    # Inter-switch link (1Gbps, 2ms delay)
    net.addLink(s1, s2, bw=1000, delay='2ms')

    info("*** Starting Network\n")
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])

    info("\n*** Network Ready!\n")
    info("*** Hosts: h1(10.0.0.1) h2(10.0.0.2) h3(10.0.0.3) h4(10.0.0.4)\n")
    info("*** Switches: s1, s2 connected via trunk link\n")
    info("\n*** TEST COMMANDS TO TRY:\n")
    info("    pingall                    - Test all host connectivity\n")
    info("    h1 ping -c 5 h3            - Ping across switches\n")
    info("    iperf h1 h3                - Throughput test\n")
    info("    link s1 s2 down            - Simulate port DOWN (Scenario 2)\n")
    info("    link s1 s2 up              - Bring port back UP\n")
    info("    sh ovs-ofctl dump-flows s1 - View flow table\n")
    info("\n")

    CLI(net)

    info("*** Stopping Network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    build_topology()
