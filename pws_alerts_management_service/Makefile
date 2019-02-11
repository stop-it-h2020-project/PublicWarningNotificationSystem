DOCKER_NAME=worldsensing/pws_alerts_management_service
VERSION=1.0.4-RC1
CONTAINER_NAME=pws_alerts_management_service
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')
DOCKER_VOLUME=$(shell pwd)
DOCKER_VOLUME_REPORTS=$(shell pwd)/reports

show_version:
	@echo $(DOCKER+NAME_FULL)

show_config:
	@more ENV/* | column -e

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

build: clean
	@cp ~/.netrc .
	docker build -t $(DOCKER_NAME_FULL) .
	@rm .netrc

run: build
	docker run -i -p 5000:5000 \
		--add-host mbpostgres:$(DOCKER_LOCALHOST) \
		--add-host mbredis:$(DOCKER_LOCALHOST) \
		--add-host pws_external_alerts_management_service:$(DOCKER_LOCALHOST) \
		--name $(CONTAINER_NAME) \
		--env-file ENV/deploy.env --rm $(DOCKER_NAME_FULL)

run-unittests: build
	docker run -i -p 5000:5000 \
		--add-host mbpostgres:$(DOCKER_LOCALHOST) \
		--add-host mbredis:$(DOCKER_LOCALHOST) \
		--add-host pws_external_alerts_management_service:$(DOCKER_LOCALHOST) \
		--name $(CONTAINER_NAME) \
		--env-file ENV/test.env --rm $(DOCKER_NAME_FULL) run_tests

publish: build
	@docker push $(DOCKER_NAME_FULL)

setup:
	@docker-compose -f docker-compose.yml -p alerts_api up -d

setup-unittests:
	@docker-compose -f docker-compose.unittest.yml -p unittests up -d

sonar-preview:
	@sonar-runner -Dsonar.analysis.mode=preview -Dsonar.issuesReport.html.enable=true

sonar-analyze:
	@sonar-runner -Dsonar.issuesReport.html.enable=true

tag_confirmation:
	@git tag
	@read -p "Are you sure to continue to create tag $(VERSION) (y/n)?" choice;\
	          case "$$choice" in\
              y|Y ) echo "...Creating tag";;\
              n|N ) echo "No tag created\n" && exit 1;;\
              * ) echo "Invalid option\n" && exit 2;;\
              esac

tag: tag_confirmation
	@git tag $(VERSION)
	@git push origin --tags
