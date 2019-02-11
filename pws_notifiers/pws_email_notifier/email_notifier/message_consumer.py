# -*- coding: utf-8 -*-
import json
import logging

from amqp_rabbit import AMQPRabbit

logger = logging.getLogger(__name__)


class MessageConsumer(AMQPRabbit):
    RECONNECT_TIMEOUT_IN_SECS = 5
    EXCHANGE = None
    EXCHANGE_TYPE = None
    QUEUE = None
    ROUTING_KEY = None

    def __init__(self, message_handler, *args, **kwargs):
        super().__init__(kwargs.get("amqp_url"))
        self.EXCHANGE = kwargs.get("exchange")
        self.EXCHANGE_TYPE = kwargs.get("exchange_type")
        self.QUEUE = kwargs.get("queue")
        self.ROUTING_KEY = kwargs.get("routing_key")
        self.EXCLUSIVE_QUEUE = False
        self.message_handler = message_handler

    def _handle_message(self, _, basic_deliver, properties, body):
        try:
            json_body = json.loads(body.decode("utf8"))
            logger.debug("Received message #{} from {}: {}".format(basic_deliver.delivery_tag,
                                                                   properties.app_id, json_body))
            self.message_handler.process_message(json_body)
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
