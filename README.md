# XScraper
Code repository for scraping data from X and Reddit. 

## Tools / Requirements
|---|---|---|
| **Python 3** | Language the script is written in |
| **Playwright** | Library that controls the browser and reads the page (for X) |
| **BeautifulSoup** | Library that reads html pages (for Reddit) |
| **Chrome DevTools Protocol (CDP)** | The channel Playwright uses to attach to a running Chrome |
| **Google Chrome** | The browser that hosts X |
| **csv** (Python standard library) | Writes the results file |
| **VSCodium + Git** | Editing and version control |
| **Linux** | OS used for the project (another OS would only need different commands for functionality) |


## Setup (one time)
 
**1. Install Chrome**:
 
```bash
cd ~/Downloads
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
 
**2. Create a virtual environment and install Playwright (for X) and BeautifulSoup (for Reddit):**
 
```bash
cd ~/XScraper
python3 -m venv venv
source venv/bin/activate
pip install playwright
pip install beautifulsoup4
```
 
If `python3 -m venv` fails, run `sudo apt install python3-venv` first.

## How to run
### X
 
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

### Reddit
#### Step 1: get threads
 
1. Open the thread in Chrome.
2. In the address bar, change `www.reddit.com` to `old.reddit.com` and press Enter. The script only works on the old layout.
3. Scroll down and click every **"load more comments"** link you want included. Only comments visible on the page when you save are captured.
4. Press `Ctrl+S` and set **Save as type** to **Webpage, Complete**. (Do not choose "HTML only": it saves the page from before you expanded the comments.)
5. Save the file:
   - for the single parser: into `~/XScraper` as `thread.html`
   - for the all-threads parser: into `~/XScraper/threads/` as `thread1.html`, `thread2.html`, `thread3.html`, and so on
Chrome also creates a folder next to the file (for example `thread1_files`). You can ignore or delete it.
 
**If `Ctrl+S` does nothing:** click an empty part of the page first, or use the three-dot menu, then **Cast, save, and share**, then **Save page as...**. As a last resort: press `F12`, open the **Elements** tab, right-click the first line (`<html ...>`), choose **Copy**, then **Copy outerHTML**, paste into a new file in VSCodium, and save it as `thread1.html`.
 
#### Step 2a: Parse ONE thread
 
```bash
cd ~/XScraper/Reddit
source venv/bin/activate
python3 parse_reddit.py thread.html
```
 
Replace `thread.html` with your file name. The result is `reddit_comments.csv` in `~/XScraper`.
 
#### Step 2b: Parse ALL threads in the folder
 
Folder layout:
 
```
XScraper/Reddit
  parse_reddit_all.py
  threads/
    thread1.html
    thread2.html
    thread3.html
```
 
Run:
 
```bash
cd ~/XScraper/Reddit
source venv/bin/activate
python3 parse_reddit_all.py
```

## Output Structure

### Reddit
 
One row per comment, all threads combined.
 
| Column | Description | Example |
|---|---|---|
| `id` | Reddit's unique comment ID (`t1_` prefix) | `t1_k3x9abc` |
| `author` | Commenter's username, or `[deleted]` | `some_user` |
| `score` | Net upvotes when the page was saved | `42` |
| `datetime` | Time posted, ISO 8601 (UTC) | `2026-11-10T14:03:22+00:00` |
| `depth` | Nesting level: 1 = top-level comment, 2 = reply to it, and so on | `1` |
| `text` | Comment text, line breaks flattened to spaces | `Great post, thanks!` |
| `link` | Direct URL to the comment | `https://old.reddit.com/r/.../k3x9abc/` |
| `thread_title` | Page title of that thread | `Best budget laptop? : r/laptops` |

