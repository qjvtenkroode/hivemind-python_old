.PHONY: clean, test

PROJECTDIR = ~/playground/active/hivemind

bootstrap: dev_requirements.txt
ifeq ($(wildcard $(PROJECTDIR)/env),)
	@echo "Bootstrapping virtualenv"
	python3 -m venv $(PROJECTDIR)/env
endif
	$(PROJECTDIR)/env/bin/pip install -r dev_requirements.txt
	@echo "Done bootstrapping"

bootstrap-travisci: dev_requirements.txt
	pip install -r dev_requirements

clean:
	@echo "Remove all temporary Python files"
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +
	@echo "Done removing"

test:
	@echo "Starting test suite with pytest"
ifeq ($(TRAVIS),"TRUE")
	pytest
else
	$(PROJECTDIR)/env/bin/pytest
endif
