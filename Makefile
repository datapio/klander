.PHONY: all
all:
	@poetry install
	@poetry run pyinstaller --onefile src/global_reconciler.py
