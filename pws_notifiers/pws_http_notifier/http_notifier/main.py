#!/usr/bin/env python

import logging

from configurelogging import ConfigureLogging
from configmanager import ConfigManager

from message_consumer import MessageConsumer
from message_handler import MessageHandler

logger = logging.getLogger(__name__)


class HTTPNotifier:
    def __init__(self, handler, consumer):
        self.handler = handler
        self.consumer = consumer

    def init(self, ):
        try:
            logger.info("HTTP Notifier initialization...")
            self.consumer.run()
        except Exception as e:
            logger.exception(e)
        finally:
            logger.info("HTTP Notifier :: Finish execution")


if __name__ == "__main__":
    config = ConfigManager().configuration
    ConfigureLogging(**config["logger"])
    try:
        handler = MessageHandler()
        consumer = MessageConsumer(handler, **config.get("rabbit"))
        HTTPNotifier(handler, consumer).init()
    except:
        logger.info("HTTP Notifier :: Finish execution")
