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

freeze:
	@echo "Freezing dev dependencies"
	$(PROJECTDIR)/env/bin/pip freeze | sort - > dev_requirements.txt
	@echo "Done"

test:
	@echo "Starting test suite with pytest"
ifdef TRAVIS
	pytest
else
	$(PROJECTDIR)/env/bin/pytest
endif
