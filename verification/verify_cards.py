
import os
from playwright.sync_api import sync_playwright

def verify_cards():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get absolute path to index.html
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"

        print(f"Navigating to {file_path}")
        page.goto(file_path)

        # Wait for the JS to populate the cards
        page.wait_for_selector("#sponsorName", state="visible")
        page.wait_for_selector("#chaosName", state="visible")
        page.wait_for_selector("#goodCitizenName", state="visible")

        # Take a full page screenshot to see the context
        page.screenshot(path="verification/full_page.png", full_page=True)

        # Take specific screenshots of the cards
        # 1. Sponsor Card
        sponsor_card = page.locator(".sponsor-card")
        sponsor_card.screenshot(path="verification/sponsor_card.png")

        # 2. Chaos Card
        chaos_card = page.locator(".chaos-card")
        chaos_card.screenshot(path="verification/chaos_card.png")

        # 3. Minimalist Card
        # The minimalist card is inside a specific container, we can find it by its unique content or class structure if specific class isn't unique enough.
        # But we added unique content structure. Let's try to locate by the "Fez o Mínimo" span parent's parent container or just the card containing #goodCitizenName
        # The card container has `bg-gray-100 rounded-xl border border-gray-300 p-6`

        # Locate by text inside
        minimalist_card = page.locator("div.bg-gray-100.rounded-xl.border.border-gray-300.p-6", has_text="Fez o Mínimo")
        if minimalist_card.count() > 0:
            minimalist_card.first.screenshot(path="verification/minimalist_card.png")
        else:
            print("Could not find Minimalist card specifically")

        browser.close()

if __name__ == "__main__":
    verify_cards()
