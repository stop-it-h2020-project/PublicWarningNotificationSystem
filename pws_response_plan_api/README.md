## API Response Plan

See the [Swagger - OpenAPI 3.0 Documentation](https://bitbucket.org/worldsensing_traffic/pws_api/raw/develop/api_devices/swagger.yaml).

### Usage
There is a Makefile explaining the main actions of the Docker.

#### Local server
`make run` and the API will be running on `:5000`.

#### Local server + Documentation
`make run-swagger` and the API will be running on `:5000` and Swagger in `:8082`.

#### Local tests
`make run-unittests` and the API tests will be run automatically.

### Future improvements
- Add possibility to search by external ID.
- Improve parsing in POST and PUT.