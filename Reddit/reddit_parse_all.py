# parses all html pages in the threads folder

import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path(__file__).parent          # folder this script is in
THREADS_DIR = BASE / "threads"        # folder with thread1.html, thread2.html, ...
OUTPUT = BASE / "reddit_comments.csv" # location of .csv file

# function to sort in order: thread2 before thread10
def natural_key(path):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", path.name)]

# function for parsing single html file
def parse_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser") # beautifullSoup makes html page searchable

    title = " ".join(soup.title.get_text().split()) if soup.title else "" # get page title
    rows = [] # list that will hold one entry per comment

    # loop over all comments in html file
    for c in soup.select("div.commentarea div.thing.comment"):
        entry = c.find("div", class_="entry", recursive=False) # look only inside the comment
        if entry is None: # skip to the next comment if no entry
            continue

        body = entry.select_one(".usertext-body .md") # get comment text
        time = entry.find("time") # get time stamp
        depth = len(c.find_parents("div", class_="comment")) + 1 # get depth
        permalink = c.get("data-permalink", "") # get link

        # build a single row
        rows.append([
            c.get("data-fullname", ""),
            c.get("data-author", ""),
            c.get("data-score", ""),
            time.get("datetime", "") if time else "",
            depth,
            " ".join(body.get_text(" ").split()) if body else "",
            "https://old.reddit.com" + permalink if permalink else "",
            title,
        ])
    return rows 


files = sorted(THREADS_DIR.glob("*.html"), key=natural_key) # finds all html files and sorts them
if not files:
    raise SystemExit(f"No .html files found in {THREADS_DIR}") # error if folder is empty/missing

all_rows = [] # full dataset

# loop over all html pages and get data from every page
for path in files: 
    rows = parse_file(path)
    print(f"{path.name}: {len(rows)} comments")
    all_rows.extend(rows)

# write data to csv
with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "author", "score", "datetime", "depth",
                     "text", "link", "thread_title"])
    writer.writerows(all_rows)

print(f"\nSaved {len(all_rows)} comments from {len(files)} threads to {OUTPUT.name}")