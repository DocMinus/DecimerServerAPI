# Makefile
IMAGE_NAME = decimer_api

.PHONY: all build 

all: build 

build:
	@echo -e "\n------------------------------------"
	@echo "Building the image $(IMAGE_NAME):"
	docker build -t $(IMAGE_NAME) .
	@echo "------------------------------------\n"
	@echo "Use 'docker-compose up -d' to start the container"

