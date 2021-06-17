#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    print("Starting to create the topology")

    net = Containernet(controller=Controller, link=TCLink, xterms=False)
    print("Created the newtork")

    mgr = VNFManager(net)
    print("Created the VNF manager")

    net.addController("c0")
    print("Added the controller")

    # create six drones
    h1 = net.addDockerHost(
        "h1", dimage="my_dev_test", ip="10.0.0.1", docker_args={"hostname":"drone1"}
    )
    h2 = net.addDockerHost(
        "h2", dimage="my_dev_test", ip="10.0.0.2", docker_args={"hostname":"drone2"},
    )
    h3 = net.addDockerHost(
        "h3", dimage="my_dev_test", ip="10.0.0.3", docker_args={"hostname":"drone3"},
    )
    h4 = net.addDockerHost(
        "h4", dimage="my_dev_test", ip="10.0.0.4", docker_args={"hostname":"drone4"}
    )
    h5 = net.addDockerHost(
        "h5", dimage="my_dev_test", ip="10.0.0.5", docker_args={"hostname":"drone5"},
    )
    h6 = net.addDockerHost(
        "h6", dimage="my_dev_test", ip="10.0.0.6", docker_args={"hostname":"drone6"},
    )
    # create mqtt broker, web server, and client
    h7 = net.addDockerHost(
        "h7", dimage="my_dev_test", ip="10.0.0.7", docker_args={"hostname":"broker"}
    )
    h8 = net.addDockerHost(
        "h8", dimage="my_dev_test", ip="10.0.0.8", docker_args={"hostname":"server"},
    )
    h9 = net.addDockerHost(
        "h9", dimage="my_dev_test", ip="10.0.0.9", docker_args={"hostname":"client"},
    )
    
    print("Added the nine hosts")

    switch1 = net.addSwitch("s1")
    
    net.addLink(switch1, h1, bw=10, delay="10ms")
    net.addLink(switch1, h2, bw=10, delay="10ms")
    net.addLink(switch1, h3, bw=10, delay="10ms")
    net.addLink(switch1, h7, bw=10, delay="10ms")
    
    net.addLink(switch1, h4, bw=10, delay="10ms")
    net.addLink(switch1, h5, bw=10, delay="10ms")
    net.addLink(switch1, h6, bw=10, delay="10ms")
    net.addLink(switch1, h7, bw=10, delay="10ms")
    
    net.addLink(switch1, h7, bw=10, delay="10ms")
    net.addLink(switch1, h8, bw=10, delay="10ms")
    net.addLink(switch1, h9, bw=10, delay="10ms")
    
        
    print("Added the switch")

    net.start()
    print("Started the newtork")

    srv7 = mgr.addContainer(
        "srv7", "h7", "broker_mqtt_broker", "/usr/sbin/mosquitto -c /mosquitto/config/mosquitto2.conf", docker_args={}
    )
    print("Added the MQTT broker")

    srv1 = mgr.addContainer(
        "srv1", "h1", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    srv2 = mgr.addContainer(
        "srv2", "h2", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    srv3 = mgr.addContainer(
        "srv3", "h3", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    srv4 = mgr.addContainer(
        "srv4", "h4", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    srv5 = mgr.addContainer(
        "srv5", "h5", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    srv6 = mgr.addContainer(
        "srv6", "h6", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    print("Added the drones MQTT client")
    
    srv8 = mgr.addContainer("srv8", "h8", "server", "", docker_args={})
    print("Added the server")

    srv9 = mgr.addContainer("srv9", "h9", "client", "bash", docker_args={})
    print("Added the client")

    #spawnXtermDocker("srv8")
    spawnXtermDocker("srv9")
    CLI(net)


    mgr.removeContainer("srv1")
    mgr.removeContainer("srv2")
    mgr.removeContainer("srv3")
    mgr.removeContainer("srv4")
    mgr.removeContainer("srv5")
    mgr.removeContainer("srv6")
    mgr.removeContainer("srv7")
    mgr.removeContainer("srv8")
    mgr.removeContainer("srv9")
    net.stop()
    mgr.stop()
