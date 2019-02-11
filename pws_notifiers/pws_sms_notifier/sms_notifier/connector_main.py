#!/usr/bin/env python

import logging

from configurelogging import ConfigureLogging
from configmanager import ConfigManager

from message_consumer import MessageConsumer
from message_handler import MessageHandler

logger = logging.getLogger(__name__)


class SmsNotifier:

    def __init__(self, handler, consumer):
        self.handler = handler
        self.consumer = consumer

    def init(self, ):
        try:
            logger.info("SMS Notifier initialization...")
            self.consumer.run()
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info("SMS Notifier :: Finish execution")


if __name__ == "__main__":
    config = ConfigManager().configuration
    ConfigureLogging(**config["logger"])
    try:
        handler = MessageHandler(**config.get("sms"))
        consumer = MessageConsumer(handler, **config.get("rabbit"))
        SmsNotifier(handler, consumer).init()
    except:
        logger.info("SMS Notifier :: Finish execution")
