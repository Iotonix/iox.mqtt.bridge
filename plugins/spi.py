import asyncio
import websockets
import json
from random import uniform
from math import sin, cos, radians, pi, sqrt
from time import sleep
from interfaces.bridge_interface import BridgeInterface


class Bridger(BridgeInterface):
    def __init__(self, topic, payload):
        print("Plugine initialized")
        self.transform(topic, payload)

    def meteorites(self):
        lat = 14.4410
        lng = 100.5962
        spread_lat = (14.4425 - 14.4395) * 1000 / 2  # 15
        spread_lng = (100.5995 - 100.5930) * 1000 / 2  # 32.5
        lat_distance = uniform(-spread_lat, spread_lat) / 1000
        lng_distance = uniform(-spread_lng, spread_lng) / 1000
        return lat + lat_distance, lng + lng_distance

    def transform(self, topic, payload):
        id = "LK-4856"
        print("Transforming now", topic, id)
        for i in range(10):
            latlong = self.meteorites()
            message = {"id": id, "lat": latlong[0], "lng": latlong[1]}
            asyncio.run(self.produce(json.dumps(message)))
            sleep(1)

    async def produce(self, message: str) -> None:
        async with websockets.connect(f"ws://localhost:28106") as ws:
            await ws.send(message)
            await ws.recv()

    def terminate(self):
        print("Cleaning Up")