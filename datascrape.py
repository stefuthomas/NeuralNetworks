import requests
from bs4 import BeautifulSoup
import json


def scrape_article(url, article_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    main_container = soup.find('main-container')
    article_text_div = soup.find('div', class_='article-text')
    article_body = soup.find('section', class_='article-body')

    if article_type in ("yle", "iltasanomat"):
        paragraphs = article.find_all('p') if article else []
    elif article_type == "hs":
        if article_body:
            summary_div = article_body.find('div', class_='summary')
            if summary_div:
                summary_div.decompose()
            paragraphs = article_body.find_all('p')
        else:
            paragraphs = []
    elif article_type == "iltalehti":
        paragraphs = main_container.find_all('p') if main_container else []
    else:
        paragraphs = article_text_div.find_all('p') if article_text_div else []

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
        "https://www.hs.fi/talous/art-2000011190019.html",
        "https://www.hs.fi/maailma/art-2000011191033.html",
        "https://www.hs.fi/talous/art-2000011188521.html",
        "https://www.hs.fi/tiede/art-2000011141875.html",
        "https://www.hs.fi/politiikka/art-2000011167461.html",
        "https://www.hs.fi/helsinki/art-2000011186533.html",
        "https://www.hs.fi/ruoka/art-2000010825843.html",
        "https://www.hs.fi/suomi/art-2000011189884.html",
        "https://www.hs.fi/helsinki/art-2000011187112.html",
        "https://www.hs.fi/politiikka/art-2000011188632.html",
        "https://www.hs.fi/urheilu/art-2000011186175.html",
        "https://www.hs.fi/pkseutu/art-2000011190722.html"
    ],
    [
        "Norjan öljyrahaston tuotot laskivat 35 miljardia euroa vuoden ensimmäisellä neljänneksellä. Rahaston varoista yli puolet on sijoitettu Yhdysvaltoihin, ja kauppasota on vaikuttanut sijoitusten arvoon. Toimitusjohtaja Nicolai Tangen rauhoittelee tilannetta ja uskoo amerikkalais­yhtiöiden olevan hyviä pitkän aikavälin sijoituksia. Norjassa pelätään Yhdysvaltojen voivan takavarikoida rahaston varoja tai painostaa epäedullisiin sijoituksiin.",
        "Yhdysvaltojen presidentti Donald Trumpin verkkokauppa myy Trump 2028 -tuotteita, vaikka perustuslaki estää kolmannen kauden. Trumpin kampanja vihjaa, että säännöt ovat muutettavissa, ja myy lippiksiä tekstillä 'Kirjoita säännöt uusiksi Trump 2028 -hatulla'. Asiantuntijoiden mukaan kyse on epäilyksen kylvämisestä perustuslakia kohtaan, eikä kolmas kausi ole mahdollinen.",
        "Valtiovarainministeri Riikka Purra ilmoitti somevaikuttajien osinkoverotuksen minimointikeinojen estämisestä. Somevaikuttaja Natalia Salmela pitää hallituksen veropäätöksiä absurdeina ja populistisina. Salmela hyötyy yhteisöveron alennuksesta, vaikka 'massimuijien' verokikkailu lopetetaan.",
        "Lasten tiedekysymyksissä pohditaan, mitä tapahtuisi, jos mikään ei maksaisi mitään. Taloushistorian professori Jari Eloranta selittää, että nyky-yhteiskunta perustuu rahan käyttöön. Jos kaikki olisi kaupoissa ilmaista, lopulta niissä ei olisi mitään tarjolla. Psykologian professori Marko Elovainio puolestaan pohtii, voiko toista ihmistä koskaan täysin tuntea. Vaikka läheisten ihmisten toimintaa oppii arvaamaan ennalta, koskaan ei voi tietää varmasti, mitä toinen tuntee tai ajattelee tai miten hän toimii.",
        "Teollisuusliiton puheenjohtaja Riku Aalto sanoo työmarkkinoiden olevan rikki, koska työnantajapuoli on unohtanut osapuolten yhteisen edun. Aallon mielestä työnantajapuoli koordinoi eri alojen neuvotteluita liian tiukasti eikä vaikuta enää välittävän lakkojen aiheuttamasta haitasta. Aallon mukaan ammattiyhdistysliikkeen pitää muuttaa tapaa, jolla lakkoja kohdennetaan. Laajojen lakkojen sijaan pitää hänen mukaansa pyrkiä katkomaan tuotantoketjuja täsmälakoilla. 60 vuotta täyttävä Aalto sanoo, ettei aio pyrkiä eduskuntaan vuonna 2027.",
        "Jarmo Asikainen ja hänen ystävänsä hyppäävät joka vuosi vappupäivänä mereen Helsingin Kaivopuistossa ylioppilaslakeissa. Perinne alkoi 1980-luvulla Sakari Salmisen ideasta ja on jatkunut vuosittain noin 10-13 hengen voimin. Vuonna 2017 perustettiin yhdistys Ullanlinnan iloiset Wappu-uimarit ry vaalimaan perinnettä ja edistämään terveyttä ja kulttuuria.",
        "Ravintolatason lihapullia varten taikina kannattaa sekoittaa sileäksi tehosekoittimessa ja pyöritellä samankokoisiksi palloiksi. Koostumuksen parantamiseksi korppujauhot kannattaa turvottaa kermassa. Taikinan kannattaa antaa viilentyä vartin verran jääkaapissa ja kädet kostuttaa kylmällä vedellä ennen pyörittämistä.",
        "Suomen evankelis-luterilainen kirkko kertoo, että hallituksen lisäleikkaukset uhkaavat sen kykyä järjestää hautaustoimea. Hallitus aikoo vähentää kirkon rahoitusta 10 miljoonaa euroa vuosina 2026 ja 2027. Kirkolliskokouksessa keskustellaan toukokuussa hautaustoimesta luopumisesta ja sen siirtämisestä hyvinvointialueille.",
        "Helsingin Roihuvuoren kirsikkapuut ovat lähellä täyttä kukintaa, kertoo kaupungin puuasiantuntija Juha Raisio. Hanami-juhla eli kirsikankukkajuhla järjestetään vasta kahden viikon kuluttua. Tänä vuonna järjestetään uutuutena yöhanami eli Yozakura, jossa valaistuja kirsikkapuita voi ihailla yöaikaan. Kukinnan runsautta Roihuvuoressa heikentää tammikuussa tehty puiden virheellinen leikkaus, joka vaikuttaa noin kahteen kolmasosaan puista.",
        "Hallituksen veronkevennysten dynaamiset vaikutukset ovat liian optimistisia, sanovat professorit Roope Uusitalo ja Kaisa Kotakorpi. Veronalennukset voivat kasvattaa julkista velkaa, sillä tutkimusnäyttö niiden talouskasvua kiihdyttävistä vaikutuksista on epävarmaa. Hallitus keventää verotusta kahdella miljardilla eurolla ja paikkaa syntyvää vajetta Valtion eläkerahastosta otettavalla miljardilainalla.",
        "Digita oy:n Antero-tv-palvelu sulkeutuu 31. toukokuuta vaikuttaen tuhansiin maksu-tv-asiakkaisiin antennitalouksissa. Palvelulla on ollut yli 20 000 tilaajaa, joista monet ovat iäkkäitä lineaarisen television katsojia. Lopetuksen syynä on sisältöjen jälleenmyynnin kannattamattomuus.",
        "Jorvin sairaalan päivystys Espoossa suljettiin torstaina pariksi tunniksi tuhkarokkoepäilyn vuoksi. Länsi-Uudenmaan hyvinvointialueen viestintäpäällikkö Eliisa Anttila vahvisti, että sairaalassa oli tuhkarokkoepäily. Päivystyksen asiakkaat joutuivat odottamaan ulkopuolella ja tilat desifioitiin ennen uudelleen avaamista."]
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
