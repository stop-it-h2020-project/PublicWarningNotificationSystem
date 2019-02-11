import logging
import json


import cerberus

from configurelogging import execution_time_logger


logger = logging.getLogger("subsystem")

schema = {'nodeModel': {'type': 'string'},
          'commMetaData':
              {'type': 'dict',
               'schema': {
                   'networkId': {'type': 'string'},
                   'macAddress': {'type': 'integer'},
                   'receivedTimestamp': {'type': 'string'},
                   'frequencyHertz': {'type': 'float'},
                   'snr': {'type': 'integer'},
                   'sequenceCounter': {'type': 'list'},
                   'gatewayId': {'type': 'integer'},
                   'rssi': {'type': 'integer'},
                   'type': {'type': 'string'},
                   'sf': {'type': 'integer'},
                   'macType': {'type': 'string'},
                   },
               },
          'nodeId': {'type': 'integer', 'required': True},
          'readings': {'type': 'list', 'items':
              [{'type': 'dict', 'schema': {'axisOne': {'type': 'integer', 'required': True},
                                           'axisTwo': {'type': 'integer', 'required': True},
                                           'temperature': {'type': 'float', 'required': True}}}]},
          'readTimestamp': {'type': 'string', 'required': True},
          'type': {'type': 'string'}}

v = cerberus.Validator(schema)


@execution_time_logger(log_name="subsystem.get_data", level="INFO")
def get_data(in_data, timestamp):
    val = v.validate(in_data)
    out_data = {"loadsensing_tiltmeter_id": {},
                "date": {},
                "sequenceCounter": {"value": None, "time": None},
                "rssi": {"value": None, "time": None},
                "gatewayId": {"value": None, "time": None},
                "sf": {"value": None, "time": None},
                "axis_one": {"value": None, "time": None},
                "axis_two": {"value": None, "time": None},
                "temperature": {"value": None, "time": None},
                "coordinates": {"type": "Point", "coordinates": None}
                }
    if val:
        out_data["loadsensing_tiltmeter_id"]["value"] = str(in_data["nodeId"])
        out_data["sequenceCounter"]["value"] = in_data["commMetaData"]["sequenceCounter"][0]    # Sequence counter is list of 1 item always
        out_data["rssi"]["value"] = in_data["commMetaData"]["rssi"]
        out_data["gatewayId"]["value"] = in_data["commMetaData"]["gatewayId"]
        out_data["sf"]["value"] = in_data["commMetaData"]["sf"]

        out_data["axis_one"]["value"] = in_data["readings"][0]["axisOne"] / 1e6
        out_data["axis_two"]["value"] = in_data["readings"][0]["axisTwo"] / 1e6
        out_data["temperature"]["value"] = in_data["readings"][0]["temperature"] / 10

        # timestamp = datetime.datetime.strptime(in_data["readTimestamp"], "%Y-%m-%dT%H:%M:%SZ")

        # If packet has a timestamp older than 10 years, set it the current time
        # This tipically happens with nodes that have been turned off and without batteries, which loose the datetime
        # info and send packets with year=1970
        # if datetime.datetime.now() > timestamp + datetime.timedelta(days=(365 * 10)):
        #     timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%SZ")

        out_data["date"]["value"] = timestamp

        out_data["sequenceCounter"]["time"] = timestamp
        out_data["rssi"]["time"] = timestamp
        out_data["gatewayId"]["time"] = timestamp
        out_data["sf"]["time"] = timestamp

        out_data["axis_one"]["time"] = timestamp
        out_data["axis_two"]["time"] = timestamp
        out_data["temperature"]["time"] = timestamp

        return out_data
    else:
        logging.error("Input data from Tiltmeter wrong format: " + json.dumps(v.errors))
        return None
