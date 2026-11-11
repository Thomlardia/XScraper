# XScraper
Code repository for scraping data from X

## Tools used
 
| Tool | Purpose |
|---|---|
| **Python 3** | Language the script is written in |
| **Playwright** | Library that controls the browser and reads the page |
| **Chrome DevTools Protocol (CDP)** | The channel Playwright uses to attach to a running Chrome via port 9222 |
| **Google Chrome** | The browser that hosts X |
| **csv** (Python standard library) | Writes the results file |
| **VSCodium + Git** | Editing and version control |


## Setup (one time)
 
**1. Install Chrome**:
 
```bash
cd ~/Downloads
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
 
**2. Create a virtual environment and install Playwright:**
 
```bash
cd ~/XScraper
python3 -m venv venv
source venv/bin/activate
pip install playwright
```
 
If `python3 -m venv` fails, run `sudo apt install python3-venv` first.

## How to run
 
**1. Start Chrome with remote debugging** (leave this terminal and window open):
 
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=$HOME/chrome-scraper-profile
```
 
**2. In that Chrome window**, log in to X manually, then open the post whose replies you want. Click into the post so the replies are showing. 
 
**3. In a second terminal, run the scraper:**
 
```bash
cd ~/XScraper
source venv/bin/activate
python3 scrape.py
```
 
**4.** When it finishes, `comments.csv` appears in the project folder.
 
While it runs, leave Chrome on the post and do not switch tabs