# Tiltmeter simulator using SensorThings 

This is a simple simulator that inserts data into the PWS using the SensorThings format from OGC. The data is inserted 
periodically (period customizable via environment file). The data format follows the one that is inserted by a real
tiltmeter, every iteration 2 values are inserted, representing the tiltmeter's axis. The values follow a 
Gaussian random variable, with mean MU and standard deviation SIGMA (also customizable via .env files).

In order to insert measurements (Observations), SensorThings requires a Datastream for them to be created in advance.

Datastreams, in turn, require at least 3 entities: Things, ObserverProperties and Sensors. All of them are created here
before entering the main loop.


## Running

There is a Makefile explaining the main actions of the Docker. It can be run locally:
`make build && make run`

or its image added in a docker-compose.yml file.
