import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def is_malayalam(text):
    # At least one Malayalam character
    return bool(re.search(r'[\u0D00-\u0D7F]', text))

def contains_link(text):
    # Detect if paragraph contains a URL or email
    return bool(re.search(r'(https?://|www\.)', text))

urls = [
    "https://www.krishipadam.com/growing-grapes-kerala/"
]

data = []

for url in urls:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            continue
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Title
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
        
        # All paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        
        # Filter rules:
        # 1. Must contain Malayalam
        # 2. Must NOT contain a link
        filtered_paragraphs = [
            p for p in paragraphs
            if is_malayalam(p) and not contains_link(p)
        ]
        
        clean_text = " ".join(filtered_paragraphs)
        
        data.append({
            "url": url,
            "title": title,
            "content": clean_text
        })
        
        time.sleep(2)
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")

df = pd.DataFrame(data)
df.to_csv("clean_malayalam_articles.csv", index=False, encoding="utf-8-sig")
print("Scraping complete! Saved to clean_malayalam_articles.csv")
