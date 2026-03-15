import sys
import os
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright

headless = "--headless" in sys.argv
interval = (
    int(sys.argv[sys.argv.index("--interval") + 1]) if "--interval" in sys.argv else 5
)
ntfy_url = "https://ntfy.sh/MH-ShiftMatch-Alerts"
page = None
seen_shifts = set()

try:
    with sync_playwright() as p:
        # Create a new browser instance
        browser = p.chromium.launch(headless=headless, args=["--incognito"])
        page = browser.new_page()
        page.goto("https://mh.shiftmatch.com.au/shiftmatch/login?r=%2F")

        # Fill in the login form
        # Username
        page.get_by_role("textbox", name="Your Employee Number").fill("701559")
        print("Entered username")

        # Password
        page.get_by_role("textbox", name="Password").fill("Jellybeans1991!")
        print("Entered password")

        # Submit
        page.get_by_role("button", name="Sign in").click()
        print("Submitted")

        page.wait_for_timeout(2000)

        # Go to my roster
        page.get_by_role("link", name="My Roster").click()

        # Change to kanban view
        page.get_by_role("button").nth(5).click()

        # Loop to check for shifts
        print("Loop starting...")
        last_alive = 0
        while True:
            page.wait_for_timeout(2000)
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            columns = soup.find_all("app-kanban-column")
            for column in columns:
                # Look for the open roster column
                header = column.find("span", class_="capitalize")
                if header and "open roster" in header.text.lower():
                    current_date = None
                    body = column.find("div", class_="kanban-column-body")
                    if body is None:
                        break
                    # Loop through each shift found
                    for child in body.children:
                        if not isinstance(child, Tag):
                            continue
                        if "day-heading" in (child.get("class") or []):
                            current_date = child.get_text(strip=True)
                        elif child.name == "app-shortfall-list-item":
                            item_text = child.get_text().lower()
                            if (
                                "dandenong hospital" in item_text
                                and "emergency" in item_text
                            ):
                                time_span = child.find("span", class_="heading")
                                shift_time = (
                                    time_span.get_text(strip=True)
                                    if time_span
                                    else "Unknown time"
                                )
                                shift_key = f"{current_date}_{shift_time}"
                                if shift_key in seen_shifts:
                                    continue
                                seen_shifts.add(shift_key)
                                msg = f"Shift available at Dandenong Emergency! {current_date} {shift_time}"
                                print(msg)
                                requests.post(
                                    ntfy_url,
                                    data=msg,
                                )
                    break

            # Log if still alive
            if time.time() - last_alive >= 180:
                print(f"Still running - {datetime.now().strftime('%H:%M:%S')}")
                last_alive = time.time()

            # Wait then relaod
            time.sleep(interval)
            page.get_by_role("button", name="Today").click()
            page.reload()
except Exception as e:
    print(f"Exception: {e}")
    if page is not None:
        try:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = (
                f"screenshots/error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        except Exception:
            pass
    requests.post(
        ntfy_url,
        data="ShiftMatch script has crashed! Check the logs!",
    )
    print("Crash detected, exiting...")
    sys.exit(1)
