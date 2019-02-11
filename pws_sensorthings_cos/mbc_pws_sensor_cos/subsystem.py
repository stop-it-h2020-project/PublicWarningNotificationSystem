import os
import logging
import json
import copy

import jinja2
import requests
import datetime
from dateutil import tz

from configurelogging import execution_time_logger


logger = logging.getLogger("subsystem")

out_data_schema_template = {"date": {}}


DS = "Datastream@iot.navigationLink"
MS = "MultiDatastream@iot.navigationLink"


def schema_to_dict(schema):
    dict_out = copy.deepcopy(out_data_schema_template)
    dict_in = json.load(open(schema))
    for key in dict_in["properties"]:
        if dict_in["properties"][key]["$ref"] == "#/timeseries":
            dict_out[key] = {"value": None, "time": None}

    return dict_out


def valid_type(data):
    """
    >>> valid_type(0.1)
    True
    >>> valid_type(1)
    True
    >>> valid_type("hola")
    False
    >>> valid_type([1, 2])
    False
    """

    return type(data) in [int, float]


def get_most_recent_timestamp(pws_cos_api):
    response = requests.get(pws_cos_api)
    data = json.loads(response.content)["data"]
    if not data:
        return None
    else:
        timestamp = data.get("updated_at")
        if not timestamp:
            timestamp = data.get("created_at")
            if not timestamp:
                raise NameError("Key [created_at] not found in COS response to /instances/last")
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=tz.tzlocal())


@execution_time_logger(log_name="subsystem.query_frost", level="INFO")
def query_frost(frost_url, frost_port, last_t):

    query = "http://{}:{}/FROST-Server/v1.0/Observations".format(frost_url, frost_port)
    if last_t is not None:
        # TODO: rename web to frost (somehow it doesn0t work, although the container's name in compose is frost)
        last_t_str = datetime.datetime.isoformat(last_t).replace("+00:00", "Z")
        if "+00:00" in last_t_str:
            last_t_str = last_t_str.replace("+00:00", "Z")
        # e.g: ?$filter=phenomenonTime%20gt%202018-10-10T07:00:00Z
        query = query + "?$filter=phenomenonTime gt {}".format(last_t_str)

    responses = requests.get(query)

    return responses


@execution_time_logger(log_name="subsystem.generate_schema", level="INFO")
def generate_schema(data, cos_config, sensor_id):

    out_timeseries_schema = []

    # TODO: consider using the observation's Datastream/Multidatastream instead of detecting data type from data itself
    if isinstance(data, list):
        if sensor_id == "_ds_":
            logging.error("Multistream data received, Datastream expected")
            return None
        for idx, elem in enumerate(data):
            if valid_type(elem):
                out_timeseries_schema.append("value_{}".format(idx))
            else:
                logging.error("Input data contains value [{}] of unknown type. "
                              "Supported: [float, int, str]".format(elem))
                return None
    else:
        if sensor_id == "_ms_":
            logging.error("Datastreamdata received, Multistream  expected")
            return None
        if valid_type(data):
            out_timeseries_schema.append("value_0")
        else:
            return None

    template = os.path.join(cos_config["schema_dir"], "schema_template.json")
    jinja_template = jinja2.Template(open(template).read())

    rendered_template = jinja_template.render(timeseries=out_timeseries_schema)

    schema_filename = os.path.join(cos_config["schema_dir"], "schema_{}.json".format(sensor_id))
    with open(schema_filename, "w+") as f:
        f.write(rendered_template)

    return schema_filename


@execution_time_logger(log_name="subsystem.get_data", level="INFO")
def format_data(data, epoch, schema, cos_config):

    dicti_schema = schema_to_dict(schema)
    supported_keys = dicti_schema.keys()

    dicti = copy.deepcopy(out_data_schema_template)

    dicti["sensorthing_id"] = {"value": cos_config["object_type"]}
    dicti["date"]["value"] = epoch

    if isinstance(data, list):
        for idx, elem in enumerate(data):
            key = "value_{}".format(idx)
            if key not in dicti_schema:
                logging.error("Got {} not present in {}".format(key, supported_keys))
                continue
            dicti[key] = {"value": elem, "time": epoch}
    else:
        dicti["value_0"] = {"value": data, "time": epoch}

    return dicti


@execution_time_logger(log_name="subsystem.get_sensor_id", level="INFO")
def get_sensor_id(response):

    stream = DS if DS in response else MS

    data_stream = requests.get(response[stream])
    sensor_id = json.loads(data_stream.content).get("@iot.id", None)

    # TODO: ensure if both data- and multi-streams can't be present
    sensor_id = "_ds_" + str(sensor_id) if DS in response else "_ms_" + str(sensor_id)

    return sensor_id


if __name__ == "__main__":
    import doctest

    doctest.testmod()
