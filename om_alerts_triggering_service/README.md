# Alerts Processor

This component consumes alerts coming from third parties or from OneMind Business Rules Engine, through a message queue. 
Then, it adds metadata for tiltmeter alerts. After the alert is "enriched" then this component posts the rule and the alert to the alerts API.

## Usage

There is a Makefile explaining the main actions of the Docker.

## Running

### Docker
`make run` and the RabbitMQ queue will be setup on port `:5672` and a
Postgres database on port `:5432`. A browsable interface of the queue
can be seen on port `:15672`.

### Locally

Assuming the dockers are launched, from the project folder use
~~~bash
python oms_alerts_processor_service/main.py
~~~

## Testing

Testing needs launching docker containers with _docker-compose.unittests.yml_
before running. use `make setup-unittests`.

Use _pytest_ locally or `make run-unittests` for docker and the tests
will be run automatically.
