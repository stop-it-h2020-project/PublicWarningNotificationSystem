import json
import pytest
from unittest.mock import patch

from configmanager import ConfigManager

from message_handler import MessageHandler
from message_consumer import MessageConsumer


@patch("twilio.rest.Client")
@patch("pika.channel.Channel")
@patch("pika.spec.Basic.Deliver")
@patch("pika.spec.BasicProperties")
@pytest.mark.parametrize("message, to, fixed_to", [
    ("hello world", "123456789", "+123456789"),
    ("", "+123456789", "+123456789")
])
def test_sms_sender(properties, deliver, channel, twilio_client, message, to, fixed_to):
    config = ConfigManager().configuration
    handler = MessageHandler(**config.get("sms"))
    handler.client = twilio_client
    consumer = MessageConsumer(handler, **config.get("rabbit"))

    consumer._handle_message(channel, deliver, properties, json.dumps({
        "receiver_phones": to,
        "message": message
    }).encode("utf8"))

    twilio_client.messages.create.assert_called_once_with(body=message,
                                                          from_=config.get("sms").get("sender"),
                                                          to=fixed_to)
