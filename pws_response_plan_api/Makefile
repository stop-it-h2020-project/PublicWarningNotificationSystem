NAME=pws_api_response_plan
DOCKER_NAME=worldsensing/$(NAME)
VERSION=1.1.1
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell /sbin/ifconfig docker0 | grep 'inet' | cut -d: -f2 | awk '{ print $$2}')
# DOCKER_LOCALHOST=$(shell /sbin/ifconfig docker0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $$1}')
# DOCKER_LOCALHOST=$(shell /sbin/ifconfig docker0 | grep 'Direc. inet:' | cut -d: -f2 | awk '{ print $$1}')
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
	docker run -it -p 5000:5000 \
	    --add-host mbpostgres:$(DOCKER_LOCALHOST) \
	    --name $(NAME) \
	    --env-file ENV/api.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i -p 15000:15000 --name $(NAME) \
		-v $(DOCKER_VOLUME_REPORTS):/opt/$(NAME)/reports \
		--link unittests_mbpostgres_1:mbpostgres --net unittests_unittests \
		--env-file ENV/test.env --rm $(DOCKER_NAME_FULL) "/opt/$(NAME)/scripts/run_tests"

run-swagger: build
	docker run -it -p 5000:5000 --name $(NAME) \
	    --add-host mbpostgres:$(DOCKER_LOCALHOST) \
	    --add-host swagger:$(DOCKER_LOCALHOST) \
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
