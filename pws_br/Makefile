DOCKER_NAME=worldsensing/mb_business_rules_engine
VERSION=1.0.3
NAME=mb_business_rules_engine
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell /sbin/ifconfig docker0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $$1}')
DOCKER_VOLUME=$(shell pwd)
DOCKER_VOLUME_REPORTS=$(shell pwd)/reports

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	docker build -t $(DOCKER_NAME_FULL) .

run: build
	docker run -it -p 9092:9092 \
			--add-host mbrabbitmq:$(DOCKER_LOCALHOST) --add-host mbinfluxdb:$(DOCKER_LOCALHOST) \
	    --name $(NAME) \
	    --env-file ENV/kapacitor.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i -p 9092:9092 \
	    --name $(NAME) \
	    --env-file ENV/kapacitor.env --rm $(DOCKER_NAME_FULL) \
	    /bin/sh -c "cd /opt/mb_bre/ && export PYTHONPATH=/opt/mb_bre && python -m pytest"

publish: build
	docker push $(DOCKER_NAME_FULL)

sonar-preview:
	sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	sonar-runner -Dsonar.issuesReport.html.enable=true
