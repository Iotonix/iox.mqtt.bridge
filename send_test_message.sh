#!/bin/bash

mosquitto_pub -h 203.155.13.171 -p 28186 -u admin -P AMDIS12345678 -t iot-2/evt/100_190/fmt/format_string -m "2142"
mosquitto_pub -h 203.155.13.171 -p 28186 -u admin -P AMDIS12345678 -t iot-2/evt/100_521127/fmt/format_string -m "2201"
