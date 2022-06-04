import os
import json
import importlib
import time
from simulators.evt_canup import coords


def main():
    """ The main simulator"""
    plugin_name = "simulators." + os.environ.get("SIMULATOR", None)
    print(plugin_name)
    events_to_send = os.environ.get("SIMULATOR_EVENTS", 1)
    sampling_rate = os.environ.get("SIMULATOR_SAMPLING_RATE", 1)
    plugin_module = importlib.import_module(plugin_name, ".")
    plugin = plugin_module.Simulator()  # here we connect and setup

    events_to_send = len(coords)

    for i in range(int(events_to_send)):
        plugin.simulate(i)
        time.sleep(int(sampling_rate))
    plugin.terminate()
    exit(0)


if __name__ == "__main__":
    main()
