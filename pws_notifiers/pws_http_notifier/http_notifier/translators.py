import json
import time
from xml.etree import ElementTree as ET

from pws_common.enums import ActionFormatEnum

from utils import prettify


def __get_date():
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    date = str(time.strftime(DATE_FORMAT, time.localtime()))

    TIMEZONE_FORMAT = "%z"
    timezone = str(time.strftime(TIMEZONE_FORMAT, time.localtime()))
    timezone = f"{timezone[:3]}:{timezone[3:]}"

    return f"{date}{timezone}"


def cap_action_position(action_format):
    for pos in range(0, len(action_format)):
        if ActionFormatEnum.CAP == action_format[pos]:
            return pos
    return -1


def __str_to_cap(message):
    alert = json.loads(message)[0]
    response_plan = json.loads(message)[1]

    rp_action_number = cap_action_position(response_plan["action_format"])

    alert_root = ET.Element("alert", attrib={"xmlns": "urn:oasis:names:tc:emergency:cap:1.2"})

    ET.SubElement(alert_root, "identifier").text = str(alert["id"])
    ET.SubElement(alert_root, "sender").text = "_test@worldsensing.com"
    ET.SubElement(alert_root, "sent").text = __get_date()
    ET.SubElement(alert_root, "status").text = "_Actual"
    ET.SubElement(alert_root, "msgType").text = "_Alert"
    ET.SubElement(alert_root, "scope").text = "_Public"
    info = ET.SubElement(alert_root, "info")
    ET.SubElement(info, "category").text = str(alert["type"])
    ET.SubElement(info, "event").text = response_plan["response_plan_id"]
    ET.SubElement(info, "urgency").text = "_Immediate"
    ET.SubElement(info, "severity").text = str(alert["severity"])
    ET.SubElement(info, "certainty").text = "_Likely"
    ET.SubElement(info, "senderName").text = "_Worldsensing Public Warning System"
    ET.SubElement(info, "headline").text = f"Warning {alert['title']}"
    ET.SubElement(info,
                  "description").text = f"{alert['description']}. {response_plan['action_body'][rp_action_number]}"
    area = ET.SubElement(info, "area")
    ET.SubElement(area, "areaDesc").text = response_plan['area']

    # Just for testing in local environment
    # file = open("../tests/filename.xml", "wb")
    # file.write(prettify(alert_root))

    return ET.tostring(alert_root, encoding="utf-8", method="xml")


def str_to_format(message, format):
    if format == ActionFormatEnum.PLAIN_TEXT.value:
        return message.__str__()
    elif format == ActionFormatEnum.CAP.value:
        return __str_to_cap(message)
    elif format == ActionFormatEnum.OTHER.value:
        return message.__str__()
