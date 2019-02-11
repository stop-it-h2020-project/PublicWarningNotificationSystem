# -*- coding: utf-8 -*-
import logging
import requests
import json
from configmanager import ConfigManager
from urllib.parse import urlencode, quote_plus

logger = logging.getLogger(__name__)

RULE_ENDPOINT = "{host}/rules"
ALERT_ENDPOINT = "{host}/alerts"
RULE_FILTER_ENDPOINT = "{host}/rules?where={statement}"

class AlertsInserter:

    def __init__(self, config=None):
        self.config = config or ConfigManager().get_specific_configuration("alerts_inserter")
        self.api_host = self.config.get("api_host")

    def send_alert(self, rule, alert):
        self.create_if_does_nots_exist(rule)
        self.post_alert(alert)

    def create_if_does_nots_exist(self, rule):
        if rule:
            rule_id = rule.get("id")
            statement = quote_plus(json.dumps(dict(id=rule_id)))
            try:
                response = requests.get(
                    RULE_FILTER_ENDPOINT.format(
                        host=self.api_host,
                        statement=statement
                    )
                )
                rule_in_db = json.loads(response.content)
                if rule_in_db["_meta"]["total"] == 0:
                    response = requests.post(RULE_ENDPOINT.format(host=self.api_host), json=rule)
                    if response.status_code != 200:
                        response.raise_for_status()
            except Exception as e:
                logger.error("Error in create_or_update_rule: %s" % e)

    def post_alert(self, alert):
        try:
            response = requests.post(ALERT_ENDPOINT.format(host=self.api_host), json=alert)
            if response.status_code != 200:
                response.raise_for_status()
        except Exception as e:
            logger.error("Error in post_alert: %s" % e)
