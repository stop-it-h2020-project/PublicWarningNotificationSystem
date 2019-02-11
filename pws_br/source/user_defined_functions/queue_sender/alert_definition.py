import sys
import logging

logger = logging.getLogger(__name__)

class AlertDefinition(object):

    def __init__(self, options):
        self.options = options
        self.point = None

    def get_alert(self, point):
        self.point = point
        item_type = self.get_option("item_type").values[0].stringValue
        alert_definition = getattr(self, item_type, lambda: None)
        alert = alert_definition()
        if not alert:
            raise ValueError("Invalid alert definition for item_type: ", item_type)
        return alert

    def tiltmeter(self):
        axis_threshold = self.get_option("threshold").values[0].doubleValue
        period = 4  # TODO READ FROM ENVIRONMENT
        period_units = "seconds"  # TODO READ FROM ENVIRONMENT
        score_one = 0.0
        score_two = 0.0
        axis_one = self.point.fieldsDouble["axis_one"]
        axis_two = self.point.fieldsDouble["axis_two"]
        self.point.fieldsDouble["forecast_value"] = 0.0
        axis_exceeded_title = []
        axis_exceeded_value = []
        if abs(axis_one) > axis_threshold:
            score_one = abs(axis_one - axis_threshold)
            axis_exceeded_title.append("axis_one")
            axis_exceeded_value.append(str(score_one))
            self.point.fieldsDouble["absolute_value"] = axis_one
        if abs(axis_two) > axis_threshold:
            score_two = abs(axis_two - axis_threshold)
            axis_exceeded_title.append("axis_two")
            axis_exceeded_value.append(str(score_two))
            self.point.fieldsDouble["absolute_value"] = axis_two
        score = pow(score_one, 2) + pow(score_two, 2)
        self.point.fieldsDouble["score"] = score

        axis_exceeded_title = ", ".join(axis_exceeded_title)
        axis_exceeded_value = ", ".join(axis_exceeded_value)

        description = "Axis {} of tiltmeter with id {} exceeded {} degree threshold during more than {} {}".format(
                       axis_exceeded_title, self.point.fieldsString["item_id"],
                       axis_exceeded_value, period, period_units)

        return self.get_alert_definition(description)


    def get_option(self, option_name):
        return next((option for option in self.options if option.name == option_name), None)

    def get_alert_definition(self, description=""):
        created_at = self.point.time / 1000000.0
        alert = {
            "related_item": {
                "item_id": self.point.fieldsString["item_id"],
                "item_type": self.get_option("item_type").values[0].stringValue,
                "measure_name": self.get_option("measure_name").values[0].stringValue,
                "measure_unit": self.get_option("measure_unit").values[0].stringValue
            },
            "alert": {
                "score": self.point.fieldsDouble["score"],
                "absolute_value": self.point.fieldsDouble["absolute_value"],
                "forecast_value": self.point.fieldsDouble["forecast_value"],
                "severity": self.get_option("severity").values[0].intValue,
                "description": description
            },
            "rule": {
                "rule_id": self.get_option("rule_id").values[0].stringValue,
                "rule_name": self.get_option("rule_name").values[0].stringValue,
                "threshold": self.get_option("threshold").values[0].doubleValue
            },
            "timestamps": {
                "created_at": created_at
            },
            "action_stamps": {
                "created_by": "BRE"
            }
        }

        return alert
