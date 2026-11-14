import csv
import sys
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    sys.exit("Usage: python3 parse_reddit.py saved_page.html")

with open(sys.argv[1], encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

rows = []
for c in soup.select("div.commentarea div.thing.comment"):
    entry = c.find("div", class_="entry", recursive=False)
    if entry is None:
        continue

    body = entry.select_one(".usertext-body .md")
    time = entry.find("time")
    depth = len(c.find_parents("div", class_="comment")) + 1
    permalink = c.get("data-permalink", "")

    rows.append([
        c.get("data-fullname", ""),
        c.get("data-author", ""),
        c.get("data-score", ""),
        time.get("datetime", "") if time else "",
        depth,
        " ".join(body.get_text(" ").split()) if body else "",
        "https://old.reddit.com" + permalink if permalink else "",
    ])

with open("reddit_comments.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "author", "score", "datetime", "depth", "text", "link"])
    writer.writerows(rows)

print(f"Saved {len(rows)} comments to reddit_comments.csv")