import csv
from playwright.sync_api import sync_playwright

MAX_SCROLLS = 50       
IDLE_LIMIT = 5          # stop after this many scrolls with nothing new

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

    # pick the tab that is on x.com 
    page = next((pg for pg in context.pages if "x.com" in pg.url or "twitter.com" in pg.url), context.pages[0])
    print("Scraping:", page.url)

    comments = {}   # keyed by (username, text) to avoid duplicates
    idle = 0

    for _ in range(MAX_SCROLLS):
        before = len(comments)

        for tweet in page.locator('article[data-testid="tweet"]').all():
            try:
                user = tweet.locator('[data-testid="User-Name"]').inner_text().replace("\n", " ")
                text_loc = tweet.locator('[data-testid="tweetText"]')
                text = text_loc.inner_text().replace("\n", " ") if text_loc.count() else ""
                time_loc = tweet.locator("time")
                when = time_loc.first.get_attribute("datetime") if time_loc.count() else ""
                link_loc = tweet.locator('a:has(time)')
                link = "https://x.com" + link_loc.first.get_attribute("href") if link_loc.count() else ""
                comments[(user, text)] = (user, when, text, link)
            except Exception:
                pass

        idle = idle + 1 if len(comments) == before else 0
        if idle >= IDLE_LIMIT:
            break

        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1500)

    with open("comments.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "datetime", "text", "link"])
        writer.writerows(comments.values())

    print(f"Saved {len(comments)} items to comments.csv")