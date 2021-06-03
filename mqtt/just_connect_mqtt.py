import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Blocking call to connect to the broker.
# The arguments are the hostname/IP, port, keepalive and bind_address (optional)
client.connect("10.0.0.1", 1883, 60)


# Subscribe to the "test_temperature" topic.
test_topic = "test_temperature"
client.subscribe(test_topic)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
