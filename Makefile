DOCKER_REPO := clocme/clocme

build:
	docker build -t $(DOCKER_REPO):local .

tag-latest:
	docker tag $(DOCKER_REPO):local $(DOCKER_REPO):latest
