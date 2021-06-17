#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
#from mininet.node import RemoteController, Controller
    
    
if __name__ == "__main__":

    print("*** Creating the net")

    #net = Containernet(controller=RemoteController, link=TCLink, xterms=False, autoSetMacs=False)
    net = Containernet(link=TCLink, xterms=False, autoSetMacs=False)
    
    mgr = VNFManager(net)

    print("*** Adding the controller")
    #controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    #net.addController("c1")

    print("*** Creating hosts")
    # In our topology we have 6 drones (h1->h6),
    # 1 MQTT broker (h7), 1 Client (h8) and 1 server (h9)
    
    h1 = net.addHost("dr1", ip="10.0.0.1", mac="00:00:00:00:00:01")
    h2 = net.addHost("dr2", ip="10.0.0.2", mac="00:00:00:00:00:02")
    h3 = net.addHost("dr3", ip="10.0.0.3", mac="00:00:00:00:00:03")
    h4 = net.addHost("dr4", ip="10.0.0.4", mac="00:00:00:00:00:04")
    h5 = net.addHost("dr5", ip="10.0.0.5", mac="00:00:00:00:00:05")
    h6 = net.addHost("dr6", ip="10.0.0.6", mac="00:00:00:00:00:06")
    h7 = net.addHost("MB",  ip="10.0.0.7", mac="00:00:00:00:00:07")
    h8 = net.addHost("MC",  ip="10.0.0.8", mac="00:00:00:00:00:08")
    h9 = net.addHost("WS",  ip="10.0.0.9", mac="00:00:00:00:00:09")
    '''
    h1 = net.addDockerHost(
        "D1", dimage="my_dev_test", ip="10.0.0.1", docker_args={"hostname":"Drone1"}
    )
    h2 = net.addDockerHost(
        "D2", dimage="my_dev_test", ip="10.0.0.2", docker_args={"hostname":"Drone2"}
    )
    h3 = net.addDockerHost(
        "D3", dimage="my_dev_test", ip="10.0.0.3", docker_args={"hostname":"Drone3"}
    )
    h4 = net.addDockerHost(
        "D4", dimage="my_dev_test", ip="10.0.0.4", docker_args={"hostname":"Drone4"}
    )
    h5 = net.addDockerHost(
        "D5", dimage="my_dev_test", ip="10.0.0.5", docker_args={"hostname":"Drone5"}
    )
    h6 = net.addDockerHost(
        "D6", dimage="my_dev_test", ip="10.0.0.6", docker_args={"hostname":"Drone6"}
    )
    h7 = net.addDockerHost(
        "MB", dimage="my_dev_test", ip="10.0.0.7", docker_args={"hostname":"MQTTbroker"}
    )
    h8 = net.addDockerHost(
        "MC", dimage="my_dev_test", ip="10.0.0.8", docker_args={"hostname":"MQTTclient"}
    )
    h9 = net.addDockerHost(
        "WS", dimage="my_dev_test", ip="10.0.0.9", docker_args={"hostname":"WebServer"}
    )
    '''
    print("*** Creating switches")
    switch1 = net.addSwitch("s1")
    switch2 = net.addSwitch("s2")
    switch3 = net.addSwitch("s3")
    switch4 = net.addSwitch("s4")
    
    print("*** Creating links")
    # From broker to central switch
    net.addLink(switch4, h7, bw=10, delay="10ms")
    
    # From the central switch to the switches
    net.addLink(switch1, switch4, bw=10, delay="10ms")
    net.addLink(switch2, switch4, bw=10, delay="10ms")
    net.addLink(switch3, switch4, bw=10, delay="10ms")
    
    # From switch 1 to hosts
    net.addLink(switch1, h8, bw=10, delay="10ms")
    net.addLink(switch1, h9, bw=10, delay="10ms")
    
    # From switch 2 to drones 1,2,3
    net.addLink(switch2, h1, bw=10, delay="10ms")
    net.addLink(switch2, h2, bw=10, delay="10ms")
    net.addLink(switch2, h3, bw=10, delay="10ms")
    
    # From switch 3 to drones 4,5,6
    net.addLink(switch3, h4, bw=10, delay="10ms")
    net.addLink(switch3, h5, bw=10, delay="10ms")
    net.addLink(switch3, h6, bw=10, delay="10ms")
    
    print("*** Starting the network")
    net.start()
    
    os.system("sudo bash ./connect_nodes.sh")
    
    CLI(net)

    net.stop()
    
    mgr.stop()
