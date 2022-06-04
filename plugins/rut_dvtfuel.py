import copy
import websockets
import json
import datetime
from utils import time_converter as tc
from interfaces.bridge_interface import BridgeInterface
from pymongo import MongoClient
from config import config as _c


class Bridger(BridgeInterface):
    def __init__(self, topic, payload, client):
        print("Rut Plugin initialized")
        self.client = client
        client = MongoClient(_c.MONGO_CONNECT_STRING)
        self.db = client.talegur
        self.transform(topic, payload)

    def transform(self, topic, payload):
        print("Transforming now: ", topic)
        print(payload[0])
        sv = payload[0]
        target_sv = tc.timestamp_to_iso(sv, "measuredAt")
        # Below a FIX. TODO: find our why RUT sends wrong time stamp
        target_sv["measuredAt"] = datetime.datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        target_sv["sensorId"] = 29021
        print(target_sv)
        target_sv = self.t_value_entries(target_sv)
        print("+++++++++++++++++++")
        print(target_sv)
        topic = (
            "amdisx/iot/edge/O/"
            + target_sv["clazz"]
            + "/"
            + str(target_sv["sensorId"])
        )
        print(topic)
        self.client.publish(topic, json.dumps(target_sv))

    def terminate(self):
        print("Cleaning Up")

    def t_value_entries(self, orig_sv):
        sv = copy.deepcopy(orig_sv)
        entries = sv["sensorValueEntries"]
        lng, lat = self.get_coords()
        for x in entries:
            if x["propName"] == "Raw":
                values = self.cleanup(x["propValue"])
                values.append(lat)
                values.append(lng)
                print("Found the values!", values, type(values))
            if x["propName"] == "Fields":
                fields = self.cleanup(x["propValue"])
                print("Found the fields!", fields, type(fields))

        sv["sensorValueEntries"] = [
            {"propName": "_measurement", "propValue": "DVT_EIOT_FUEL"}
        ]

        num_values = len(values)
        for idx, fld in enumerate(fields):
            field = fld.strip()
            if len(field) > 0 and field[0:1] != "_":
                if idx <= num_values:
                    value = float(values[idx])
                else:
                    value = -1
                new_entry = {"propName": field, "propValue": value}
                sv["sensorValueEntries"].append(new_entry)
        return sv

    def get_coords(self):
        last_coords = self.db.gps_track.find_one({}, sort=[("_id", -1)])
        return last_coords["lng"], last_coords["lat"]

    def cleanup(self, p_str):
        p_str = p_str.replace("[", "")
        p_str = p_str.replace("]", "")
        p_str = p_str.rstrip(",")
        return p_str.split(",")
