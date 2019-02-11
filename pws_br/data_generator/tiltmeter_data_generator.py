from time import sleep
from datetime import datetime
import random

from influxdb import InfluxDBClient

TIME_TO_SLEEP = 20


def main(host='localhost', port=8086, dbname='measurements'):
    """Instantiate a connection to the InfluxDB."""
    client = InfluxDBClient(host=host, port=port, database=dbname)
    print("Create database: " + dbname)
    client.create_database(dbname)

    while True:
        temperature = random.normalvariate(20.0, 10.0)
        axis_one = 2.0 #random.normalvariate(0.0, 1.0)
        axis_two = 2.0 # random.normalvariate(0.0, 1.0)
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        internal_id = "0"
        loadsensing_tiltmeter_id = "1"
        object_type = "loadsensing_tiltmeter"
        json_body = [
            {
                "measurement": "tiltmeter",
                "time": current_time,
                "fields": {
                    "axis_one": float(axis_one),
                    "temperature": float(temperature)
                },
                "tags": {
                    "internal_id": internal_id,
                    "object_type": object_type,
                    "loadsensing_tiltmeter_id": loadsensing_tiltmeter_id
                },
            },
            {
                "measurement": "tiltmeter",
                "time": current_time,
                "fields": {
                    "axis_two": float(axis_two),
                    "temperature": float(temperature)
                },
                "tags": {
                    "internal_id": internal_id,
                    "object_type": object_type,
                    "loadsensing_tiltmeter_id": loadsensing_tiltmeter_id
                },
            }
        ]
        print("Write points: {0}".format(json_body))
        client.write_points(json_body)
        sleep(TIME_TO_SLEEP)


if __name__ == '__main__':
    main()
