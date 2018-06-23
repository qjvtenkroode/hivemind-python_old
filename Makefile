.PHONY: clean, test

PROJECTDIR = ~/playground/active/hivemind

bootstrap: dev_requirements.txt
ifdef TRAVIS
	@echo "Inside TravisCI, bootstrapping..."
	pip install -r dev_requirements.txt
else
ifeq ($(wildcard $(PROJECTDIR)/env),)
	@echo "Bootstrapping virtualenv"
	python3 -m venv $(PROJECTDIR)/env
endif
	$(PROJECTDIR)/env/bin/pip install -r dev_requirements.txt
endif
	@echo "Done bootstrapping"

clean:
	@echo "Remove all temporary Python files"
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +
	@echo "Done removing"

docker:
ifeq ($(strip $(shell docker ps -a -f name=hivemind-nervecenter --format {{.Names}})),hivemind-nervecenter)
	@echo "Found existing containers"
	docker start hivemind-nervecenter
else
	@echo "Building container images from dockerfiles"
	docker build dockerfiles -f dockerfiles/Rabbitmq_mqtt_management -t hivemind:nervecenter
	@echo "Done building container images"
	@echo "Running container:"
	docker run -d --hostname hivemind-nervecenter --name hivemind-nervecenter -p 1883:1883 -p 5672:5672 -p 15672:15672 hivemind:nervecenter
endif
	@echo "Done running containers"

test:
	@echo "Starting test suite with pytest"
ifdef TRAVIS
	pytest
else
	$(PROJECTDIR)/env/bin/pytest
endif
