""" this bridge bridges incomming MQTT messages and forwards them to talegur"""
import sys
import signal
import asyncio
import websockets
from time import sleep
from tg_bridge import Bridge


def main():
    """ The main bridge"""
    _ = Bridge()
    while True:
        sleep(1)


if __name__ == "__main__":
    main()
