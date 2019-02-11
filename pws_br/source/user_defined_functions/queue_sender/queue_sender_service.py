import json
import time
import logging

import pika

from alert_definition import AlertDefinition
import udf_types

ERROR_FIELD_BROKER_MISSING = "You must supply a broker address."
ERROR_FIELD_QUEUE_MISSING = "You must supply a queue name."
ERROR_FIELD_NAME_MISSING = "You must supply a data name."

"""
Sends the received data to a queue.
The options it has are:
   broker - the address of the queue broker
   queue - the queue to which data will be sent
   name - name of the measurements that will be sent
"""

logger = logging.getLogger(__name__)


class QueueSenderHandler(object):
    def __init__(self):
        self._broker = "amqp://mbrabbitmq/"
        self._exchange = "om.alerts"
        self._exchange_type = "topic"
        self._item_type = ""
        self._options = None
        # Sample, to send just a point
        self.point = None
        self.alert_definition = None

    def get_options(self):
        options = {
            "broker": udf_types.STRING,
            "queue": udf_types.STRING,
            "item_type": udf_types.STRING,
            "measure_name": udf_types.STRING,
            "measure_unit": udf_types.STRING,
            "rule_id": udf_types.STRING,
            "rule_name": udf_types.STRING,
            "threshold": udf_types.DOUBLE,
            "severity": udf_types.INT
        }
        return options

    def init(self, options):
        self._options = options
        success = True
        msg = ''
        for opt in options:
            if opt.name == "broker":
                self._broker = opt.values[0].stringValue
                if "?" in self._broker:
                    self._broker += "&heartbeat_interval=0"
                else:
                    self._broker += "?heartbeat_interval=0"
            elif opt.name == "queue":
                self._exchange = opt.values[0].stringValue
            elif opt.name == "item_type":
                self._item_type = opt.values[0].stringValue

        if self._broker is None or self._broker == '':
            success = False
            msg += ERROR_FIELD_BROKER_MISSING
        if self._exchange is None or self._exchange == '':
            success = False
            msg += ERROR_FIELD_QUEUE_MISSING
        if self._item_type is None or self._item_type == '':
            success = False
            msg += ERROR_FIELD_NAME_MISSING
        if not success:
            raise Exception(msg)
        self.alert_definition = AlertDefinition(self._options)
        self.init_broker_connection()

    def init_broker_connection(self):
        connected = False
        count = 0
        while not connected:
            try:
                self.connect()
                connected = True
            except Exception as e:
                count += 1
                logger.error(str(e))
                if count > 5:
                    return logger.error("Trying to reconnect in 1 second")
                time.sleep(1)

    def connect(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self._broker))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type)

    def snapshot(self):
        return {}

    def restore(self, data):
        pass

    def begin_batch(self, begin_req):
        self.point = None

    def process_point(self, point):
        self.point = point
        return {}

    def end_batch(self, end_req):
        if self.point is not None:
            data = self.alert_definition.get_alert(self.point)
            self.send_alert(data)

    def send_alert(self, data, should_reconnect=True):
        try:
            self.channel.basic_publish(
                exchange=self._exchange,
                routing_key="bre.alerts.{}".format(self._item_type),  # pws.alerts.tiltmeter
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
        except Exception as e1:
            logger.error(str(e1))
            try:
                if should_reconnect:
                    logger.error("Trying to reconnect to broker")
                    self.connect()
                    self.send_alert(data, should_reconnect=False)
            except Exception as e:
                logger.error(str(e))
                return
