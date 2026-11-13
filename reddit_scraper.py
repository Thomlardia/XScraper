# Scrapes comments from Reddit

import csv
from urllib.parse import urlparse, urlunparse
from playwright.sync_api import sync_playwright

MAX_CLICKS = 200   # max number of "load more comments" clicks

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

    # pick the tab that is on reddit
    page = next((pg for pg in context.pages if "reddit.com" in pg.url), context.pages[0])

    # old.reddit.com has simple, stable HTML, so switch the tab to it
    parts = urlparse(page.url)
    old_url = urlunparse(parts._replace(netloc="old.reddit.com"))
    print("Scraping:", old_url)
    page.goto(old_url)
    page.wait_for_selector("div.commentarea", timeout=15000)

    # expand every "load more comments" button
    for i in range(MAX_CLICKS):
        more = page.locator("span.morecomments > a").first
        if more.count() == 0:
            break
        try:
            more.click(timeout=5000)
            page.wait_for_timeout(1200)
        except Exception:
            break
        print(f"Loaded more comments (click {i + 1})", end="\r")

    # read all comments from the page in one go
    rows = page.evaluate("""
    () => [...document.querySelectorAll('div.commentarea div.thing.comment')].map(c => {
        const body = c.querySelector(':scope > .entry .usertext-body .md');
        const time = c.querySelector(':scope > .entry time');
        let depth = 0, el = c.parentElement;
        while (el) {
            if (el.matches && el.matches('div.thing.comment')) depth++;
            el = el.parentElement;
        }
        return {
            id: c.dataset.fullname || '',
            author: c.dataset.author || '',
            score: c.dataset.score || '',
            datetime: time ? time.getAttribute('datetime') : '',
            depth: depth,
            text: body ? body.innerText.replace(/\\n+/g, ' ').trim() : '',
            link: c.dataset.permalink ? 'https://old.reddit.com' + c.dataset.permalink : ''
        };
    })
    """)

    with open("reddit_comments.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "author", "score", "datetime", "depth", "text", "link"])
        for r in rows:
            writer.writerow([r["id"], r["author"], r["score"], r["datetime"],
                             r["depth"], r["text"], r["link"]])

    print(f"\nSaved {len(rows)} comments to reddit_comments.csv")