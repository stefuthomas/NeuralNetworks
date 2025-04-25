import requests
from bs4 import BeautifulSoup
import json


def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    main_container = soup.find('main-container')
    article_text_div = soup.find('div', class_='article-text')

    if article:
        paragraphs = article.find_all('p')
    elif main_container:
        paragraphs = main_container.find_all('p')
    elif article_text_div:
        paragraphs = article_text_div.find_all('p')
    else:
        paragraphs = soup.find_all('p')

    article_text = ' '.join(p.get_text() for p in paragraphs if p.get_text())

    return article_text.strip()

yle = [
    "https://yle.fi/a/74-20157596",
    "https://yle.fi/a/74-20158034"
]
yle_summaries = [
    "Joroisten kunnassa on vakava rottaongelma...",
    "Entiset ministerit Matti Vanhanen ja Osmo Soininvaara kritisoivat yhteisöveron laskemista..."
]

hs = [
    "https://www.hs.fi/politiikka/art-2000011190341.html"
]
hs_summaries = [
    "Taloustutkijoiden mukaan hallituksen 12 miljoonan euron yritystukileikkaus on erittäin pieni..."
]

iltalehti = [
    "https://www.iltalehti.fi/ulkomaat/a/73a46709-9483-4d82-8b5a-41fe2ebf989d"
]
iltalehti_summaries = [
    "Britannia luopuu suunnitelmistaan lähettää joukkoja Ukrainaan..."
]

mtv = [
    "https://www.mtvuutiset.fi/artikkeli/trumpin-vihjailu-kolmannesta-kaudesta-yltyy-myynnissa-hammastyttava-tuote/9143602"
]
mtv_summaries = [
    "Donald Trump on vihjaillut olevansa avoin kolmannelle presidenttikaudelle..."
]


urls = yle + hs + iltalehti + mtv
summaries = yle_summaries + hs_summaries + iltalehti_summaries + mtv_summaries

dataset = []

for i, url in enumerate(urls):
    try:
        full_text = scrape_article(url)
        summary = summaries[i]

        entry = {
            "text": full_text,
            "summary": summary
        }
        dataset.append(entry)

    except Exception as e:
        print(f"Virhe artikkelissa {url}: {e}")

with open("projects/datasets/article_summary/finnish_articles.json", "w", encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
