# -*- coding: utf-8 -*-
import logging
from pprint import pprint
from datetime import datetime, timezone

from eve import Eve
from eve_sqlalchemy import SQL, validation, config

from sqlalchemy.sql.expression import and_
from geoalchemy2 import WKBElement
from flask import current_app
from flask_cors import CORS
from flask_sse import sse
from flask_script import Shell
from werkzeug.exceptions import UnprocessableEntity

from enum import IntEnum
import requests
import json

from configmanager import ConfigManager

from .auxiliary import CustomJSONEncoder, construct_db_uri
from .models import Alert, Rule, ALERT_RESOLVED_STATUS
from .models.common import wkb_to_geojson
from .commands import new_alert, clear_alerts
from .database import get_db
from . import custom_endpoints

from pws_common import enums


logger = logging.getLogger(__name__)
db_config = ConfigManager().get_specific_configuration("database")
debug_mode = ConfigManager().get_specific_configuration("flask_debug_mode")
redis_url = ConfigManager().get_specific_configuration("redis", "url")
external_alerts_module = ConfigManager().get_specific_configuration("external_alerts_module")
response_plans_api = ConfigManager().get_specific_configuration("response_plans_api")
responder_api = ConfigManager().get_specific_configuration("responder_api")


WKBElement.copy = wkb_to_geojson  # PATCH to workaround WKB serialization

swagger_info = {
    'title': 'OneMind Alerts Management Service',
    'version': '1.0.0',
    'description': 'Alerts Service API',
    'schemes': ['http'],
}

RECURRENCE_MESSAGE = "Alert 'operative_status' < {} (not resolved) and with same 'rule_id', " \
                     "'related_item_id' and 'related_item_type' already present in database. " \
                     "Won't be inserted, but recurrence increased".format(ALERT_RESOLVED_STATUS)

DATE_CREATED = "created_at"  # instead of _created
LAST_UPDATED = "updated_at"  # instead of _updated
DATE_FORMAT = "%s.%f"
ALERT_STREAM_URL = '/alert_stream'

_DOMAIN = config.DomainConfig({
    'alerts': config.ResourceConfig(Alert),
    'rules': config.ResourceConfig(Rule)
}).render(date_created=DATE_CREATED, last_updated=LAST_UPDATED)
_DOMAIN["alerts"]["schema"]["the_geom"]["type"] = 'dict'  # PATCH to parse geojson on the API
# PATCH replace embedder Rule by its related_id
_DOMAIN["alerts"]["schema"]["rule_id"] = {'maxlength': 64, 'nullable': True,
                                          'required': False, 'type': 'string'}
_DOMAIN["alerts"]["datasource"]["projection"]["rule_id"] = 1
_DOMAIN["alerts"]["datasource"]["projection"]["rule"] = 0

coerce_date = lambda x: datetime.utcfromtimestamp(x).replace(tzinfo=timezone.utc)
for domain in _DOMAIN:
    for key, value in _DOMAIN[domain]["schema"].items():
        if value["type"] == "datetime":
            _DOMAIN[domain]["schema"][key]["coerce"] = coerce_date

EVE_SETTINGS = {
    "DEBUG": debug_mode,
    "DATE_CREATED": DATE_CREATED,
    "LAST_UPDATED": LAST_UPDATED,
    "DATE_FORMAT": DATE_FORMAT,
    "SQLALCHEMY_DATABASE_URI": construct_db_uri(db_config),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "RESOURCE_METHODS": ['GET', 'POST'],  # For Collection methods
    "ITEM_METHODS": ['GET', 'PATCH'],  # For Detail methods
    "DOMAIN": _DOMAIN,
    "SSE_REDIS_URL": f"redis://{redis_url}",
    "ALERT_STREAM": True  # NOTE Workaround to allow tests
}


def catch_wrong_http_response(response):
    if not response.ok:
        response.raise_for_status()


def forward_alert(alert):
    response = requests.post(external_alerts_module, json=alert)
    catch_wrong_http_response(response)
    return True


def execute_automatic_response(alert):
    response_response_plans = requests.get(response_plans_api + str(alert["type"]))
    catch_wrong_http_response(response_response_plans)

    for plan in json.loads(response_response_plans.text)["data"]:
        if enums.PlanAutomation.AUTOMATIC in plan["action_trigger"]:
            data_to_send = {"data": {"response_plan": plan,
                                     "alert": {"title": alert["title"],
                                               "id": alert["id"],
                                               "type": alert["type"],
                                               "severity": alert["severity"],
                                               "description": alert["description"]}}}
            response_responder = requests.post(responder_api, json=data_to_send)

            catch_wrong_http_response(response_responder)
            return True
    return False


def on_alert_posted(alerts):
    for alert in alerts:
        logger.debug(f"Alert {alert['id']} published.")
        sse.publish(alert, type='alert')
        if alert["operative_status"] == enums.OperativeStatus.CONFIRMED:
            try:
                execute_automatic_response(alert)
            except Exception as e:
                logger.error("Error executing automatic response plan: %s" % e)


def on_alert_updated(updates, alert):
    logger.debug(f"Alert {alert['id']} updated.")
    updates["id"] = alert["id"]
    if alert["operative_status"] < enums.OperativeStatus.CONFIRMED <= updates.get("operative_status", 0):
        try:
            alert_forwarded = forward_alert(alert)  # TODO: forward alerts only if specified in config, not by default
        except Exception as e:
            logger.error("Error forwarding alert to external module: %s" % e)
            alert_forwarded = False
        try:
            automatic_response_executed = execute_automatic_response(alert)
        except Exception as e:
            logger.error("Error executing automatic response plan: %s" % e)
            automatic_response_executed = False

        new_status = alert["status"]
        if alert_forwarded:
            new_status |= enums.Status.FORWARDED
        if automatic_response_executed:
            new_status |= enums.Status.AUTOMATIC_RESPONSE_PLAN_EXECUTED

        if new_status != alert["status"]:
            db = get_db(current_app)
            db.engine.execute("update alerts set status = {} where id = {}".format(new_status, alert["id"]))

    sse.publish(updates, type='alert_updated')


def forbid_id(alerts):
    for alert in alerts:
        if "id" in alert:
            raise UnprocessableEntity("'id' field is not allowed.")
        if "rule" in alert:
            raise UnprocessableEntity("'rule' field is not allowed. Use 'rule_id'.")


def forbid_repeated(alerts):
    for alert in alerts:
        sql_query = f"select id from alerts where ("

        for column in ["rule_id", "related_item_id", "related_item_type"]:
            value = alert.get(column)
            if value is None:
                sql_query += f"{column} is null AND "
            else:
                sql_query += f"{column} = '{value}' AND "

        sql_query += f"operative_status < {enums.OperativeStatus.RESOLVED});"

        db = get_db(current_app)

        ret = db.engine.execute(sql_query)

        matched = ret.fetchall()
        n_matched = len(matched)
        if n_matched > 0:
            if n_matched > 1:
                logger.warning(f"{n_matched} open alerts found in DB with same rule and related item. "
                               f"Maximum should be 1, since duplicates aren't inserted")
            for match in matched:
                db.engine.execute("update alerts set recurrence = recurrence + 1 where id = {}".format(match[0]))
            raise UnprocessableEntity(f"Alert 'operative_status' < {enums.OperativeStatus.RESOLVED} (not resolved) "
                                      "and with same 'rule_id', 'related_item_id' and 'related_item_type' already "
                                      "present in database. Won't be inserted, but recurrence increased")


def add_swagger(the_app):
    from eve_swagger import swagger, add_documentation
    from .auxiliary import construct_alert_stream_doc
    logger.info("Generating Swagger documentation")
    add_documentation(construct_alert_stream_doc(ALERT_STREAM_URL))
    the_app.register_blueprint(swagger)
    the_app.config["SWAGGER_INFO"] = swagger_info


def create_app(settings=EVE_SETTINGS):
    logger.info("Connecting to DB %s", EVE_SETTINGS["SQLALCHEMY_DATABASE_URI"])
    app = Eve(settings=settings, json_encoder=CustomJSONEncoder, validator=validation.ValidatorSQL, data=SQL)
    app.json_encoder = CustomJSONEncoder
    if EVE_SETTINGS["ALERT_STREAM"]:
        app.register_blueprint(sse, url_prefix=ALERT_STREAM_URL)

    app.on_insert_alerts += forbid_id
    app.on_insert_alerts += forbid_repeated
    app.on_inserted_alerts += on_alert_posted
    app.on_updated_alerts += on_alert_updated

    custom_endpoints.add_custom_endpoints(app)

    app.cli.add_command(new_alert)
    app.cli.add_command(clear_alerts)
    if debug_mode:
        add_swagger(app)

    with app.app_context():
        db = get_db(app)
        db.create_all(app=app)

    # Automatize imports in shell
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app, db=db,
            pprint=pprint,
            Alert=Alert, Rule=Rule)

    app.cli.add_command('shell', Shell(make_context=make_shell_context, use_ipython=True))
    CORS(app)  # Needed for Flask SSE
    return app, db  # Returns db for dev purposes
