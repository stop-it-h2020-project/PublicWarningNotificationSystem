import random
import requests
import datetime
import logging
import time

from configurelogging import ConfigureStdoutLogging
from configmanager import ConfigManager


logger = logging.getLogger("simulator")


def create_datastream(frost_base_url):
    frost_datastream_url = frost_base_url + "Datastreams"

    entity_ids = {}

    for entity in ["Things", "ObservedProperties", "Sensors"]:
        frost_entity_url = frost_base_url + entity
        with open("schemas/{}.json".format(entity), "rb") as f:
            try:
                response = requests.post(frost_entity_url,
                                         headers={"content-type": "application/json"},
                                         data=f)
                if response.status_code != 200:
                    response.raise_for_status()

                logging.info(response.request)  # TODO: add response.ok check in all
                entity_id = response.headers["location"].split("(")[1].split(")")[0]
                entity_ids[entity] = entity_id

            except Exception as e:
                logger.error("Error in create entity: %s" % e)

    # Create DataStream
    with open("schemas/tiltmeter_datastream_template.json") as f:
        template = f.read()

    new_data = (template
                .replace("{thing_id}", entity_ids["Things"])
                .replace("{observedproperty_id}", entity_ids["ObservedProperties"])
                .replace("{sensor_id}", entity_ids["Sensors"]))

    with open("schemas/tiltmeter_datastream.json", "w") as f:
        f.write(new_data)

    with open("schemas/tiltmeter_datastream.json", "rb") as f:
        response = requests.post(frost_datastream_url,
                                 headers={"content-type": "application/json"},
                                 data=f)

    logging.info(response.request)
    datastream_id = response.headers["location"].split("(")[1].split(")")[0]

    return datastream_id


def simulator_loop():
    conf_manager = ConfigManager()

    frost_config = conf_manager.get_specific_configuration("sensorthings")
    frost_url = frost_config.pop("url")
    frost_port = frost_config.pop("port")
    query_sleep = frost_config.pop("query_sleep")

    simulator_config = conf_manager.get_specific_configuration("simulator")
    mu = simulator_config.pop("mu")
    sigma = simulator_config.pop("sigma")

    frost_base_url = "http://{}:{}/FROST-Server/v1.0/".format(frost_url, frost_port)
    frost_observation_url = frost_base_url + "Observations"

    datastream_id = create_datastream(frost_base_url)

    with open("schemas/tiltmeter_observation_template.json") as f:
        template = f.read()
        template = template.replace("{datastream_id}", datastream_id)

    while True:
        axis_one = random.gauss(mu, sigma)
        axis_two = random.gauss(mu, sigma)
        dt = datetime.datetime.now()

        new_data = template.replace("{axis_one}", str(axis_one))
        new_data = new_data.replace("{axis_two}", str(axis_two))
        new_data = new_data.replace("{datetime}", dt.strftime("%Y-%m-%dT%H:%M:%SZ"))

        # TODO: find the way to prevent from having to write-read the file every iteration
        with open("schemas/tiltmeter_sensorthings.json", "w") as f:
            f.write(new_data)

        with open("schemas/tiltmeter_sensorthings.json", "rb") as f:
            response = requests.post(frost_observation_url,
                                     headers={"content-type": "application/json"},
                                     data=f)

        logging.info(response.request)

        time.sleep(query_sleep)


if __name__ == "__main__":
    log_level = ConfigManager().get_specific_configuration("log", "level")
    ConfigureStdoutLogging(level="DEBUG")
    simulator_loop()
