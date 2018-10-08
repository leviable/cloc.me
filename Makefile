DOCKER_REPO := clocme/clocme
DOCKER_REPO_CI := clocme/clocme-ci
GIT_HASH = $(shell git rev-parse --short HEAD)

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
	docker run --rm -it \
		-w /clocme \
		-v `pwd`:/clocme \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e IMAGE_NAME=$(DOCKER_REPO):local \
		python:alpine \
		ash -c ' \
			set -e; \
			pip install tox; \
			tox -e functional \
		'

tag-latest:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO):latest

push-latest:
	docker push $(DOCKER_REPO):latest

push-ci:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO_CI):$(GIT_HASH)
	docker push $(DOCKER_REPO_CI):$(GIT_HASH)

pull-ci:
	docker pull $(DOCKER_REPO_CI):$(GIT_HASH)
	docker tag $(DOCKER_REPO_CI):$(GIT_HASH) $(DOCKER_REPO):local
