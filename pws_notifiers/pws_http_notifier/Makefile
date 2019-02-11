NAME=pws_http_notifier
DOCKER_NAME=worldsensing/$(NAME)
VERSION=1.0.2-RC1
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')
DOCKER_VOLUME=$(shell pwd)
DOCKER_VOLUME_REPORTS=$(shell pwd)/reports

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

run: build
	docker run -it \
	    --add-host mbrabbitmq:$(DOCKER_LOCALHOST) \
	    --name $(NAME) \
	    --env-file ENV/http_notifier.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i \
	    -v $(DOCKER_VOLUME_REPORTS):/opt/pws_http_notifier/reports \
	    --name $(NAME) \
	    --env-file ENV/test.env --rm $(DOCKER_NAME_FULL) "/opt/$(NAME)/scripts/run_tests"

setup:
	docker-compose -f docker-compose.yml up -d

sonar-preview:
	@sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	@sonar-runner -Dsonar.issuesReport.html.enable=true
