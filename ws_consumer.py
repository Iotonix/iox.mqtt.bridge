import asyncio
import logging
import websockets
from websockets import WebSocketClientProtocol


def main():
    """ The main consumer"""
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume("localhost", 28106))
    loop.run_forever()


async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    async for message in websocket:
        log_message(message)


async def consume(hostname: str, port: int) -> None:
    websocker_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocker_url) as websocket:
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"Message: {message}")


if __name__ == "__main__":
    main()
