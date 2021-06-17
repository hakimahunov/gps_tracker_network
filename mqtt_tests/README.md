# MQTT 

Activities, documentation and instructions regarding the configuration of MQTT broker and clients in the GSP Tracker Network project. For any info, write to sberlato@fbk.eu.


## Requirements

* The [comnetsemu](https://git.comnets.net/public-repo/comnetsemu) virtual machine.


## What is MQTT

[TODO] Here there will be a brief description of: 
* what MQTT is
* the publish/subscribe model.
* topics


In MQTT, topics are created dynamically when:
* a client subscribes to a topic;
* a client publishes a message to a topic with the retained message set to `True`.

Topics are removed from an MQTT Broker when:
* the last client that is subscribing to that topic disconnects and clean session is `True`;
* a client connects with clean session set to `True`.



## Content of this Folder

In this folder, you will find three Dockerfiles:
* [*DockerfileMyMosquitto*](DockerfileMyMosquitto) - starting from the eclipse-mosquitto base image, specify an [alternative configuration file](./mosquitto.conf) to expose the broker to the network;
* [*DockerfileDroneMQTTClient*](DockerfileDroneMQTTClient) - starting from a Python3 base image, install an MQTT client, **Paho** (an [Eclipse Foundation](https://www.eclipse.org/org/foundation/) project) and copy the [*drone_client_mqtt.py*](./drone_client_mqtt.py) file in the `/home` directory;
* [*DockerfileMyDevTest*](DockerfileMyDevTest) - starting from the comnetsemu dev_test base image, install python3, pip, Paho and copy the [*just_connect_mqtt.py*](./just_connect_mqtt.py), [*drone_client_mqtt.py*](./drone_client_mqtt.py) and [*mock_server_mqtt.py*](./mock_server_mqtt.py) files in the `/home` directory. This image can be used to manually connect to the MQTT broker, subscribe to topics and check that everything is working.

The [*build_docker_images.sh*](build_docker_images.sh) file builds these three new images:
* the drone MQTT client, *drone_mqtt_client*
* the custom MQTT broker, *broker_mqtt_broker*
* the custom dev_test image, *my_dev_test*

Finally, there are four python files:
* [*drone_client_mqtt.py*](./drone_client_mqtt.py) - connect to the MQTT broker simulating the presence of a drone over Trento. Initially, generate a random position and publish it in a public topic "positions". Then, subscribe to a private topic ("command_${drone_id}") from which receive the server commands. When a command is received, parse the given position and simulate the drone moving to that position by sending position updates every second;
* [*just_connect_mqtt.py*](./just_connect_mqtt.py) - connect to the MQTT broker and subscribe to the "positions" and "log" topic;
* [*mock_server_mqtt.py*](./mock_server_mqtt.py) - simulate a server sending commands to the drones;
* [*topology.py*](./topology.py) - create a simple topology with one switch, connected to three hosts:
    * h1 - host srv1, the MQTT broker;
    * h2 - host srv2, the drone MQTT client;  
    * h3 - host srv3, the custom dev_test.



## How to Run

1. Clone/pull this folder in the comnetsemu virtual machine;
2. in the comnetsemu virtual machine, run *sudo ./build_docker_images.sh*;
3. in comnetsemu virtual machine, run *sudo python3 ./topology.py*. This will spawn a terminal connected to srv3 (on host h3);
4. in the spawned terminal, run *python3 ../home/just_connect.py*;
5. in the spawned terminal, you should see a new message every second. That message is published in the "gps_network_tracker" topic by srv2 and forwarded by srv1 to srv3.
