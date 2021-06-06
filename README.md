# Drones GPS tracker

## Project description

This project has been implemented by the following contributors as part of the PhD course [Computing in Communication Networks](https://ict.unitn.it/node/889):

* [Francesco Riz](https://webapps.unitn.it/du/it/Persona/PER0185299)
* [Stefano Berlato](https://www.dibris.unige.it/berlato-stefano)
* [Khakim Akhunov](https://webapps.unitn.it/du/en/Persona/PER0230856/Didattica)

### Requirements

* The [comnetsemu](https://git.comnets.net/public-repo/comnetsemu) virtual machine

### Functionality

The topology of the system's network is presented in the figure below. The aim of the system is to allow the user to move the drones by sending a command to the web server and to observe the drones current position on a map in a web-browser. The functionality of the network's components are the following:

* Client 
  - sends the request to the web server containing ID and new coordinates (longitude and latitude) of a drone
  - displays the drones position in a web-browser
  - sends the request to the web server to generate a .kml file suitable for uploading to Google Maps application
* Web server
  - responds to the client, sending back an html web page or generating a .kml file
  - subscribes to a topic within MQTT protocol
  - publish a message within MQTT protocol when drone movement is needed
* MQTT broker (refer to the separate folder)
* Drone
  - moves to a new position
  - subscribes to a topic within MQTT protocol
  - publish a message within MQTT protocol when drone coordinates are required
* Controller
  - manages the SDN (Software Defined Network)

### Topology

The network is sliced into three parts delineated by different colors in the figure. Devices belonging to different subnets are not able to communicate to each other.

![](topology.png)

## Content of the project

TBD

## How to Run

TBD
