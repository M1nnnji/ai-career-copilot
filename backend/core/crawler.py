from playwright.sync_api import sync_playwright


def crawl_job(url: str) -> str:
    with sync_playwright() as p:
        print("1. playwright start")

        browser = p.chromium.launch(headless=True)
        print("2. browser launched")

        page = browser.new_page()
        print("3. page created")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000,
        )
        print("4. page loaded")

        page.wait_for_timeout(3000)
        print("5. waited")

        text = page.locator("body").inner_text()
        print("6. text length =", len(text))

        browser.close()

        return text