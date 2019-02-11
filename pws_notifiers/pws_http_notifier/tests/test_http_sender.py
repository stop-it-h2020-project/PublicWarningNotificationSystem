import json
from unittest.mock import patch, MagicMock

import pytest
from configmanager import ConfigManager

from message_consumer import MessageConsumer
from message_handler import MessageHandler

from tests.fixtures import *


@pytest.mark.parametrize("message, url, format", [
    ("hello world", "https://postman-echo.com/post", 10),
    ("{'to': 'person_in_charge', 'body': 'TEST 1'}", "https://postman-echo.com/post", 10),
    (json.dumps([alert, response_plan_httppost_cap]), "https://postman-echo.com/post", 20),
    ("hello world", "https://postman-echo.com/post", 30)
])
def test_http_sender_unit(message, url, format):
    # Fake message from queue

    message_raw = {
        "url": url,
        "message": message,
        "format": format
    }
    response = MessageHandler().process_message(message_raw)

    assert response.status_code == 200


# Skipped test because it needs an API accepting this request
@pytest.mark.skip
@pytest.mark.parametrize("message, url, format", [
    (json.dumps([alert, response_plan_httppost_cap]), "http://localhost:5001", 20)

])
def test_http_sender_integration(message, url, format):
    # Fake message from queue

    message_raw = {
        "url": url,
        "message": message,
        "format": format
    }
    response = MessageHandler().process_message(message_raw)

    assert response.status_code == 200


@patch("pika.channel.Channel")
@patch("pika.spec.Basic.Deliver")
@patch("pika.spec.BasicProperties")
@pytest.mark.parametrize("message, url, format", [
    ("hello world", "https://postman-echo.com/post", 10)
])
def test_http_sender_queue(properties, deliver, channel, message, url, format):
    # Add message to queue

    message_raw = {
        "url": url,
        "message": message,
        "format": format
    }

    config = ConfigManager().configuration
    message_handler = MessageHandler()
    consumer = MessageConsumer(message_handler, **config.get("rabbit"))
    message_handler._send_http_post = MagicMock()

    consumer._handle_message(channel, deliver, properties, json.dumps(message_raw).encode("utf8"))

    assert message_handler._send_http_post.called
