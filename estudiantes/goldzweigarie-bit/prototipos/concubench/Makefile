IMAGE ?= concubench-base:latest
PY ?= python3

.PHONY: image test validate oracle

image:
	docker build -t $(IMAGE) images/base

test:
	$(PY) -m unittest -v

validate:
	$(PY) -m bench validate --image $(IMAGE)

oracle:
	$(PY) -m bench run --agent oracle --attempts 3 --image $(IMAGE)
