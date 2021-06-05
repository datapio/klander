PYRIGHT := $(shell which pyright 2> /dev/null)

.PHONY: all
all: lint typecheck build

.PHONY: deps
deps:
	@poetry install

.PHONY: lint
lint: deps
	@poetry run pylint src

.PHONY: typecheck
typecheck:
ifdef PYRIGHT
	@poetry run pyright
endif

.PHONY: build
build: deps
	@poetry run pyinstaller --onefile src/klander.py

.PHONY: docker/build
docker/build:
	@docker build -t ghcr.io/datapio/klander:latest -f Dockerfile .

.PHONY: docker/run
docker/run:
	@docker run --rm ghcr.io/datapio/klander:latest
