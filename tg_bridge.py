import json
import datetime
import time
import paho.mqtt.client as mqtt
from config import config as _c
from mqtt_util import MqttUtil as mq_util


class Bridge:
    def __init__(self):
        self.version = _c.VERSION
        self.clients = []
        self.run()

    def run(self):
        print("Let's run here", self.version)
        print("NORTH USER: ", _c.MQTT_SOUTH_USER, ".")
        print("SOUTH USER: ", _c.MQTT_NORTH_USER, ".")

        for plugin in _c.PlUGINS:
            print(plugin["topic"], plugin["plugin"])
            self.clients.append(
                mq_util(plugin["topic"], plugin["plugin"], True)
            )
        # while True:
        #     time.sleep(1)

    def terminate(self):
        print("Let's cleanup")
