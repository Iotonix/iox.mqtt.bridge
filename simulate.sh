#!/bin/bash
export MQTT_NORTH_SERVER=localhost
export MQTT_NORTH_PORT=28186
export MQTT_NORTH_USER=writer
export MQTT_NORTH_PASSWORD=CamelsDrinkLotsOfGin!123

#what sensot to be simulated
export SIMULATOR=jv-technotron
#nr of events to be created
export SIMULATOR_EVENTS=10
#sample rate in seconds
export SIMULATOR_SAMPLING_RATE=1
export SIMULATOR_TOPIC=iot-2/evt/sa_spn_26100_26101/fmt/json


python3 simulator.py