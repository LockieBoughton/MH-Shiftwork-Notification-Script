# ShiftMatch

Monitors the ShiftMatch roster for available shifts at Dandenong Hospital Emergency and sends push notifications via ntfy.sh when one is found.

## Fresh Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install just

```bash
# macOS
brew install just

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
```

### 3. Install dependencies and Playwright browser

```bash
just install
```

This runs `uv sync` to install Python packages and `playwright install chromium` to download the browser.

## Running

```bash
# Run with a visible browser window
just run

# Run headless (no window) with a custom check interval in seconds
just run-headless 10

# Run with Playwright inspector for debugging
just inspect
```

## Notifications

Notifications are sent to ntfy.sh. Subscribe to alerts on your phone by installing the [ntfy app](https://ntfy.sh) and subscribing to the topic `MH-ShiftMatch-Alerts`.

## Output

- `screenshots/` — Screenshots captured on crash for debugging
