# ShiftMatch

Monitors the ShiftMatch roster for available shifts at Dandenong Hospital Emergency and sends push notifications via ntfy.sh when one is found.

## Fresh Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies and Playwright browser

```bash
make install
```

This runs `uv sync` to install Python packages and `playwright install chromium` to download the browser.

## Running

```bash
# Run headless (default, no window) with optional interval in seconds
make run
make run INTERVAL=10

# Run with a visible browser window
make run-visible

# Run with Playwright inspector for debugging
make inspect
```

## Notifications

Notifications are sent to ntfy.sh. Subscribe to alerts on your phone by installing the [ntfy app](https://ntfy.sh) and subscribing to the topic `MH-ShiftMatch-Alerts`.

## Output

- `screenshots/` — Screenshots captured on crash for debugging
