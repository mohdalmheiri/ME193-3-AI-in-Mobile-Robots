"""Two-way MQTT text chat.

Type a line and hit Enter to publish it to a shared topic; anything anyone
(including you) publishes to that topic prints live - the same round-trip
subscribe pattern as MQTTLIB.md's "reading back your own publish" example,
just kept running instead of exiting after one message.

Run this on two laptops (or two terminals) with the same channel to chat
between them over the public test.mosquitto.org broker. Ctrl+C to quit.
"""

from mqttlib import MQTTClient

DEFAULT_TOPIC = "ME193"


def on_message(topic, payload):
    # A plain newline + print, not an in-place "\r" redraw: overwriting the
    # active input() line with \r looks fine in some terminals but can
    # visually corrupt or hide the message in others, since input() is also
    # managing that same line via readline.
    print(f"\n{payload}", flush=True)


def main():
    name = input("Your name: ").strip() or "anon"
    topic = input(f"Channel [{DEFAULT_TOPIC}]: ").strip() or DEFAULT_TOPIC

    with MQTTClient() as client:
        client.subscribe(topic, on_message)
        print(f"Connected. Chatting on '{topic}' - Ctrl+C to quit.")
        try:
            while True:
                line = input("> ")
                if line.strip():
                    client.publish(topic, f"{name}: {line}")
        except (KeyboardInterrupt, EOFError):
            print("\nDisconnecting...")


if __name__ == "__main__":
    main()
