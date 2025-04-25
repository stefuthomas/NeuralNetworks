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
    [

    ],
    [

    ]
)]

articles += [(url, summary, "iltalehti") for url, summary in zip(
    [
        "https://www.iltalehti.fi/smliiga/a/a66d4fda-09ca-462e-9898-7c3c5e028f43",
        "https://www.iltalehti.fi/ulkomaat/a/73a46709-9483-4d82-8b5a-41fe2ebf989d",
        "https://www.iltalehti.fi/kotimaa/a/5ea75a41-4794-4910-9f04-e66357b18db3",
        "https://www.iltalehti.fi/digiuutiset/a/2ba5bc21-7f57-4782-8ff6-575fc2b3a0da",
        "https://www.iltalehti.fi/tyoelama/a/4c6bf02f-7af2-4dbb-b61f-c694f79f1fa4",
        "https://www.iltalehti.fi/tyoelama/a/0ef79e43-817a-4a9a-8ed9-7140c92aef94",
        "https://www.iltalehti.fi/talviurheilu/a/d7aa5e1e-4431-4908-b9e1-a4b1ad05e2cb",
        "https://www.iltalehti.fi/ralli/a/325d4338-dd3f-436d-90d7-aa3ad5049407",
        "https://www.iltalehti.fi/muutlajit/a/a113147e-1208-40e7-bbc4-56d34742eaf2",
        "https://www.iltalehti.fi/jalkapallo/a/25044916-0fb6-4ffa-a342-3f76e53ebf9e",
        "https://www.iltalehti.fi/politiikka/a/efbfb170-e939-4c1a-bc27-eeba47a16601",
        "https://www.iltalehti.fi/viihdeuutiset/a/09ab2395-5863-41e9-803a-51e79aab154f",
        "https://www.iltalehti.fi/kuninkaalliset/a/0416469e-9b88-4bd1-b063-bbac3023d5bb",
        "https://www.iltalehti.fi/viihdeuutiset/a/e0af5cc7-af8b-424f-a7f4-f0e2195e517b",
        "https://www.iltalehti.fi/viihdeuutiset/a/dcc1383b-1479-4d45-b8ae-8cfd94300907",
        "https://www.iltalehti.fi/viihdeuutiset/a/3a562eca-bdd6-4d38-89b6-0edad4cd9a7c",
        "https://www.iltalehti.fi/viihdeuutiset/a/0ef230a8-da6d-417c-b983-12c9279f9c2f",
        "https://www.iltalehti.fi/tv-ja-leffat/a/e2a217e3-8f5b-4acc-a339-96288821fb3b",
        "https://www.iltalehti.fi/kuninkaalliset/a/23cc97f3-8e54-4f7c-9d8b-fdab382f468c",
        "https://www.iltalehti.fi/kuninkaalliset/a/7369dde1-9349-4ce1-8788-1c35bf19514f"
    ],
    [
                "Ville Peltonen on saanut potkut HIFK:n päävalmentajan tehtävästä kesken sopimuskauden heikkojen tulosten vuoksi, eikä myöskään valmennustiimin jäsenet Samuel Tilkanen ja Marko Ojanen jatka. HIFK-legendan nelivuotinen valmennusjakso toi vain yhden välieräpaikan ilman mitaleita, ja fanit ovat olleet pettyneitä. Samalla myös seuran toimitusjohtaja Alexander Sneen jättää tehtävänsä, mikä liittyy kauden jälkeiseen kohuun, jossa opiskelijahierojat kertoivat kokeneensa epäasiallista kohtelua IFK:ssa.",
        "Britannia on vetäytymässä suunnitelmastaan lähettää tuhansia joukkoja Ukrainaan vartioimaan keskeisiä kohteita, ja aikoo sen sijaan keskittyä Ukrainan armeijan kouluttamiseen ja aseistamiseen. Lähteiden mukaan brittien ja ranskalaisten kouluttajat sijoitettaisiin Länsi-Ukrainaan kauas etulinjasta. Taustalla on eroavaisuus Britannian varovaisemman ja Ranskan voimakkaamman lähestymistavan välillä. Samaan aikaan britti- ja ranskalaistahot yrittävät saada Donald Trumpin ja presidentti Zelenskyin tapaamaan Roomassa paavi Franciscuksen hautajaisten yhteydessä rauhanedistämiseksi.",
        "Hallitus aikoo poistaa työsuhdepyörien verovapauden vuoden 2026 alusta, mikä uhkaa romahduttaa suositun edun synnyttämän alan ja vaarantaa tuhansia työpaikkoja. Yli 100 000 suomalaista on hankkinut työsuhdepyörän, ja useat alan toimijat sekä kansanedustajat ovat kritisoineet päätöstä voimakkaasti. Muoti- ja urheilukauppa ry:n mukaan veroton pyöräetu on tuottanut enemmän verotuloja kuin sen poistolla aiotaan saada, ja esityksen pelätään johtavan konkursseihin erityisesti pyöräliikkeissä. Päätöstä pidetään ristiriitaisena hallituksen ilmasto- ja terveyspoliittisten tavoitteiden kanssa.",
        "Kyberturvallisuuskeskus varoittaa S-pankin nimissä liikkuvista huijausviesteistä, joissa kehotetaan päivittämään käyttäjätietoja ja ohjataan huijaussivustolle. Sivustolla kalastellaan pankkitunnuksia, ja niiden päätyessä rikollisille tilin voi menettää nopeasti. Äskettäin uhri menetti 86 000 euroa vastaavassa huijauksessa, eikä pankki ollut korvausvelvollinen.",
        "Rakennusalan yksinyrittäjä Antti Kiili on tyytyväinen päätökseensä siirtyä yrittäjäksi ja on saavuttanut noin 150 000 euron vuotuisen liikevaihdon ilman markkinointibudjettia. Kiili vakuutti yrityksensä kattavasti Fennialla, ja kehuu saamaansa palvelua erinomaiseksi. Fennia tarjoaa yksinyrittäjille oman verkkosivuston ja palvelun, joka auttaa kartoittamaan vakuutustarpeet helposti ja nopeasti.",
        "Työttömäksi jääminen voi aiheuttaa voimakkaita tunteita, mutta niiden käsittely ja keskustelu läheisten kanssa helpottavat tilannetta. MIELI ry:n asiantuntija kannustaa näkemään muutoksen mahdollisuutena ja hyödyntämään aiempia selviytymiskokemuksia. Työttömän ensiapupaketti tarjoaa tietoa työnhausta, taloudesta ja mielenterveydestä. Työnantajat eivät etsi täydellisiä ihmisiä, vaan motivoituneita ja sopivia työntekijöitä.",
        "Pekka Hyysalo koki ikävän tilanteen helsinkiläisessä ravintolassa, kun hänet käännytettiin ovelta ilman keskustelua ja sai kuulla, ettei hänelle tarjoilla. Vaikka tilanne nostatti voimakkaita tunteita, Hyysalo pohti jälkeenpäin, miten olisi itse voinut reagoida rauhallisemmin ja vaikuttaa tilanteeseen rakentavasti. Hän korosti some-päivityksessään, ettei halua syyllistää ketään vaan muistuttaa, että asiat eivät aina ole siltä miltä näyttävät, ja että vuorovaikutus on tärkeää.",
        "Kalle Rovanperä aloitti Kanarian MM-rallin huimassa vireessä ja otti johdon heti ensimmäisellä erikoiskokeella, jättäen tallikaverinsa Elfyn Evansin 6,5 sekunnin päähän. Toisella pätkällä hän kasvatti etumatkaansa entisestään Sébastien Ogieriin, ja johtaa nyt rallia 15,8 sekunnilla. Rovanperä on tyytyväinen suoritukseensa sumuisista olosuhteista huolimatta ja aikoo jatkaa samalla linjalla. Myös Sami Pajari onnistui nousemaan viidenneksi ohittaen Ott Tänakin.",
        "Suomen tyttöjen cheerleading-maajoukkue voitti MM-kultaa Orlandossa, jättäen Yhdysvallat toiseksi ja Ruotsin kolmanneksi. Joukkue sai finaalista 89,64 pistettä, ja kapteeni Saga Ingström iloitsee pitkän työn palkinnosta. Tämä on Suomelle toinen maailmanmestaruus cheerleadingin juniorisarjassa. Myös Suomen naisten, sekacheer- ja cheertanssimaajoukkueet ylsivät finaaliin.",
        "Bayern Münchenin pelaaja Michael Olise kiinnitti huomiota hurjalla ylinopeudellaan, ajettuaan 72 km/h alueella, jossa raja on 30 km/h. Myös muut pelaajat, kuten Leroy Sané ja Raphaël Guerreiro, ovat sortuneet ylinopeuksiin. Vaikka nopeudet eivät tallentuneet virallisiin kameroihin eikä seurauksia ole vielä tullut, Münchenin poliisi ja lakimies arvioivat, että alueen nopeusvalvontaa tullaan tiukentamaan. Olise on suoriutunut erinomaisesti debyyttikaudellaan Bayernin paidassa, tehden kahdeksan maalia ja syöttäen 11 kertaa.",
        "Kansanedustaja Teemu Keskisarja esitti eduskunnassa Yle kuriin nyt! -kansalaisaloitteen hyväksymistä, mikä aiheutti kohua perussuomalaisten sisällä, sillä aloite ei saanut tukea omilta puoluekavereilta. Keskisarja oli pettynyt, sillä hän oli saanut aiemmin tukea somessa, mutta eduskunnassa kukaan ei ilmaissut kannatustaan. Ryhmän puheenjohtaja Jani Mäkelä selitti, että perussuomalaiset eivät hyväksyneet aloitetta, koska Yleisradion taloussopeutukset ovat jo käynnissä ja lainsäädäntöä valmistellaan. Keskisarja epäili, että hänelle tulee seurauksia linjauksestaan.",
        "Mikko Koivu on haastanut entisen vaimonsa Helena Koivun oikeuteen lasten huoltajuuteen liittyvissä asioissa, kuten elatusapua, tapaamista ja asumista koskien. Erilaiset oikeuskiistat, mukaan lukien omaisuudenjako Suomessa ja Yhdysvalloissa, ovat jatkuneet eron jälkeen, ja viime aikoina ex-pari on riidellyt Kakskerran kiinteistön omistajuudesta. Viime viikolla poliisit kävivät hakemassa Helena Koivun pois tontilta, ja asiasta on suunnitteilla istunto kesäkuussa.",
        "Meghan ja prinssi Harry edustivat yhdessä ensimmäistä kertaa kuukausiin Time100-tilaisuudessa New Yorkissa. Meghan puhui muun muassa Netflix-sarjastaan ja kertoi olevansa onnellisempi kuin koskaan. Hänen asusteensa sisälsi kunnianosoituksen Harryn äidille, prinsessa Dianalle, sillä Meghanin ranteessa oli Dianan omistama Cartier Tank Française -kello. Meghan ja Harry ovat äskettäin joutuneet kohuihin, joissa on väitetty heidän elämänsä olevan kriisissä.",
        "Korson seurakunta järjestää saunakirkon 13. toukokuuta KAJ-yhtyeen Euroviisukappaleen innoittamana. Kirkossa on oma sauna, ja tilaisuuteen osallistuvat pukeutuvat uimapukuihin ja pyyhkeisiin. Tapahtumassa yhdistetään saunominen ja hartaushetki, ja tilaisuuden tuotto menee Yhteisvastuukeräykseen. Kirkkoherra Tuomas Antola pitää saunaa pyhänä paikkana, ja tapahtuma on saanut osakseen kiinnostusta erityisesti saunateeman vuoksi.",
        "Rodeo-yhtye, joka herätti huomiota esiintymisellään Linnan juhlia seuranneilla jatkoilla, on saanut osakseen kritiikkiä, erityisesti sen nopeasta noususta ja suuresta näkyvyydestä. Yhtyeen jäsenet, Anna Puu, Ida Paul ja Erin, puolustavat itseään Ylen haastattelussa, kritisoiden muun muassa median roolia ja ihmisten reaktioita, joita he kokevat usein perustuvan juoruihin ja mielikuvien luomiseen. Yhtye, joka julkaisi debyyttisingelnsä syksyllä 2024, kokee, että erityisesti naisten yhdessä esiintyminen herättää voimakasta ärsytystä.",
        "Bianca Censori, joka tunnetaan provokatiivisista pukeutumisistaan, bongattiin hiljattain Mallorcalla pukeutuneena erittäin paljastavaan mustaan bodyyn ja sukkahousuihin. Censori on ollut myös uutisissa, sillä hän ja räppäri Kanye West väitetysti palasivat yhteen sen jälkeen, kun he olivat aiemmin eronneet. Hänen asustaan on kommentoitu, että se koettelee säädyllisen pukeutumisen rajoja, vaikka Espanjassa ei ole tarkkaa pukeutumiskoodia.",
        "Laulaja Isaac Sene on hämmentänyt seuraajiaan julkaisemalla TikTokissa videon, jossa hän ja nuori nainen suutelevat ja vietetään aikaa yhdessä maalaismaisemassa. Videon yhteydessä Sene jakoi tunteikkaan viestin, jossa hän kertoo tunteistaan naiselle, ja someseuraajat ovat arvuutelleet, onko kyseessä uusi suhde vai vain musiikkivideo. Sene oli aiemmin mukana suhdehuhujen keskellä, kun hän tanssi Tanssii tähtien kanssa -kilpailussa Kastanja Rauhalan kanssa, mutta molemmat ovat pitäytyneet yksityiselämänsä yksityisinä.",
        "Entinen lapsinäyttelijä Sophie Nyweide kuoli 24-vuotiaana epäselvissä olosuhteissa, ja kuolinsyyntutkinta on edelleen kesken. Poliisi tutkii kuolemaa mahdollisena tahattomana yliannostuksena, mutta henkirikoksen mahdollisuus on myös avoinna. Nyweide löydettiin kuolleena joen rannalta Vermontista, ja hänen äitinsä kertoi, että tytär oli käyttänyt huumeita ja oli kuollessaan muiden seurassa. Nyweide tunnettiin rooleistaan elokuvissa kuten 'Noah' ja 'Mammoth', ja hänen viimeinen näyttelijäntyönsä oli vuonna 2015.",
        "Ruotsin kuningas Kaarle Kustaa ja kuningatar Silvia osallistuivat torstaina prinssi Andreaksen hautajaisiin Saksassa. Kuningatar Silvia tukeutui kävelykeppiin, koska hän oli aiemmin huhtikuussa käynyt leikkauksessa vaivaisenluun vuoksi. Hautajaisiin osallistuivat myös prinsessa Madeleine, Chris O'Neill ja prinsessa Christina. Kuningatar ja kuningas osallistuvat myös paavi Franciscuksen hautajaisiin Vatikaanissa lauantaina.",
        "Ruotsin kruununprinsessa Victoria vierailee parhaillaan Suomessa, ja hän osallistui keskiviikkoaamuna Hanasaaren kulttuurikeskuksessa konferenssiin. Victoria pukeutui Suomen väreihin sähkönsiniseen housupukuun, ja asun kruunasi Kalevalan Naisen ääni -rintakoru, joka symboloi tasa-arvoa. Korua on aiemmin nähty Victorialla useilla valtiovierailuilla, ja tällä kertaa se oli osa hänen Suomi-teemaa. Vierailun teemoihin kuuluu Suomen yksityisen ja julkisen sektorin yhteistyö huoltovarmuuden alalla."

    ]
)]

articles += [(url, summary, "mtv") for url, summary in zip(
    [
        "https://www.mtvuutiset.fi/artikkeli/trumpin-vihjailu-kolmannesta-kaudesta-yltyy-myynnissa-hammastyttava-tuote/9143602",
        "https://www.mtvuutiset.fi/artikkeli/nyt-se-on-varmaa-ville-peltoselle-potkut/9143752"
    ],
    [

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
