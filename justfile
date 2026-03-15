install:
    uv sync
    uv run playwright install chromium

run:
    uv run main.py

run-headless interval="5":
    uv run main.py --headless --interval {{interval}}

inspect:
    PWDEBUG=1 uv run main.py
