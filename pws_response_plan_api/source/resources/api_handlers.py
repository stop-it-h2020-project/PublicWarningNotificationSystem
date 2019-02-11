import logging

from flask_restful import reqparse

from pws_common import enums

from errors.api_errors import GENERIC, NOT_EXISTS_ID, EXISTS_ID, FIELD_NOT_VALID
from models.models import ResponsePlan
from resources import Resource, Response
from translators import api_translators as translator
from validators import api_validator as validator

logger = logging.getLogger(__name__)

response_plan_parser = reqparse.RequestParser()
response_plan_parser.add_argument("response_plan_id", type=str)
response_plan_parser.add_argument("message_status", type=int)
response_plan_parser.add_argument("alert_category", type=int)
response_plan_parser.add_argument("alert_severity", type=int)
response_plan_parser.add_argument("actions", type=int, action='append')
response_plan_parser.add_argument("action_parameters", type=str, action='append')
response_plan_parser.add_argument("action_format", type=int, action='append')
response_plan_parser.add_argument("action_description", type=str, action='append')
response_plan_parser.add_argument("action_body", type=str, action='append')
response_plan_parser.add_argument("action_trigger", type=int, action='append')
response_plan_parser.add_argument("accessibility", type=int)
response_plan_parser.add_argument("area", type=str)
response_plan_parser.add_argument("geolocation", type=str)


class ResponsePlanHandler:
    class ResponsePlans(Resource):
        def get(self):
            responses = self.repository.get_responses()

            return Response.success(
                [translator.responseplan_translator(responseplan) for responseplan in responses])

        def post(self):
            args = response_plan_parser.parse_args()

            # Get response_plan arguments
            if validator.is_response_plan_id_valid(args["response_plan_id"]):
                response_plan_id = args["response_plan_id"]

                response = self.repository.get_response_external_id(response_plan_id)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_message_status_valid(args["message_status"]):
                message_status = args["message_status"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_alert_category_valid(args["alert_category"]):
                category = args["alert_category"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_alert_severity_valid(args["alert_severity"]):
                severity = args["alert_severity"]
            else:
                severity = str(enums.AlertSeverityEnum.NORMAL.value)

            if validator.is_actions_valid(args["actions"]):
                actions = str(args["actions"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_parameters_valid(args["action_parameters"]):
                parameters = str(args["action_parameters"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_formats_valid(args["action_format"]):
                format = str(args["action_format"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_descriptions_valid(args["action_description"]):
                description = str(args["action_description"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_bodys_valid(args["action_body"]):
                body = str(args["action_body"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_triggers_valid(args["action_trigger"]):
                trigger = str(args["action_trigger"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_accessibility_valid(args["accessibility"]):
                accessibility = args["accessibility"]
            else:
                accessibility = str(enums.AccessibilityEnum.ADMINISTRATOR.value)

            if validator.is_area_valid(args["area"]):
                area = args["area"]
            else:
                area = ""

            if validator.is_geolocation_valid(args["geolocation"]):
                geolocation = args["geolocation"]
            else:
                return Response.error(FIELD_NOT_VALID)

            response_plan = ResponsePlan(response_plan_id=response_plan_id,
                                         message_status=message_status, alert_category=category,
                                         alert_severity=severity, actions=actions,
                                         action_parameters=parameters, action_format=format,
                                         action_description=description, action_body=body,
                                         action_trigger=trigger, accessibility=accessibility,
                                         area=area, geolocation=geolocation)

            result = self.repository.add_response(response_plan)

            if result:
                return Response.success({"internal_id": result})

            return Response.error(GENERIC)

    class ResponsePlansFilter(Resource):
        def get(self, alert_category):
            responses = self.repository.get_responses(alert_category)

            return Response.success(
                [translator.responseplan_translator(responseplan) for responseplan in responses])

    class ResponsePlan(Resource):
        def get(self, response_id):
            response = self.repository.get_response(response_id)

            if response:
                return Response.success(translator.responseplan_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, response_id=None):
            args = response_plan_parser.parse_args()

            response = self.repository.get_response(response_id)
            if not response:
                return Response.error(NOT_EXISTS_ID)

            # Get response_plan arguments
            if validator.is_response_plan_id_valid(args["response_plan_id"]):
                response_plan_id = args["response_plan_id"]

                response = self.repository.get_response_external_id(response_plan_id)
                if response and response.internal_id != int(response_id):
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_message_status_valid(args["message_status"]):
                message_status = args["message_status"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_alert_category_valid(args["alert_category"]):
                category = args["alert_category"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_alert_severity_valid(args["alert_severity"]):
                severity = args["alert_severity"]
            else:
                severity = str(enums.AlertSeverityEnum.NORMAL.value)

            if validator.is_actions_valid(args["actions"]):
                actions = str(args["actions"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_parameters_valid(args["action_parameters"]):
                parameters = str(args["action_parameters"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_formats_valid(args["action_format"]):
                format = str(args["action_format"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_descriptions_valid(args["action_description"]):
                description = str(args["action_description"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_bodys_valid(args["action_body"]):
                body = str(args["action_body"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_action_triggers_valid(args["action_trigger"]):
                trigger = str(args["action_trigger"])
            else:
                return Response.error(FIELD_NOT_VALID)

            if validator.is_accessibility_valid(args["accessibility"]):
                accessibility = args["accessibility"]
            else:
                accessibility = str(enums.AccessibilityEnum.ADMINISTRATOR.value)

            if validator.is_area_valid(args["area"]):
                area = args["area"]
            else:
                area = ""

            if validator.is_geolocation_valid(args["geolocation"]):
                geolocation = args["geolocation"]
            else:
                return Response.error(FIELD_NOT_VALID)

            response_plan = {
                "response_plan_id": response_plan_id,
                "message_status": message_status,
                "alert_category": category,
                "alert_severity": severity,
                "actions": actions,
                "action_parameters": parameters,
                "action_format": format,
                "action_description": description,
                "action_body": body,
                "action_trigger": trigger,
                "accessibility": accessibility,
                "area": area,
                "geolocation": geolocation
            }

            result = self.repository.modify_response(response_id, response_plan)

            if result:
                return Response.success({"internal_id": result})

            return Response.error(GENERIC)

        def delete(self, response_id=None):
            response = self.repository.get_response(response_id)

            if response:
                result = self.repository.delete_response(response_id)
                if result:
                    return Response.success({"internal_id": result})
            return Response.error(NOT_EXISTS_ID)
