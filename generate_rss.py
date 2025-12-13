import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urlparse

ARCHIVE_URL = "https://nav.al/archive"

EXCLUDE_SLUGS = {
    "archive", "subscribe", "search",
    "wealth", "venture-capital", "technology", "science",
    "quotes", "politics", "podcast", "jobs",
    "interviews", "happiness", "crypto", "classifieds",
    "bubble", "stories", "startups", "sundry",
    "uncategorized", "instagram", "twitter"
}

r = requests.get(ARCHIVE_URL, timeout=20)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

seen = set()
items = []

for a in soup.select("a[href^='https://nav.al/']"):
    title = a.get_text(strip=True)
    href = a["href"]

    if not title:
        continue

    slug = urlparse(href).path.strip("/")

    # skip obvious non-articles
    if not href.startswith("https://nav.al") or slug in EXCLUDE_SLUGS:
        continue

    if href in seen:
        continue

    seen.add(href)
    items.append((title, href))

print(f"Found {len(items)} essays")

fg = FeedGenerator()
fg.id(ARCHIVE_URL)
fg.title("Naval Ravikant – Archive (Unofficial)")
fg.link(href=ARCHIVE_URL, rel="alternate")
fg.description("Unofficial RSS feed generated from nav.al/archive")

# newest first
items.reverse()

for title, url in items:
    fe = fg.add_entry()
    fe.id(url)
    fe.title(title)
    fe.link(href=url)

fg.rss_file("naval_archive.xml")
print("Wrote naval_archive.xml")
