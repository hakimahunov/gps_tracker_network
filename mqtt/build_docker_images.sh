#!/bin/bash

echo "Downloading the base docker image for the MQTT broker."
docker pull eclipse-mosquitto

echo "Building a custom docker image with a different conf file for the MQTT broker."
docker build -t broker_mqtt_client --file ./DockerfileMyMosquitto .

echo "Building a docker image for the drone MQTT client."
docker build -t drone_mqtt_client --file ./DockerfileDroneMQTTClient .

echo "Building a docker image for the my dev test image."
docker build -t my_dev_test --file ./DockerfileMyDevTest .



