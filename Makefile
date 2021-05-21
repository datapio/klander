.PHONY: all
all:
	@poetry install
	@poetry run pyinstaller --onefile src/klander.py

.PHONY: docker/build
docker/build:
	@docker build -t ghcr.io/datapio/klander:latest -f Dockerfile .

.PHONY: docker/run
docker/run:
	@docker run --rm ghcr.io/datapio/klander:latest
