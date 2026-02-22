# Updated to use buildx for multi-arch support
# Copy .env.example to .env and set your DOCKER_USER there (never committed to git)
-include .env

IMAGE_NAME = decimer_api

# Set DOCKER_USER before pushing, e.g.:
#   export DOCKER_USER=yourname
#   make push
# or inline:
#   make push DOCKER_USER=yourname
DOCKER_USER ?=

.PHONY: all build buildx tag push publish check-docker-user

all: buildx

publish: buildx tag push

check-docker-user:
	@if [ -z "$(DOCKER_USER)" ]; then \
		echo "ERROR: DOCKER_USER is not set. Run: make push DOCKER_USER=yourname! NOTE: Optional, only required for dockerhub pushing."; \
		exit 1; \
	fi

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

tag: check-docker-user
	@echo "\n------------------------------------"
	@echo "Tagging the image $(IMAGE_NAME):"
	docker tag $(IMAGE_NAME) docker.io/$(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"

push: check-docker-user
	@echo "\n------------------------------------"
	@echo "Pushing the image $(IMAGE_NAME):"
	docker push docker.io/$(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"
