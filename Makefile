# Updated to use buildx for multi-arch support
IMAGE_NAME = decimer_api
DOCKER_USER = DocMinus

.PHONY: all build buildx tag push

all: buildx tag push

build:
	@echo -e "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker build -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

buildx:
	@echo -e "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

tag: 
	@echo -e "\n------------------------------------"
	@echo "Tagging the image $(IMAGE_NAME):"
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):latest
	@echo "------------------------------------\n"

push: tag
	@echo -e "\n------------------------------------"
	@echo "Pushing the image $(IMAGE_NAME):"
	docker push $(DOCKER_USER)/$(IMAGE_NAME):latest
	@echo "------------------------------------\n"
