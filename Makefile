DOCKER_REPO := clocme/clocme

build:
	docker build -t $(DOCKER_REPO):local .

test: test-lint test-unit test-functional

test-lint:
	docker run --rm -it \
		--entrypoint tox \
		$(DOCKER_REPO):local \
		-e lint

test-unit:
	docker run --rm -it \
		--entrypoint tox \
		$(DOCKER_REPO):local \
		-e unit

test-functional:
	# docker run --rm -it \
	# 	--entrypoint tox \
	# 	$(DOCKER_REPO):local \
	# 	-e functional
	IMAGE_NAME=$(DOCKER_REPO):local tox -e functional

tag-latest:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO):latest

push:
	docker push $(DOCKER_REPO):latest
