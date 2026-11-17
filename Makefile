PYTHON ?= python3
VENV_PYTHON := .venv/bin/python
PARAMETERS ?= 7000000000
PRECISION ?= fp16
ENVIRONMENT ?= local
IMAGE ?= ai-lab-starter

.PHONY: setup check test estimate benchmark docker-build docker-check

setup:
	PYTHON="$(PYTHON)" sh scripts/setup.sh

check:
	$(VENV_PYTHON) -m ailab.check_env

test:
	$(VENV_PYTHON) -m pytest

estimate:
	$(VENV_PYTHON) -m ailab.model_size $(PARAMETERS) $(PRECISION)

benchmark:
	$(VENV_PYTHON) -m ailab.benchmark --environment $(ENVIRONMENT)

docker-build:
	docker build -t $(IMAGE) .

docker-check: docker-build
	docker run --rm $(IMAGE)
