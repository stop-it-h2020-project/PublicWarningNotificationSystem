# -*- coding: utf-8 -*-

import json
import logging

from configmanager import ConfigManager
from datetime import datetime
from queue_consumer import QueueConsumer
from enricher import AlertEnricher
from inserter import AlertsInserter


logger = logging.getLogger(__name__)


class AlertsProcessor(QueueConsumer):

    RECONNECT_TIMEOUT_IN_SECS = 10

    def __init__(self, config=None):
        self.config = config or ConfigManager().get_specific_configuration("alerts_processor")
        super().__init__(self.config["amqp_url"])
        self.exchange = self.config["exchange"]
        self.exchange_type = self.config["exchange_type"]
        self.queue = self.config["queue"]
        self.routing_key = self.config["routing_key"]
        self.alerts_enricher = AlertEnricher()
        self.alerts_inserter = AlertsInserter()

    def _handle_message(self, channel, basic_deliver, properties, body):
        try:
            alert = json.loads(body)
            enriched_rule, enriched_alert = self.alerts_enricher.validate_and_traslate(alert)
            self.alerts_inserter.send_alert(enriched_rule, enriched_alert)
        except Exception as e:
            logger.error(str(e))

    def on_message(self, channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        self._handle_message(channel, basic_deliver, properties, body)
        self.acknowledge_message(basic_deliver.delivery_tag)
