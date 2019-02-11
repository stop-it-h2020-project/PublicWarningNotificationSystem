import pytest
import json

from unittest.mock import patch, ANY

from configmanager import ConfigManager

from message_handler import MessageHandler
from message_consumer import MessageConsumer


@patch("smtplib.SMTP")
@patch("pika.channel.Channel")
@patch("pika.spec.Basic.Deliver")
@patch("pika.spec.BasicProperties")
@pytest.mark.parametrize("sender, recipients, subject, message", [
    ("fastprk.app@gmail.com", "test@worldsensing.com", "Test message", "<html>Test message</html>")
])
def test_email_sender(properties, deliver, channel, server, sender, recipients, subject, message):

    def _build_server():
        return server

    config = ConfigManager().configuration
    handler = MessageHandler(**config.get("smtp"))
    handler._build_server = _build_server
    consumer = MessageConsumer(handler, **config.get("rabbit"))

    consumer._handle_message(channel, deliver, properties, json.dumps({
        "receiver_emails": recipients,
        "message_html": message,
        "title": subject
    }).encode("utf8"))

    server.sendmail.assert_called_once_with(sender, 'test@worldsensing.com', ANY)
