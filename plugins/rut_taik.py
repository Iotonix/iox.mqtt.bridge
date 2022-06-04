import copy
import websockets
import json
import datetime
from utils import time_converter as tc
from interfaces.bridge_interface import BridgeInterface
from models.power_sensor import power_sensor_value


class Bridger(BridgeInterface):
    def __init__(self, topic, payload, client):
        print("Rut Plugin initialized")
        self.client = client
        self.transform(topic, payload)

    def transform(self, topic, payload):
        print("Transforming now: ", topic)
        dt_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        sv = payload[0]
        print(sv)
        target_sv = copy.deepcopy(power_sensor_value)
        target_sv["name"] = sv["name"]
        target_sv["sensorId"] = sv["sensorId"]
        target_sv["sensorId"] = 702
        target_sv["measuredAt"] = dt_now
        # target_sv = tc.timestamp_to_iso(target_sv, "measuredAt")
        target_sv = self.t_value_entries(target_sv, sv)
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

    def t_value_entries(self, target, orig_sv):
        sv = copy.deepcopy(orig_sv)
        entries = sv["sensorValueEntries"]
        values = []
        fields = []
        for x in entries:
            if x["propName"] == "Raw":
                values = self.cleanup(x["propValue"])
            if x["propName"] == "Fields":
                fields = self.cleanup(x["propValue"])

        sv["sensorValueEntries"] = []

        num_values = len(values)
        for idx, fld in enumerate(fields):
            field = fld.strip()
            if len(field) > 0 and field[0:1] != "_":
                if idx <= num_values:
                    value = abs(float(values[idx]))
                else:
                    value = -2
                if field in target:
                    target[field] = value
        return target

    def cleanup(self, p_str):
        p_str = p_str.replace("[", "")
        p_str = p_str.replace("]", "")
        return p_str.split(",")
