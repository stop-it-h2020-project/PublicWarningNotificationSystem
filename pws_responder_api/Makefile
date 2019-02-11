DOCKER_NAME=worldsensing/pws_responder_api
VERSION=1.0.3
NAME=pws_responder_api
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')
DOCKER_VOLUME=$(shell pwd)
DOCKER_VOLUME_REPORTS=$(shell pwd)/reports

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	@cp ~/.netrc .
	docker build -t $(DOCKER_NAME_FULL) .
	@rm .netrc

run: build
	docker run -it -p 5001:5000 \
	    --add-host mbrabbitmq:$(DOCKER_LOCALHOST) \
	    --name $(NAME) \
	    --env-file ENV/api.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i -p 5001:5000 \
	    --add-host mbrabbitmq:$(DOCKER_LOCALHOST) \
	    --name $(NAME) \
	    -v $(DOCKER_VOLUME_REPORTS):/opt/$(NAME)/reports \
	    --env-file ENV/test.env --rm $(DOCKER_NAME_FULL) "/opt/$(NAME)/scripts/run_tests"

run-swagger: build
	docker run -it -p 5001:5000 --name $(NAME) \
	    --link swaggerapi_swagger_1:swagger \
	    --net swaggerapi_swaggerapi \
	    --env-file ENV/api.env --rm $(DOCKER_NAME_FULL)

publish: build
	docker push $(DOCKER_NAME_FULL)

setup:
	docker-compose -f docker-compose.yml up -d

setup-swagger:
	@sh scripts/run_swagger.sh
	docker-compose -f docker-compose.swagger.yml -p swaggerapi up -d --force-recreate

setup-unittests:
	docker-compose -f docker-compose.unittest.yml -p unittests up -d

sonar-preview:
	sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	sonar-runner -Dsonar.issuesReport.html.enable=true
