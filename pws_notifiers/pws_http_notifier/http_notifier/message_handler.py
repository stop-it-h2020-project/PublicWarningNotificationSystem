# -*- coding: utf-8 -*-

import logging

import requests

import translators
import validator

logger = logging.getLogger(__name__)


class MessageHandler:
    def _send_http_post(self, message, url, format):
        """
        Simple function that sends an HTTP post curl.

        send_http_post("This is a test message", "http://localhost:5000/alerts")
        """

        formatted_message = translators.str_to_format(message, format)

        response = requests.post(url, data={'message': formatted_message})

        logger.info(f"Sending HTTP notification to {url}, message: {formatted_message}")

        return response

    def process_message(self, message_raw):
        url = message_raw["url"]
        message = message_raw["message"]  # Supposing that message is a string
        format = message_raw["format"]

        if (validator.is_url_valid(url) and validator.is_message_valid(message)
                and validator.is_format_valid(format)):
            logger.info(f"Received HTTP notification to {url}, format: {format}, message: {message}")
            response = self._send_http_post(message, url, format)
            return response

        return None
