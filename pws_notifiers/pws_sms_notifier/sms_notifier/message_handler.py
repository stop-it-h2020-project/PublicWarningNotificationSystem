# -*- coding: utf-8 -*-

import logging

from twilio.rest import Client

logger = logging.getLogger(__name__)


class MessageHandler:

    def __init__(self, *args, **kwargs):
        self.account = kwargs.get("account")
        self.token = kwargs.get("token")
        self.sender = kwargs.get("sender")
        self.msg = kwargs.get("msg")
        self.client = Client(self.account, self.token)

    def _send_twilio_sms(self, message, recipient, sender):
        """
        Simple function that sends an SMS using Twilio service.
        Credentials inserted here correspond to a trial account created for
        testing purposes only by tmartinez@worldsensing.com

        >>> send_twilio_sms("This is a test message",
        ...                 "+34911061312",
        ...                 "+34644394179")
        """

        if not recipient.startswith("+"):
            recipient = "+{}".format(recipient)
        if not sender.startswith("+"):
            sender = "+{}".format(sender)

        self.client.messages.create(to=recipient, from_=sender, body=message)

    def process_message(self, message_raw):
        recipients = message_raw["receiver_phones"]
        sender = self.sender
        message = message_raw["message"]

        for recipient in recipients.split(","):
            try:
                self._send_twilio_sms(message, recipient, sender)
                logger.info("Sent SMS notification to number {}. msg: {}".format(recipient,
                                                                                 message))
            except Exception as ex:
                logger.error("Error Sending SMS notification to number {}. {}".format(recipient,
                                                                                      ex))
