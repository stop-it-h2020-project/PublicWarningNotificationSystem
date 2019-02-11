pws_sensor
=============================

Standards
---------

This repository follows this general standards:
- [Semantic versioning 2.0.0](https://semver.com)
- [Keep a changelog](https://keepachangelog.com/en/1.0.0/)
- [PEP-8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Sytle Guide](https://google.github.io/styleguide/pyguide.html) and [Google-style docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

Moreover, specific choices are detailed in Worldsensing Software Guides.


Intro
-----

This is a connector for Loadsensing's Tiltmeter sensor that injects the measurements into a database.

Behaviour
---------

It expects POSTs from the LoRa gateway containing the the sensor's data in JSON format.
The sensor's format is validated against the following Cerberus schema:
```
schema = {
    "nodeModel":{
        "type":"string"
    },
    "commMetaData":{
        "type":"dict",
        "schema":{
            "networkId":{
                "type":"string"
            },
            "macAddress":{
                "type":"integer"
            },
            "receivedTimestamp":{
                "type":"string"
            },
            "frequencyHertz":{
                "type":"float"
            },
            "snr":{
                "type":"integer"
            },
            "sequenceCounter":{
                "type":"list"
            },
            "gatewayId":{
                "type":"integer"
            },
            "rssi":{
                "type":"integer"
            },
            "type":{
                "type":"string"
            },
            "sf":{
                "type":"integer"
            },
            "macType":{
                "type":"string"
            }
        }
    },
    "nodeId":{
        "type":"integer",
        "required":"True"
    },
    "readings":{
        "type":"list",
        "Items":[
            {
                "type":"dict",
                "schema":{
                    "axisOne":{
                        "type":"integer",
                        "required":"True"
                    },
                    "axisTwo":{
                        "type":"integer",
                        "required":"True"
                    },
                    "temperature":{
                        "type":"float",
                        "required":"True"
                    }
                }
            }
        ]
    }
}

```

Development
----------

A simulator has been included sensing random data in `scripts/simulator.py`


### Testing

Run `make run-test` to execute the tests.

