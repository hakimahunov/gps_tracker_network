import paho.mqtt.client as mqtt
import random
import time


# This MQTT client just connects to the broker to print messages published in two topics:
# - "log": for debug logs;
# - "positions": for updates on drones positions.
topic_log = "log"
topic_positions = "positions"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message on topic " + msg.topic + ": " + str(msg.payload))



# Create the MQTT client and define callbacks for connection and messages.
client = mqtt.Client("just_connect")
client.on_connect = on_connect
client.on_message = on_message

# Blocking call to connect to the broker.
# The arguments are the hostname/IP, port, keepalive and bind_address (optional, here omitted).
client.connect("10.0.0.1", 1883, 60)

# Subscribe to the topics
client.subscribe(topic_log)
print("Subscribed to topic: " + topic_log)
client.subscribe(topic_positions)
print("Subscribed to topic: " + topic_positions)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()