import logging
import time
import datetime
import dateutil.parser
import requests
import json
import os

from mbconnector import mbcos
from configurelogging import ConfigureStdoutLogging, execution_time_logger
from configmanager import ConfigManager

import subsystem


logger = logging.getLogger("connector_main")


def connector_loop():

    cos_client = {}

    conf_manager = ConfigManager()
    mobility_config = conf_manager.get_specific_configuration("mobility").copy()
    cos_config = conf_manager.get_specific_configuration("cos")
    frost_config = conf_manager.get_specific_configuration("sensorthings")
    mobility_url = mobility_config.pop("url")
    frost_url = frost_config.pop("url")
    frost_port = frost_config.pop("port")
    query_sleep = frost_config.pop("query_sleep")
    sensorthings_path = frost_config.pop("schema_dir")
    pws_cos_api = conf_manager.get_specific_configuration("pws_cos_api")

    last_t = subsystem.get_most_recent_timestamp(pws_cos_api)

    while True:

        time.sleep(query_sleep)     # Timer to prevent over-loading the FROST server

        responses = subsystem.query_frost(frost_url, frost_port, last_t)

        status_code = responses.status_code
        if status_code != 200:
            logger.info("Received {} status code".format(status_code))
            logger.info("Response content: {}".format(responses.content))
            continue

        responses_dict = json.loads(responses.content)

        for response in responses_dict["value"]:
            # TODO: handle phenomenonTime not present
            t = dateutil.parser.parse(response["phenomenonTime"])   # Converts from ISO 8601 timeformat
            if last_t is None or t > last_t:    # Update last_t in first occation and if newer data received
                last_t = t

            sensor_id = subsystem.get_sensor_id(response)

            data = response["result"]
            epoch = response["phenomenonTime"]

            if sensor_id not in cos_client:
                _cos_config = dict(cos_config)
                _cos_config["object_type"] = _cos_config["object_type"] + sensor_id

                schema_file = subsystem.generate_schema(data, _cos_config, sensor_id)

                cos_client[sensor_id] = mbcos.CosObject(_cos_config['object_type'], mobility_url, **mobility_config)
                cos_client[sensor_id].create_object()
                cos_client[sensor_id].set_schema_from_file(schema_file)

            else:
                schema_file = os.path.join(sensorthings_path, "schema_{}.json".format(sensor_id))

            formatted_data = subsystem.format_data(data, epoch, schema_file, _cos_config)
            send_data(cos_client[sensor_id], [formatted_data])


@execution_time_logger(log_name="connector_main.send_data", level="INFO")
def send_data(cos_client, raw_data):
    logger.info(raw_data)
    cos_client.add_data(raw_data, delete_others=False)


if __name__ == "__main__":
    log_level = ConfigManager().get_specific_configuration("log", "level")
    ConfigureStdoutLogging(level=log_level)
    connector_loop()

