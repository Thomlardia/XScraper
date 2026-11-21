# XScraper
Code repository for scraping data from X and Reddit. 

## Tools / Requirements
|---|---|
| **Python 3** | Language the script is written in |
| **Playwright** | Library that controls the browser and reads the page (for X) |
| **BeautifulSoup** | Library that reads html pages (for Reddit) |
| **Chrome DevTools Protocol (CDP)** | The channel Playwright uses to attach to a running Chrome |
| **Google Chrome** | The browser that hosts X and Reddit |
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

### [X](X/x_scraper.md)
### [Reddit](Reddit/reddit_parser.md)
