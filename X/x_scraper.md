# X Scraper
## How to run

**1. Start Chrome with remote debugging** (leave this terminal and window open):
 
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=$HOME/chrome-scraper-profile
```
 
**2. In that Chrome window**, log in to X manually, then open the post whose replies you want. Click into the post so the replies are showing. 
 
**3. In a second terminal, run the scraper:**

```bash
cd ~/XScraper/X
source venv/bin/activate
python3 x_scraper.py
```

**4.** When it finishes, the .csv file will appear in the project folder.
 
While it runs, leave Chrome on the post and do not switch tabs

## Output

| Column | Description | Example |
|---|---|---|
| `user` | Display name and @handle as shown on the page, line breaks flattened to spaces | `Some User @some_user · 3h` |
| `datetime` | Time posted, ISO 8601 (UTC), from the tweet's `<time>` element; empty if missing | `2026-11-10T14:03:22.000Z` |
| `text` | Comment text, line breaks flattened to spaces; empty if the tweet has no text (e.g. image only) | `Great post, thanks!` |
| `link` | Direct URL to the comment | `https://x.com/some_user/status/1234567890123456789` |
| `likes` | Like count as displayed by X when scraped; `0` if nothing is shown. Large numbers stay abbreviated | `42`, `1.2K` |
| `replies` | Reply count as displayed by X when scraped; `0` if nothing is shown. Large numbers stay abbreviated | `3`, `1.2K` |

Notes:
- **Duplicates:** rows are deduplicated by `(user, text)`, so the same user posting identical text twice is kept once.
- **No `id`:** the script doesn't collect this. The tweet ID is the last part of `link`, and could be added after scraping.

