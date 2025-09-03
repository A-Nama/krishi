import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from readability import Document
from google import genai
from google.genai import types
from dotenv import load_dotenv 

# Load environment variables from .env
load_dotenv()

# Malayalam character range regex
malayalam_pattern = re.compile(r'[\u0D00-\u0D7F]')

# Gemini client using key from .env
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def scrape_article(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    html = response.text

    doc = Document(html)
    title = doc.short_title().strip()

    soup = BeautifulSoup(doc.summary(), "html.parser")
    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        # Keep only if it contains Malayalam characters
        if malayalam_pattern.search(text):
            paragraphs.append(text)

    content = "\n".join(paragraphs)
    return title, content

def rewrite_content(original_content):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=original_content)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0.8,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""You are given the content of a markdown file containing a news article from an agriculture news site.
Your task:

Keep the title same as provided externally.
Rewrite only the content in clear, concise, and engaging language while keeping all factual information intact. Keep the information Malayalam.

Remove irrelevant text like ads, unrelated navigation elements, or decorative captions that don't add factual agricultural information.

Output only a valid JSON object in the following format:
{
  "content": "Rewritten full article content here"
}
Ensure no extra commentary or text outside the JSON object.

Input format: Markdown
Output format: JSON with content
"""),
        ],
    )

    result_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            result_text += chunk.text

    return result_text

if __name__ == "__main__":
    url ="https://www.mathrubhumi.com/agriculture/tips/protect-chickens-summer-heat-1.10425394"

    # Step 1: Scrape
    title, content = scrape_article(url)

    # Step 2: Rewrite with Gemini
    rewritten_json = rewrite_content(content)

    # Step 3: Save to DataFrame
    df = pd.DataFrame([{"url": url, "title": title, "content": rewritten_json}])
    df.to_csv("articles42.csv", index=False, encoding="utf-8")

    print(df)
