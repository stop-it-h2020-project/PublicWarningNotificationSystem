
TIME = 1539769622466000000.0
DESCRIPTION = ""

THE_GEOM = "LINESTRING(-71.160281 42.258729,-71.160837 42.259113,-71.161144 42.25932)"

TILTMETER_COS_RESPONSE = {
    "custom_fields": {
        "axis_one": {
            "time": "2018-10-30T14:20:00Z",
            "type": "timeseries",
            "value": -18.146667
        },
        "axis_two": {
            "time": "2018-10-30T14:20:00Z",
            "type": "timeseries",
            "value": -0.587853
        },
        "coordinates": {
            "coordinates": [41.380858, 2.141304],
            "type": "Point"
        },
        "date": {
            "type": "date", "value": "2018-10-30T14:20:00Z"
        },
        "loadsensing_tiltmeter_id": {
            "type": "external_id",
            "value": "7292"
        },
        "temperature": {
            "time": "2018-10-30T14:20:00Z",
            "type": "timeseries",
            "value": 24.1
        }
    },
    "id": 1,
    "refs": {},
    "type": "loadsensing_tiltmeter"
}

TILTEMETER_ALERT = {
    "action_stamps": {
        "created_by": "BRE"
    },
    "alert": {
        "absolute_value": -18.14668,
        "description": "Axis axis_one of tiltmeter with id 7292 exceeded 19.14668 degree threshold during more than 4 seconds",
        "forecast_value": 0.0,
        "score": 366.5953550224,
        "severity": 1
    },
    "related_item": {
        "item_id": "7292",
        "item_type": "tiltmeter",
        "measure_name": "tilt",
        "measure_unit": "degrees"
    },
    "rule": {
        "rule_id": "RULE#TILTMETER#1",
        "rule_name": "tiltmeter rule",
        "threshold": 1.0
    },
    "timestamps": {
        "created_at": 1540907610000.0
    }
}

ENRICHED_TILTMETER_ALERT = {
    "description": "Axis axis_one of tiltmeter with id 7292 exceeded 19.14668 degree threshold during more than 4 seconds",
    "meta_type": "meta_data",
    "sub_type": "n/a",
    "absolute_value": -18.14668,
    "absolute_difference": 18.14668,
    "created_by": "BRE",
    "related_item_id": "7292",
    "related_item_type": "tiltmeter",
    "severity": 1,
    "address": "Tiltmeter empty adress",
    "the_geom": {
        "coordinates": [41.380858, 2.141304],
        "type": "Point"
    },
    "title": "Inclination threshold exceeded for tiltmeter 7292",
    "type": "Inclination exceeded threshold",
    "rule_id": "RULE#TILTMETER#1",
    "status": 10
 }


TILTEMETER_ALERT_NO_RELATED_ITEM = {
    "action_stamps": {"created_by": "BRE"},
    "alert": {"absolute_value": -18.14668,
              "description": "Axis axis_one of tiltmeter with id 7292 exceeded 9.14668 degree threshold during more than 4 seconds",
              "forecast_value": 0.0,
              "score": 366.5953550224,
              "severity": 1},
    "rule": {"rule_id": "RULE#TILTMETER#1",
             "rule_name": "tiltmeter rule",
             "threshold": 1.0},
    "timestamps": {"created_at": 1540907610000.0}
}


TILTEMETER_ALERT_NO_ITEM_TYPE = {
    "action_stamps": {"created_by": "BRE"},
    "alert": {"absolute_value": -18.14668,
              "description": "Axis axis_one of tiltmeter with id 7292 exceeded 19.14668 degree threshold during more than 4 seconds",
              "forecast_value": 0.0,
              "score": 366.5953550224,
              "severity": 1},
    "related_item": {"item_id": "7292",
                     "measure_name": "tilt",
                     "measure_unit": "degrees"},
    "rule": {"rule_id": "RULE#TILTMETER#1",
             "rule_name": "tiltmeter rule",
             "threshold": 1.0},
    "timestamps": {"created_at": 1540907610000.0}
}


TILTEMETER_ALERT_UNSUPPORTED_TYPE = {
    "action_stamps": {"created_by": "BRE"},
    "alert": {"absolute_value": -18.14668,
              "description": "Axis axis_one of tiltmeter with id 7292 exceeded 9.14668 degree threshold during more than 4 seconds",
              "forecast_value": 0.0,
              "score": 366.5953550224,
              "severity": 1},
    "related_item": {"item_id": "7292",
                     "item_type": "tamagotchi",
                     "measure_name": "tilt",
                     "measure_unit": "degrees"},
    "rule": {"rule_id": "RULE#TILTMETER#1",
             "rule_name": "tiltmeter rule",
             "threshold": 1.0},
    "timestamps": {"created_at": 1540907610000.0}
}
