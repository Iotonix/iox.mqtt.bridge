import sys
import paho.mqtt.client as paho_mqtt
import json
import datetime
import importlib
from pymongo import MongoClient
from config import config as _c


class MqttUtil:
    def __init__(self, topic=None, plugin=None, persist=False):
        self.topic = topic
        self.plugin = plugin
        self.persist = persist

        self.init_north()
        self.init_south()
        print(_c.MONGO_CONNECT_STRING)
        client = MongoClient(_c.MONGO_CONNECT_STRING)
        self.db = client.talegur
        plugin_name = "plugins." + plugin
        print(plugin_name)
        self.plugin_module = importlib.import_module(plugin_name, ".")

    def init_north(self):
        print("Initializing North: (Outbound)", _c.MQTT_NORTH_SERVER)
        self.north = paho_mqtt.Client()
        if len(_c.MQTT_NORTH_USER) > 0:
            print(
                "setting north user:",
                _c.MQTT_NORTH_USER,
                ":",
                _c.MQTT_NORTH_PASSWORD,
            )
            self.north.username_pw_set(
                _c.MQTT_NORTH_USER, _c.MQTT_NORTH_PASSWORD
            )
        try:
            self.north.connect(
                _c.MQTT_NORTH_SERVER, int(_c.MQTT_NORTH_PORT), 45
            )
        except Exception as e:
            print(
                "NORTH connection failed! ",
                _c.MQTT_NORTH_SERVER,
                _c.MQTT_NORTH_PORT,
                _c.MQTT_NORTH_USER,
                _c.MQTT_NORTH_PASSWORD,
            )
            print(e)
            exit(2)
        self.north.loop_start()
        print("started MQTT NORTH bound route")

    def init_south(self):
        print("Initializing South: (Inbound)", _c.MQTT_SOUTH_SERVER)
        self.south = paho_mqtt.Client()
        self.south.on_message = self.on_message_in
        self.south.on_connect = self.on_connect_south
        if len(_c.MQTT_SOUTH_USER) > 0:
            print(
                "setting south user:",
                _c.MQTT_SOUTH_USER,
                ":",
                _c.MQTT_SOUTH_PASSWORD,
            )
            self.south.username_pw_set(
                _c.MQTT_SOUTH_USER, _c.MQTT_SOUTH_PASSWORD
            )

        try:
            self.south.connect(
                _c.MQTT_SOUTH_SERVER, int(_c.MQTT_SOUTH_PORT), 45
            )
        except Exception as e:
            print(
                "SOUTH connection failed! ",
                _c.MQTT_SOUTH_SERVER,
                _c.MQTT_SOUTH_PORT,
                _c.MQTT_SOUTH_USER,
                _c.MQTT_SOUTH_PASSWORD,
            )
            print(e)
            exit(3)
        self.south.loop_start()
        print("started MQTT SOUTH bound route")

    def on_connect_south(self, client, userdata, flags, rc):
        print("\nInbound Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message_in(self, client, userdata, msg):
        print("Received:", msg.topic)
        # print(str(msg.payload))
        try:
            event = msg.payload.decode("utf-8")
            iot_obj = json.loads(event)
            if self.persist:
                print("persisting")
                self.save_data(msg.topic, iot_obj)
            self.plugin_module.Bridger(msg.topic, iot_obj, self.north)
        except Exception as e:
            print(e)
            print("\n01-None JSON Message. Continue:" + msg.topic)
            pass

    def save_data(self, topic, data):
        print("saving", topic)
        rec = {
            "topic": topic,
            "cfgTopic": self.topic,
            "savedAt": datetime.datetime.now().strftime(_c.TIME_FORMAT),
            "sensorValue": data,
        }
        self.db[self.plugin].insert_one(rec)

    def terminate(self):
        print("Terminating", self.plugin)
        self.north.loop_stop()
        self.south.loop_stop()
        self.north.disconnect()
        self.south.disconnect()
