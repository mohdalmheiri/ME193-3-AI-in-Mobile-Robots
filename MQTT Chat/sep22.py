"""MQTT subscribe-and-answer demo.

Subscribes to a topic on a public test broker and, whenever a message
arrives that isn't one of our own replies, publishes an answer back on the
same topic - the request/response pattern from MQTTLIB.md's "reading back
your own publish" example, extended so every non-answer message gets one.

Run two copies in separate terminals to see them answer each other, or just
run one to see it answer its own opening "hello world" ping.
"""

import time

from mqttlib import MQTTClient

TOPIC = "ME193"
ANSWER_PREFIX = "answer: "  # marks our own replies so we don't answer ourselves forever


def on_message(topic, payload):
    print(f"Got it back: [{topic}] {payload}")

    if payload.startswith(ANSWER_PREFIX):
        return  # this is a reply (ours or someone else's) - don't answer an answer

    reply = f"{ANSWER_PREFIX}{payload}"
    client.publish(topic, reply)
    print(f"Published '{reply}' to '{topic}'")


with MQTTClient() as client:
    client.subscribe(TOPIC, on_message)
    time.sleep(1)  # give the subscription time to reach the broker
    client.publish(TOPIC, "hello world")
    print(f"Published 'hello world' to '{TOPIC}'")
    time.sleep(2)  # give the message (and the answer to it) time to come back
