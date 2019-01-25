import json

import paho.mqtt.client as mqtt
import structlog

from app import config
from app.accessories import ACCESSORIES

logger = structlog.getLogger(__name__)

logger.info("Starting tv-backlight-handler")


def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('commands/tvbacklight')
    logger.info("Connected", rc=str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    accessory = ACCESSORIES.get(1)
    accessory.handle(payload)

    if 'color' in payload:
        topic = "events/tvbacklight/rgb"
        values = ','.join([payload['color'].get(c) for c in list('rgb')])
        client.publish(topic=topic, payload=values, retain=True)

    if 'brightness' in payload:
        topic = "events/tvbacklight/brightness"
        value = payload['brightness']
        client.publish(topic=topic, payload=value, retain=True)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.BROKER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
