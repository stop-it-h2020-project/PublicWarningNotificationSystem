Business Rules Engine
=====================


## Table of contents

[TOC]

## Introduction

This services allows to create business rules using tick scripts in kapacitor and influxDB.
When the rule is triggered then the service sends the alert definition to Alert processor using
QueueSender.

## Development Notes

### Configuration parameters

```bash
export KAPACITOR_HOSTNAME=mb_bre
export KAPACITOR_INFLUXDB_0_URLS_0=http://mbinfluxdb:8086

```


### Docker compose

```yaml
mbbusiness_rules_engine:
  image: worldsensing/mb_business_rules_engine:1.0.0-RC1
  env_file:
    - kapacitor.env
  links:
    - mbinfluxdb
    - mbrabbitmq
  ports:
    - "9092:9092" # For debugging using httpOut kapacitor nodes
  networks:
    - private
  restart: always
```

### Run locally

#### With docker-compose

```bash
$ docker-compose -p mb up -d
$ docker exec -it mb_mbbusiness_rules_engine_1
$ kapacitor show alerts_tiltemeter
$ kapacitor watch alerts_tiltemeter
```

#### With docker

First you need to have an influxdb and rabbitmq instances up, using for example the
docker-compose.yml in this repo.

```bash
$ make run
```

### Testing

#### With docker:

```bash
$ make run-unittests
```

#### Without docker:

1. Install Python dependencies:
~~~bash
pip install -r requirements/dev.txt
~~~

2. Run tests:
~~~bash
pytest
~~~

### Implementation

This service is implemented in python 2.7. This affects pytest: python2.7 -m pytest.

_Recommendation_: for local use and testing use a Python's Virtual Environment.
