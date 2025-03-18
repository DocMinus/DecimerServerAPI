# Updated to use buildx for multi-arch support
IMAGE_NAME = decimer_api
DOCKER_USER = docminus

.PHONY: all build buildx tag tagpush push

all: buildx tagpush push

build:
	@echo "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker build -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

buildx:
	@echo "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

tag:
	@echo "\n------------------------------------"
	@echo "Tagging the image $(IMAGE_NAME):"
	docker push $(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"

tagpush:
	@echo "\n------------------------------------"
	@echo "Tagging the image $(IMAGE_NAME):"
	docker tag $(IMAGE_NAME) docker.io/$(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"

push:
	@echo "\n------------------------------------"
	@echo "Pushing the image $(IMAGE_NAME):"
	docker push docker.io/$(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"
