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

This is a connector for Sensor Things that injects the measurements into a database.

Behaviour
---------

It comes with a FROST server (see https://github.com/FraunhoferIOSB/FROST-Server/wiki), which is a SensorThings 
server implementation by the Fraunhofer Institute. 

The FROST server accepts requests using the OGC protocol, which is a standard for IoT 
(see http://docs.opengeospatial.org/is/15-078r6/15-078r6.html).
An example of a request can be found in examples/demoEntities.json.

This connector queries periodically the FROST server for new data and sends it to COS.

Supported data types are numbers (integers, doubles, ...) and lists of numbers. More complex data can't be handled
at the moment.


### Testing

Run `make run-test` to execute the tests.

