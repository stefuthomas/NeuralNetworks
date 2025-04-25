import requests
from bs4 import BeautifulSoup
import json


def scrape_article(url, article_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    main_container = soup.find('main-container')
    article_text_div = soup.find('div', class_='article-text')
    artice_body = soup.find('section', class_='article-body')

    if article_type == "yle" or article_type == "iltasanomat":
        paragraphs = article.find_all('p')
    elif article_type == "hs":
        paragraphs = artice_body.find_all('p')
    elif article_type == "iltalehti":
        paragraphs = main_container.find_all('p')
    else:
        paragraphs = article_text_div.find_all('p')

    article_text = ' '.join(p.get_text() for p in paragraphs if p.get_text())
    return article_text.strip()


# Artikkelit ja tiivistelmät, lisätty mukaan myös article_type
articles = []

articles += [(url, summary, "yle") for url, summary in zip(
    [
        "https://yle.fi/a/74-20157596",
        "https://yle.fi/a/74-20158034"
    ],
    [
        "Joroisten kunnassa on vakava rottaongelma...",
        "Entiset ministerit Matti Vanhanen ja Osmo Soininvaara kritisoivat yhteisöveron laskemista..."
    ]
)]

articles += [(url, summary, "hs") for url, summary in zip(
    [
        "https://www.hs.fi/politiikka/art-2000011190341.html"
    ],
    [
        "Taloustutkijoiden mukaan hallituksen 12 miljoonan euron yritystukileikkaus on erittäin pieni..."
    ]
)]

articles += [(url, summary, "iltasanomat") for url, summary in zip(
    [],
    []
)]

articles += [(url, summary, "iltalehti") for url, summary in zip(
    [
        "https://www.iltalehti.fi/ulkomaat/a/73a46709-9483-4d82-8b5a-41fe2ebf989d"
    ],
    [
        "Britannia luopuu suunnitelmistaan lähettää joukkoja Ukrainaan..."
    ]
)]

articles += [(url, summary, "mtv") for url, summary in zip(
    [
        "https://www.mtvuutiset.fi/artikkeli/trumpin-vihjailu-kolmannesta-kaudesta-yltyy-myynnissa-hammastyttava-tuote/9143602",
        "https://www.mtvuutiset.fi/artikkeli/nyt-se-on-varmaa-ville-peltoselle-potkut/9143752"
    ],
    [
        "Donald Trump on vihjaillut olevansa avoin kolmannelle presidenttikaudelle...",
        "Helsingin IFK on vapauttanut päävalmentaja Ville Peltosen sekä apuvalmentajat Samuel Tilkasen ja Marko Ojasen tehtävistään..."
    ]
)]

dataset = []

for i, (url, summary, article_type) in enumerate(articles):
    try:
        full_text = scrape_article(url, article_type)
        entry = {
            "text": full_text,
            "summary": summary
        }
        dataset.append(entry)
    except Exception as e:
        print(f"Virhe artikkelissa {url}: {e}")

with open("projects/datasets/article_summary/finnish_articles.json", "w", encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
