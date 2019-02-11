# -*- coding: utf-8 -*-

import requests
import json
import logging

from postgresclient import PostgresClient
from configmanager import ConfigManager


logger = logging.getLogger(__name__)


class AlertEnricher(object):

    def __init__(self, config=None):
        if config is None:
            self.config = ConfigManager().get_specific_configuration("alerts_enricher")
        else:
            self.config = config
        self.db_connection = PostgresClient(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["pass"],
            database=self.config["database"]
        )

    def validate_and_traslate(self, alert_data):

        related_item = alert_data.get("related_item")
        if related_item is None:
            raise ValueError("Key [related_item] not found in input alert")

        item_type = related_item.get("item_type")
        if item_type is None:
            raise ValueError("Key [item_type] not found in input alert")

        translate_alert = getattr(self, item_type, None)
        if not translate_alert:
            raise ValueError("There isn't an alert translator for item_type: %s" % item_type)
        rule, alert = translate_alert(alert_data)
        return rule, alert
    

    def tiltmeter(self, alert_data): # Requiers cos
        cos_host = self.config["cos_host"]
        item_id =  alert_data.get("related_item").get("item_id")
        url = f"{cos_host}/objects/loadsensing_tiltmeter/instances/external/loadsensing_tiltmeter_id/{item_id}"
        metadata = dict()
        try:
            response = requests.get(url)
            if response.status_code != 200:
                response.raise_for_status()
            coordinates = json.loads(response.content).get("custom_fields", None).get("coordinates", None)
            address = "Tiltmeter empty adress"
            metadata = dict(coordinates=coordinates.get("coordinates", None), address=address)
        except Exception as e:
            logger.error("Error %s getting metadata from COS in tiltmeter enricher" % str(e))
        rule, alert = self.generate_alert_and_rule(metadata, alert_data)
        alert["type"] = 10
        alert["title"] = f"Inclination threshold exceeded for tiltmeter {item_id}"

        return rule, alert


    def generate_alert_and_rule(self, metadata, alert_data):
        alert = self.generate_alert(metadata, alert_data)
        rule = self.generate_rule(alert_data)

        alert.update({"rule_id": rule["id"]})

        return rule, alert


    def generate_alert(self, metadata, alert_data):
        absolute_value = alert_data.get("alert").get("absolute_value")
        forecast_value = alert_data.get("alert").get("forecast_value")
        absolute_difference = abs(absolute_value - forecast_value)
        alert = dict(
            meta_type="meta_data",
            sub_type="n/a",
            absolute_value=absolute_value,
            absolute_difference=absolute_difference,
            severity=alert_data.get("alert").get("severity"),
            status=10,
            created_by=alert_data.get("action_stamps").get("created_by"),
            related_item_id=alert_data.get("related_item").get("item_id"),
            related_item_type=alert_data.get("related_item").get("item_type"),
            the_geom={
                "type": "Point",
                "coordinates": metadata.get("coordinates", None)
            }
        )

        description = alert_data.get("alert").get("description", None)
        if description:
            alert.update({"description": description})
        address = metadata.get("address", None)
        if address:
            alert.update({"address": address})
        title = metadata.get("title", None)
        if title:
            alert.update({"title": title})

        return alert

    def generate_rule(self, alert_data):
        rule = None
        rule_id = alert_data.get("rule").get("rule_id", None)

        if rule_id:
            rule = dict(
                id=rule_id,
                name=alert_data.get("rule").get("rule_name"),
                measure_name=alert_data.get("related_item").get("measure_name"),
                measure_unit=alert_data.get("related_item").get("measure_unit"),
                reference_type= "threshold"
            )

        return rule


    @staticmethod
    def query(connection, query):
        return connection.execute_statement(statement=query, fetch=True)
