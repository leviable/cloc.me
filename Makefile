SHELL := /bin/bash

DOCKER_REPO := clocme/clocme
DOCKER_REPO_CI := clocme/clocme-ci
GIT_HASH = $(shell git rev-parse --short HEAD)
GIT_TAG = $(shell git describe --tags --exact-match $(GIT_HASH) 2>/dev/null)

.PHONY: build
build:
	docker build -t $(DOCKER_REPO):local .

.PHONY: test
test: test-lint test-unit test-functional

.PHONY: test-lint
test-lint:
	docker run --rm -it \
		--entrypoint ash \
		$(DOCKER_REPO):local \
		-c ' \
			set -e; \
			pip install tox; \
			tox -e lint; \
		'

.PHONY: test-unit
test-unit:
	docker run --rm -it \
		--env-file <(env | grep -e "^CI") \
		--entrypoint ash \
		$(DOCKER_REPO):local \
		-c ' \
			set -e; \
			pip install tox; \
			tox -e unit; \
			if [ -n "$$CIRCLE_SHA1" ]; \
				then pip install codecov && codecov --commit=$$CIRCLE_SHA1; \
			fi \
		'

.PHONY: test-functional
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

.PHONY: tag-latest
tag-latest:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO):latest

.PHONY: tag-git-tag
tag-git-tag:
	docker tag $(DOCKER_REPO):$(GIT_HASH) $(DOCKER_REPO):$(GIT_TAG)

.PHONY: push-latest
push-latest:
	docker push $(DOCKER_REPO):latest

.PHONY: pull-latest
pull-latest:
	docker pull $(DOCKER_REPO):latest

.PHONY: tag-latest-as-local
tag-latest-as-local:
	docker tag $(DOCKER_REPO):latest $(DOCKER_REPO):local

.PHONY: push-tagged
push-tagged:
	docker push $(DOCKER_REPO):$(GIT_TAG)

.PHONY: push-ci
push-ci:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO_CI):$(GIT_HASH)
	docker push $(DOCKER_REPO_CI):$(GIT_HASH)

.PHONY: pull-ci
pull-ci:
	docker pull $(DOCKER_REPO_CI):$(GIT_HASH)
	docker tag $(DOCKER_REPO_CI):$(GIT_HASH) $(DOCKER_REPO):$(GIT_HASH)
	docker tag $(DOCKER_REPO_CI):$(GIT_HASH) $(DOCKER_REPO):local
