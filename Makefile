# Updated to use buildx for amd64 only — tensorflow has no linux/arm64 wheels
# edit .env if you want to push to your own dockerhub account
-include .env

IMAGE_NAME = decimer_api
DOCKER_USER ?= docminus
REGISTRY ?= docker.io
IMAGE_REF := $(REGISTRY)/$(DOCKER_USER)/$(IMAGE_NAME)
PLATFORM ?= linux/amd64
VERSION ?=

.PHONY: all build buildx tag push publish check-version freeze-latest release

all: buildx

publish: buildx tag push

check-version:
	@if [ -z "$(VERSION)" ]; then \
		echo "ERROR: VERSION is required (example: make release VERSION=0.3.1)"; \
		exit 1; \
	fi

build:
	@echo "\n------------------------------------"
	@echo "WARNING: 'make build' is deprecated. Use 'make buildx' instead."
	@echo "Building the image $(IMAGE_NAME):"
	docker build -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

buildx:
	@echo "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker buildx build --platform linux/amd64 -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

tag:
	@echo "\n------------------------------------"
	@echo "Tagging the image $(IMAGE_NAME):"
	docker tag $(IMAGE_NAME) $(IMAGE_REF):latest
	@echo "------------------------------------\n"

push:
	@echo "\n------------------------------------"
	@echo "Pushing the image $(IMAGE_NAME):"
	docker push $(IMAGE_REF):latest
	@echo "------------------------------------\n"

freeze-latest: check-version
	@echo "\n------------------------------------"
	@echo "Freezing current latest as $(VERSION):"
	docker buildx imagetools create --tag $(IMAGE_REF):$(VERSION) $(IMAGE_REF):latest
	@echo "------------------------------------\n"

release: check-version
	@echo "\n------------------------------------"
	@echo "Building and pushing $(VERSION) and latest:"
	docker buildx build --platform $(PLATFORM) -t $(IMAGE_REF):$(VERSION) -t $(IMAGE_REF):latest --push .
	@echo "------------------------------------\n"
