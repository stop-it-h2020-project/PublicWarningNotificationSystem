CONNECTOR_NAME=email_notifier
DOCKER_NAME=worldsensing/pws_${CONNECTOR_NAME}
VERSION=1.0.0
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')
DOCKER_VOLUME=$(shell pwd)
DOCKER_VOLUME_REPORTS=$(shell pwd)/reports

TEST_CMD=/opt/pws_email_notifier/scripts/run_tests

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true
	@find . -iname "*.log" | xargs rm -rf 2>/dev/null || true

build: clean
	@cp ~/.netrc .
	docker build -t $(DOCKER_NAME_FULL) .
	@rm .netrc

publish: build
	@docker push $(DOCKER_NAME_FULL)

stop:
	docker kill unittests_pws_email_notifier_1 || true
	docker kill unittests_rabbitmq_1 || true

run: build
	docker run -it --add-host mbrabbitmq:$(DOCKER_LOCALHOST) --name pws_${CONNECTOR_NAME} \
		--env-file ENV/email_notifier.env --rm $(DOCKER_NAME_FULL) $(CMD)

run-unittests: stop build setup-unittests
	docker run -i -p 15000:15000 --name pws_${CONNECTOR_NAME} \
		-v $(DOCKER_VOLUME_REPORTS):/opt/pws_email_notifier/reports \
		--link unittests_rabbitmq_1:mbrabbitmq --net unittests_unittests \
		--net unittests_default \
		--env-file tests/test.env --rm $(DOCKER_NAME_FULL) $(TEST_CMD)

setup-unittests:
	docker-compose -f docker-compose.unittest.yml -p unittests up -d

sonar-preview:
	@sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	@sonar-runner -Dsonar.issuesReport.html.enable=true

setuptest:
	@docker-compose -f docker-compose.unittest.yml -p unittests up -d
