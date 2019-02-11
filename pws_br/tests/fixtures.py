from base_test import Point, create_option


TIME = 1539769622466000000.0
GROUP = "item_id=RC#10"
DESCRIPTION = ""
ALERT = {
}

EXPECTED_ALERT = ALERT
EXPECTED_ALERT["timestamps"]["created_at"] = TIME / 1000000.0
RULE = ALERT["rule"]
RELATED_ITEM = ALERT["related_item"]
ACTION_STAMPS = ALERT["action_stamps"]
TILTMETER_AXIS = [3.0, 4.0]


def generate_point(item_type):
    point = Point()
    ALERT["related_item"]["item_type"] = item_type
    point.fieldsDouble["score"] = ALERT["alert"]["score"]
    point.fieldsString["item_id"] = ALERT["related_item"]["item_id"]
    point.group = GROUP
    point.time = TIME
    point.tags[GROUP.split("=")[0]] = GROUP.split("=")[1]
    if item_type == 'tiltmeter':
        point.fieldsDouble["axis_one"] = TILTMETER_AXIS[0]
        point.fieldsDouble["axis_two"] = TILTMETER_AXIS[1]
        ALERT["alert"]["score"] = 13.0  # (axis_one - threshold)^2 + (axis_two - threshold)^2
        ALERT["alert"]["absolute_value"] = TILTMETER_AXIS[1]
        ALERT["alert"]["forecast_value"] = 0.0

    return point

def create_options(item_type):
    options = []
    options.append(create_option("item_type", item_type))
    options.append(create_option("measure_name", RELATED_ITEM["measure_name"]))
    options.append(create_option("measure_unit", RELATED_ITEM["measure_unit"]))
    options.append(create_option("rule_id", RULE["rule_id"]))
    options.append(create_option("rule_name", RULE["rule_name"]))
    options.append(create_option("created_by", ACTION_STAMPS["created_by"]))
    options.append(create_option("threshold", RULE["threshold"] ,type='double'))
    options.append(create_option("severity", ALERT["alert"]["severity"] ,type='int'))

    return options
