# -*- coding: utf-8 -*-

import logging
import time
import pika
import json


logger = logging.getLogger(__name__)


class QueueSender(object):

    def __init__(self, config):
        self._exchange = config.get("exchange")
        self._url = config.get("amqp_url")
        self._routing_key = config.get("routing_key")
        self._exchange_type = config.get("exchange_type")
        self.init_broker_connection()
        self.connected = False

    def init_broker_connection(self):
        self.connected = False
        count = 0
        while not self.connected:
            try:
                self.connect()
                self.connected = True
            except Exception as e:
                count += 1
                logger.error(e)
                if count > 5:
                    return
                logger.info("Trying to reconnect in 1 second")
                time.sleep(1)

    def connect(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self._url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type)

    def publish(self, message, should_reconnect=True):
        try:
            self.channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._routing_key,  # pws.notifications...
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
        except Exception as e1:
            logger.error(e1)
            try:
                if should_reconnect:
                    logger.info("Trying to reconnect to broker")
                    self.connect()
                    self.send_points(message, should_reconnect=False)
            except Exception as e:
                logger.error("Couldn't reconnect to broker")
                logger.error(e)
                return

    def close(self):
        try:
            if self.connected:
                self.close()
        except Exception as e:
            pass