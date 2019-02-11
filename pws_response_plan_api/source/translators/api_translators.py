# -*- coding: utf-8 -*-
import json


def actions_translator(actions):
    return json.loads(actions)


def action_parameters_translator(action_parameters):
    return json.loads(action_parameters.replace("'", '"'))


def action_format_translator(action_format):
    return json.loads(action_format)


def action_description_translator(action_description):
    return json.loads(action_description.replace("'", '"'))


def action_body_translator(action_body):
    return json.loads(action_body.replace("'", '"'))


def action_trigger_translator(action_trigger):
    return json.loads(action_trigger)


def accessibility_translator(accessibility_from_db):
    return accessibility_from_db.value


def responseplan_translator(responseplan_from_db):
    return {
        "internal_id": responseplan_from_db.internal_id,
        "response_plan_id": responseplan_from_db.response_plan_id,
        "message_status": responseplan_from_db.message_status,
        "alert_category": responseplan_from_db.alert_category,
        "alert_severity": responseplan_from_db.alert_severity,
        "actions": actions_translator(responseplan_from_db.actions),
        "action_parameters": action_parameters_translator(responseplan_from_db.action_parameters),
        "action_format": action_format_translator(responseplan_from_db.action_format),
        "action_description": action_description_translator(
            responseplan_from_db.action_description),
        "action_body": action_body_translator(responseplan_from_db.action_body),
        "action_trigger": action_trigger_translator(responseplan_from_db.action_trigger),
        "accessibility": responseplan_from_db.accessibility,
        "area": responseplan_from_db.area,
        "geolocation": responseplan_from_db.geolocation
    }
