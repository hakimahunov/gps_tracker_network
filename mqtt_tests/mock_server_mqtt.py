import paho.mqtt.client as mqtt
import random
import time


# GPS coordinate boundaries for Trento.
maxLat = 46.096244200191684
minLat = 46.040603518369856
maxLon = 11.139450300806237
minLon = 11.108262519974287

# Create the MQTT client and define callbacks for connection and messages.
client = mqtt.Client("mock_server")

# Blocking call to connect to the broker.
# The arguments are the hostname/IP, port, keepalive and bind_address (optional, here omitted).
client.connect("10.0.0.1", 1883, 60)

# Simulates a server sending a new message every minute to the drone with ID = "drone1".
while True:
    posToReach = ((random.random()%(maxLat - minLat) + minLat), (random.random()%(maxLon - minLon) + minLon))
    msg = "drone1" + "_" + str(posToReach[0]) + "_" + str(posToReach[1]) + "_"
    client.publish("command_drone1", msg)
    client.publish("log", "Just published " + msg + " to the topic command_drone1")
    time.sleep(60)
