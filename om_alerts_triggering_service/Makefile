DOCKER_NAME=worldsensing/oms_alerts_processor_service
VERSION=1.0.2-pws
NAME=oms_alerts_processor_service
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell /sbin/ifconfig docker0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $$1}')
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
		@docker run -i \
		--add-host mbrabbitmq:$(DOCKER_LOCALHOST) \
		--add-host mbpostgres:$(DOCKER_LOCALHOST) \
		--name $(NAME) \
		--env-file ENV/deploy.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i \
		--add-host mbpostgres:$(DOCKER_LOCALHOST) \
		--name $(NAME) \
		--env-file ENV/test.env --rm $(DOCKER_NAME_FULL) "run_tests"

publish: build
	@docker push $(DOCKER_NAME_FULL)

setup:
	@docker-compose -f docker-compose.yml -p alerts_processor up -d

setup-unittests:
	@docker-compose -f docker-compose.unittest.yml -p unittests up -d

sonar-preview:
	@sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	@sonar-runner -Dsonar.issuesReport.html.enable=true
