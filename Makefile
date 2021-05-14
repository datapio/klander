.PHONY: all
all:
	@poetry install
	@poetry run pyinstaller --onefile src/klander.py
