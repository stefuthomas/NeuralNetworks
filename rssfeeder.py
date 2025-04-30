import feedparser
from newspaper import Article
import json
import time
from tqdm import tqdm
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"  # estää varoituksen

print("🧠 Initializing summarizer model...")
from transformers import pipeline
summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
print("✅ Summarizer ready.")

# 2. List of Finnish RSS feeds (you can expand this)
rss_feeds = [
    "https://feeds.yle.fi/uutiset/v1/mostRead/YLE_UUTISET.rss",
    "https://www.hs.fi/rss/uutiset.xml",
    "https://www.is.fi/rss/tuoreimmat.xml",
    "https://www.talouselama.fi/rss.xml",
    "https://www.uusisuomi.fi/feed",
    "https://www.iltalehti.fi/rss.xml"
]


# 3. Output setup
articles = []
seen_urls = set()
max_articles = 10

print("📡 Fetching and summarizing Finnish news articles...")

for feed_url in rss_feeds:
    feed = feedparser.parse(feed_url)
    for entry in tqdm(feed.entries, desc=f"📥 {feed_url}"):
        if len(articles) >= max_articles:
            break
        url = entry.link
        if url in seen_urls:
            continue
        try:
            article = Article(url, language='fi')
            article.download()
            article.parse()
            text = article.text.strip()

            if len(text) < 200:
                continue  # skip too-short or broken articles

            # Use summary from feed if available
            summary = entry.get("summary", "").strip()
            print(summary)
            if not summary or len(summary) < 30:
                continue

            articles.append({
                "text": text,
                "summary": summary
            })
            seen_urls.add(url)

            print(f"✅ Collected: {entry.title}")
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
        time.sleep(0.5)

    if len(articles) >= max_articles:
        break

# 5. Save result
output_path = "finnish_articles_rss.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"\n✅ Done. Collected {len(articles)} articles.")
print(f"💾 Saved to {output_path}")
