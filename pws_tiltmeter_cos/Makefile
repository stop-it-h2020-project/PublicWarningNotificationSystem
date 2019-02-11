DOCKER_NAME=worldsensing/mbc_pws_sensor_cos
VERSION=`python -c "from mbc_pws_sensor_cos import __version__; print(__version__)"`
CONNECTOR_CONTAINER_NAME=mbc_pws_sensor_cos
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)
DOCKER_LOCALHOST=$(shell ip addr show docker0 | grep -Po 'inet \K[\d.]+')

show_version:
	@echo $(VERSION)

show_config:
	@cat customization/ENV/$(CONTAINER_NAME).env

clean:
	@find . -iname "*~" | xargs rm 2>/dev/null || true
	@find . -iname "*.pyc" | xargs rm 2>/dev/null || true
	@find . -iname "build" | xargs rm -rf 2>/dev/null || true

minify: clean
	@mkdir -p build/minified && pyminifier --obfuscate --destdir=build/minified/ **/*.py

build: clean
	@cp ~/.netrc .
	@docker build -t $(DOCKER_NAME_FULL) .
	@rm .netrc

build-minified: minify
	@cp Dockerfile requirements/common.txt requirements/dev.txt build/
	docker build -t $(DOCKER_NAME_FULL) build/

run: build
	@docker run -it -p 5050:5050 --name $(CONNECTOR_CONTAINER_NAME) \
	--add-host mbcustomobjects_service_rest:$(DOCKER_LOCALHOST) \
	--env-file customization/ENV/mbc_pws_sensor_cos.env --rm $(DOCKER_NAME_FULL) "/opt/mb/scripts/run"

run-test: build
	@docker run -i -p 5050:5050 --name $(CONNECTOR_CONTAINER_NAME) \
	--add-host mbcustomobjects_service_rest:$(DOCKER_LOCALHOST) \
	--net pwssensorcos_test_default \
	--env-file customization/ENV/mbc_pws_sensor_cos.test.env --rm $(DOCKER_NAME_FULL) "/opt/mb/scripts/run_tests"

setup:
	@docker-compose -f docker-compose.yml up -d
	@docker-compose -f docker-compose.yml restart mbcustomobjects_service_core mbcustomobjects_service_rest

setup-test:
	@docker-compose -f docker-compose.unittest.yml up -d restart mbcustomobjects_service_core mbcustomobjects_service_rest

publish: build
	@docker push $(DOCKER_NAME_FULL)

publish-minified: build-minified
	@docker push $(DOCKER_NAME_FULL)

tag_confirmation:
	@read -p "Are you sure to continue to create a tag (y/n)?" choice;\
		case "$$choice" in\
		y|Y ) echo "yes";;\
		n|N ) exit 1;;\
		* ) exit 1;;\
		esac

tag: tag_confirmation
	@git tag $(VERSION)

tag_publish:
	@git push origin --tags
