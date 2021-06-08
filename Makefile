PYRIGHT := $(shell which pyright 2> /dev/null)

.PHONY: all
all: lint typecheck test build

.PHONY: deps
deps:
	@poetry install

.PHONY: lint
lint: deps
	@poetry run pylint src

.PHONY: typecheck
typecheck: deps
ifdef PYRIGHT
	@poetry run pyright src
else
	@echo "!!WARNING!! pyright was not found, no type checking has been done."
endif

.PHONY: test
test: deps
	@poetry run pytest --cov=src/klander_core --cov-report html --cov-report term --cov-fail-under=95

.PHONY: build
build: deps
	@poetry run pyinstaller --onefile src/klander.py

.PHONY: docker/build
docker/build:
	@docker build -t ghcr.io/datapio/klander:latest -f Dockerfile .

.PHONY: docker/run
docker/run:
	@docker run --rm ghcr.io/datapio/klander:latest
