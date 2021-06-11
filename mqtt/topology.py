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

    h1 = net.addDockerHost(
        "h1", dimage="my_dev_test", ip="10.0.0.1", docker_args={"hostname":"h1"}
    )
    h2 = net.addDockerHost(
        "h2", dimage="my_dev_test", ip="10.0.0.2", docker_args={"hostname":"h2"},
    )
    h3 = net.addDockerHost(
        "h3", dimage="my_dev_test", ip="10.0.0.3", docker_args={"hostname":"h3"},
    )
    print("Added the three hosts")

    switch1 = net.addSwitch("s1")
    net.addLink(switch1, h1, bw=10, delay="10ms")
    net.addLink(switch1, h2, bw=10, delay="10ms")
    net.addLink(switch1, h3, bw=10, delay="10ms")
    print("Added the switch")

    net.start()
    print("Started the newtork")

    srv1 = mgr.addContainer(
        "srv1", "h1", "broker_mqtt_broker", "/usr/sbin/mosquitto -c /mosquitto/config/mosquitto2.conf", docker_args={}
    )
    print("Added the MQTT broker")

    srv2 = mgr.addContainer(
        "srv2", "h2", "drone_mqtt_client", "python3 /home/drone_client_mqtt.py", docker_args={}
    )
    print("Added the drone MQTT client")

    srv3 = mgr.addContainer("srv3", "h3", "my_dev_test", "bash", docker_args={})
    print("Added the my dev test 1")

    srv4 = mgr.addContainer("srv4", "h3", "my_dev_test", "bash", docker_args={})
    print("Added the my dev test 2")

    spawnXtermDocker("srv3")
    spawnXtermDocker("srv4")
    CLI(net)


    mgr.removeContainer("srv1")
    mgr.removeContainer("srv2")
    mgr.removeContainer("srv3")
    mgr.removeContainer("srv4")
    net.stop()
    mgr.stop()

