import csv
from playwright.sync_api import sync_playwright

MAX_SCROLLS = 50        # How many times the script will scroll down
IDLE_LIMIT = 5          # stop after this many scrolls with nothing new

with sync_playwright() as p: # starts playwright and assigns it to the variable p
    browser = p.chromium.connect_over_cdp("http://localhost:9222") # connects to the manually opened chrome page
    context = browser.contexts[0] # sets context

    # pick the tab that is on x.com 
    page = next((pg for pg in context.pages if "x.com" in pg.url), context.pages[0])
    print("Scraping:", page.url) # check adress

    comments = {}   # dictionary containing user and text as keys to check duplicates. value is the tuple (user, when, text, link) which gets turned into csv
    idle = 0 # counter for scrolls where nothing changes

    for _ in range(MAX_SCROLLS): # repeats block for every scroll
        before = len(comments) # store the lenght of comments to see if anything changes in the page

        # loop over all comments (tweets) currently in the page
        # for each tweet, find necesarry data and store it to the comments dictionary
        for tweet in page.locator('article[data-testid="tweet"]').all():
            try: # error handling
                user = tweet.locator('[data-testid="User-Name"]').inner_text().replace("\n", " ")
                text_loc = tweet.locator('[data-testid="tweetText"]')
                text = text_loc.inner_text().replace("\n", " ") if text_loc.count() else ""
                time_loc = tweet.locator("time")
                when = time_loc.first.get_attribute("datetime") if time_loc.count() else ""
                link_loc = tweet.locator('a:has(time)')
                link = "https://x.com" + link_loc.first.get_attribute("href") if link_loc.count() else ""
                comments[(user, text)] = (user, when, text, link) # store data
            except Exception: # if the sequence fails, move on to next tweet instead of erroring
                pass

        # stop if no new comments are collected
        idle = idle + 1 if len(comments) == before else 0
        if idle >= IDLE_LIMIT:
            break

        # simulated scrolling command
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(1500)

    # save data to csv
    with open("comments.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "datetime", "text", "link"])
        writer.writerows(comments.values())

    print(f"Saved {len(comments)} items to comments.csv")