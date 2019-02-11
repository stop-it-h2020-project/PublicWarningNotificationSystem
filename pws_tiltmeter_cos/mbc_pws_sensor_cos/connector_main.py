import logging
import datetime
import pytz
import requests
import json

from flask import Flask, request

from mbconnector import mbcos
from configurelogging import ConfigureStdoutLogging, execution_time_logger
from configmanager import ConfigManager

import subsystem

import pkg_resources
tiltmeter_cos_schema = pkg_resources.resource_filename("pws_common", "tiltmeter_cos_schema.json")

logger = logging.getLogger("connector_main")

app = Flask(__name__)

cos_client = None

conf_manager = ConfigManager()
pws_cos_api = conf_manager.get_specific_configuration("pws_cos_api")


@app.route("/<nw_id>/write", methods=["POST"])
def rx_gw_data(nw_id):
    timestamp = datetime.datetime.strftime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc), "%Y-%m-%dT%H:%M:%SZ")

    token = request.args.get("auth")
    logger.info("Received data from LoRa gateway in network [" + nw_id + "] with token [" + token + "]")

    data = subsystem.get_data(request.json, timestamp)
    if data is not None:
        sensor_name = data["loadsensing_tiltmeter_id"]["value"]
        response = requests.get(f"{pws_cos_api}/sensors/loadsensing_tiltmeter/{sensor_name}")
        if response.status_code == 200:
            coordinates = json.loads(response.content)["data"]["coords"]
            data["coordinates"]["coordinates"] = coordinates
            send_data(cos_client, [data])
        else:
            logger.info(f"Sensor {sensor_name} not found. Must be onboarded before")
    return ""


def connector_loop():
    global cos_client

    mobility_config = conf_manager.get_specific_configuration("mobility").copy()
    cos_config = conf_manager.get_specific_configuration("cos")
    mobility_url = mobility_config.pop('url')
    internal_api = conf_manager.get_specific_configuration("internal_api")

    cos_client = mbcos.CosObject(cos_config['object_type'], mobility_url, **mobility_config)

    cos_client.create_object()
    cos_client.set_schema_from_file(tiltmeter_cos_schema)

    app.run(debug=True, host="0.0.0.0", port=internal_api["port"])


@execution_time_logger(log_name="connector_main.send_data", level="INFO")
def send_data(cos_client, raw_data):
    logger.info(raw_data)
    cos_client.add_data(raw_data, delete_others=False)


if __name__ == "__main__":
    log_level = ConfigManager().get_specific_configuration("log", "level")
    ConfigureStdoutLogging(level=log_level)
    connector_loop()

