import copy
import websockets
import json
import datetime
from utils import time_converter as tc
from interfaces.bridge_interface import BridgeInterface


class Bridger(BridgeInterface):
    def __init__(self, topic, payload, client):
        print("Rut Plugin initialized")
        self.client = client
        self.transform(topic, payload)

    def transform(self, topic, payload):
        print("Transforming now: ", topic)
        print(payload[0])
        sv = payload[0]
        topic = "iox/fog/edge/" + sv["clazz"] + "/" + str(sv["sensorId"])
        print(topic)
        # self.client.publish(topic, json.dumps(target_sv))

    def terminate(self):
        print("Cleaning Up")

    def t_value_entries(self, orig_sv):
        sv = copy.deepcopy(orig_sv)
        entries = sv["sensorValueEntries"]
        for x in entries:
            if x["propName"] == "Raw":
                values = self.cleanup(x["propValue"])
                print("Found the values!", values, type(values))
            if x["propName"] == "Fields":
                fields = self.cleanup(x["propValue"])
                print("Found the fields!", fields, type(fields))

        sv["sensorValueEntries"] = [
            {"propName": "_measurement", "propValue": "ACER_PM"}
        ]

        num_values = len(values)
        for idx, fld in enumerate(fields):
            field = fld.strip()
            if len(field) > 0 and field[0:1] != "_":
                if idx <= num_values:
                    value = int(values[idx])
                else:
                    value = -1
                if field == "Temperature" or field == "Humidty":
                    value = value / 10
                new_entry = {"propName": field, "propValue": value}
                sv["sensorValueEntries"].append(new_entry)
        return sv

    def cleanup(self, p_str):
        p_str = p_str.replace("[", "")
        p_str = p_str.replace("]", "")
        return p_str.split(",")
