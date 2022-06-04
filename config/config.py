import os

VERSION = "1.0.12"

MQTT_NORTH_SERVER = os.environ.get("MQTT_NORTH_SERVER", default="ax-activemq")
MQTT_NORTH_PORT = os.environ.get("MQTT_NORTH_PORT", default=1883)
MQTT_NORTH_USER = os.environ.get("MQTT_NORTH_USER", default="writer")
MQTT_NORTH_PASSWORD = os.environ.get(
    "MQTT_NORTH_PASSWORD", default="CamelsDrinkLotsOfGin!123"
)

MQTT_SOUTH_SERVER = os.environ.get("MQTT_SOUTH_SERVER", default="ax-activemq")
MQTT_SOUTH_PORT = os.environ.get("MQTT_SOUTH_PORT", default=1883)
MQTT_SOUTH_USER = os.environ.get("MQTT_SOUTH_USER", default="reader")
MQTT_SOUTH_PASSWORD = os.environ.get(
    "MQTT_SOUTH_PASSWORD", default="CamelsDonTDrinkLotsOfGin!456"
)

MONGO_CONTAINER = os.getenv("MONGO_CONTAINER", "localhost")
MONGO = {
    "user": os.getenv("APPLICATION_MONGO_USER", "tgadmin"),
    "pw": os.getenv("APPLICATION_MONGO_PW", "ait1234"),
    "host": os.getenv("APPLICATION_MONGO_HOST", MONGO_CONTAINER),
    "port": os.getenv("APPLICATION_MONGO_PORT", 28105),
    "db": os.getenv("APPLICATION_MONGO_DB", "talegur"),
}

MONGO_CONNECT_STRING = (
    "mongodb://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s?authSource=admin"
    % MONGO
)

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

PlUGINS = [
    # {
    #     "topic": "iot-2/evt/#",
    #     "plugin": "spi",
    #     "persist": int(os.environ.get("PERSIST_SPI", default=0)),
    # },
    # {
    #     "topic": "talegur/bridge/Acer/#",
    #     "plugin": "rut_acer",
    #     "persist": int(os.environ.get("PERSIST_SPI", default=0)),
    # },
    # {
    #     "topic": "talegur/bridge/Taik/#",
    #     "plugin": "rut_taik",
    #     "persist": int(os.environ.get("PERSIST_SPI", default=0)),
    # },
    # {
    #     "topic": "talegur/bridge/Dvtfuel/#",
    #     "plugin": "rut_dvtfuel",
    #     "persist": int(os.environ.get("PERSIST_SPI", default=0)),
    # },
    {
        "topic": "amdisx/edge/cloud/O/#",
        "plugin": "iox_na",
        "persist": 0,
    },
]
