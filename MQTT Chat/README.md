# MQTT Chat

Publish/subscribe messaging over MQTT, using the public `test.mosquitto.org`
broker. `mqttlib.py` is a small wrapper around `paho-mqtt` shared by both
demo scripts:

- **`sep22.py`** — subscribe-and-answer demo. Publishes a "hello world" ping
  and, for every non-answer message it receives on the topic, publishes an
  answer back. Run two copies in separate terminals to see them answer each
  other, or run one to see it answer its own opening ping.
- **`chat.py`** — two-way text chat. Type a line and hit Enter to publish it
  to a shared topic; anything anyone (including you) publishes to that topic
  prints live. Run this on two laptops (or two terminals) with the same
  channel name to chat between them.

## Requirements

- Python 3.8+
- An internet connection (uses the public `test.mosquitto.org` broker — no
  local broker setup needed)
- Packages: `paho-mqtt`

```
pip install --upgrade pip
pip install paho-mqtt
```

## Setup

1. Run either script:
   ```
   python sep22.py
   python chat.py
   ```
2. For `chat.py`: enter your name and a channel (defaults to `ME193`) when
   prompted, then type messages and press Enter to send. Run a second copy
   (same channel) in another terminal or on another laptop to chat with it.
   Ctrl+C to quit.

## Notes / limitations

- `test.mosquitto.org` is a shared public broker — anyone using the same
  topic name (e.g. the default `ME193`) will see your messages, so pick a
  more specific channel name in `chat.py` if you want a private conversation.
- `mqttlib.py`'s `MQTTClient` only supports one callback per topic
  (`subscribe()` overwrites any previous callback for that topic).
