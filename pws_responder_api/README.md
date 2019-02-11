## Responder API

This API is an intermediate layer between the Alerts and Response Plans APIs and the execution of such Response Plans.
When running the PWS with a Front End, this API will be called from the "Alerts" tab after the operator has selecte an
Alert, a Response Plan for it and the parameters to customize it. In the case there is no Front End, the API will be 
called when a given alert has been validated with the corresponding Automatic Response Plan for it.

### Usage
There is a Makefile explaining the main actions of the Docker. 

The file pws_responder_api.postman_collection.json can also be used to test some example queries against the API if it
is run locally.

#### Local server
`make setup && make run` and the API will be running on `:5001`.

#### Local server + Documentation
`make setup-swagger && make run-swagger` and the API will be running on `:5001` and Swagger in `:8082`.

#### Local tests
`make setup-unittests && make run-unittests` and the API tests will be run automatically.