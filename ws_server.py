import asyncio
import logging
import websockets
from websockets import WebSocketClientProtocol


class WsServer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.clients = set()
        logging.info(f"hello")

    async def register(self, ws: WebSocketClientProtocol) -> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connected")

    async def unregister(self, ws: WebSocketClientProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnected")

    async def send(self, message: str) -> None:
        if self.clients:
            await asyncio.wait(
                [client.send(message) for client in self.clients]
            )

    async def distribute(self, ws: WebSocketClientProtocol) -> None:
        async for message in ws:
            await self.send(message)

    async def ws_handler(self, ws: WebSocketClientProtocol, uri: str) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)
