DOCKER_NAME=worldsensing/pws_external_alerts_management_service
VERSION=1.0.4
NAME=pws_external_alerts_management_service
DOCKER_NAME_FULL=$(DOCKER_NAME):$(VERSION)

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
		--name $(NAME) \
		--env-file ENV/deploy.env --rm $(DOCKER_NAME_FULL)

publish: build
	@docker push $(DOCKER_NAME_FULL)

