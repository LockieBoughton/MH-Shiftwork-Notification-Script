INTERVAL ?= 5

install:
	uv sync
	uv run playwright install chromium

run:
	uv run main.py --headless --interval $(INTERVAL)

run-visible:
	uv run main.py

inspect:
	PWDEBUG=1 uv run main.py
