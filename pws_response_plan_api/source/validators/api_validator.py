from pws_common import enums


def is_response_plan_id_valid(response_plan_id):
    return isinstance(response_plan_id, str) and not response_plan_id == ""


def is_message_status_valid(message_status):
    try:
        if not isinstance(message_status, int):
            return False

        return enums.MessageStatusEnum.has_value(message_status)
    except:
        return False


def is_alert_category_valid(alert_category):
    try:
        if not isinstance(alert_category, int):
            return False

        return enums.AlertCategoryEnum.has_value(alert_category)
    except:
        return False


def is_alert_severity_valid(alert_severity):
    try:
        if not isinstance(alert_severity, int):
            return False

        return enums.AlertSeverityEnum.has_value(alert_severity)
    except:
        return False


def is_actions_valid(actions):
    if not isinstance(actions, list):
        return False

    try:
        for action in actions:
            if not isinstance(action, int):
                return False

            if not enums.ActionEnum.has_value(action):
                return False
    except:
        return False

    return True


def is_action_parameters_valid(action_parameters):
    if not isinstance(action_parameters, list):
        return False

    try:
        for action_parameter in action_parameters:
            if not isinstance(action_parameter, str):
                return False
    except:
        return False

    return True


def is_action_formats_valid(action_formats):
    if not isinstance(action_formats, list):
        return False

    try:
        for action_format in action_formats:
            if not isinstance(action_format, int):
                return False

            if not enums.ActionFormatEnum.has_value(action_format):
                return False
    except:
        return False

    return True


def is_action_descriptions_valid(action_descriptions):
    if not isinstance(action_descriptions, list):
        return False

    try:
        for action_description in action_descriptions:
            if not isinstance(action_description, str):
                return False
    except:
        return False

    return True


def is_action_bodys_valid(action_bodys):
    if not isinstance(action_bodys, list):
        return False

    try:
        for action_body in action_bodys:
            if not isinstance(action_body, str):
                return False
    except:
        return False

    return True


def is_action_triggers_valid(action_triggers):
    if not isinstance(action_triggers, list):
        return False

    try:
        for action_trigger in action_triggers:
            if not isinstance(action_trigger, int):
                return False

            if not enums.ActionTriggerEnum.has_value(action_trigger):
                return False
    except:
        return False

    return True

def is_accessibility_valid(accessibility):
    try:
        if not isinstance(accessibility, int):
            return False

        return enums.AccessibilityEnum.has_value(accessibility)
    except:
        return False


def is_area_valid(area):
    return isinstance(area, str)


def is_geolocation_valid(geolocation):
    try:
        if not geolocation.isdigit():
            return False

        return len(geolocation) == 42
    except:
        return False
