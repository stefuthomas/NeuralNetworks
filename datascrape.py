import requests
from bs4 import BeautifulSoup
import json


def scrape_article(url, article_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('article')
    main_container = soup.find('div', class_='main-container')
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
        "https://www.hs.fi/pkseutu/art-2000011190722.html",
        "https://www.hs.fi/maailma/art-2000011196315.html",
        "https://www.hs.fi/helsinki/art-2000011196101.html",
        "https://www.hs.fi/helsinki/art-2000011194813.html",
        "https://www.hs.fi/politiikka/art-2000011198105.html",
        "https://www.hs.fi/tiede/art-2000011196351.html",
        "https://www.hs.fi/maailma/art-2000011198669.html",
        "https://www.hs.fi/kulttuuri/art-2000011197723.html",
        "https://www.hs.fi/tiede/art-2000011191008.html"

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
        "Jorvin sairaalan päivystys Espoossa suljettiin torstaina pariksi tunniksi tuhkarokkoepäilyn vuoksi. Länsi-Uudenmaan hyvinvointialueen viestintäpäällikkö Eliisa Anttila vahvisti, että sairaalassa oli tuhkarokkoepäily. Päivystyksen asiakkaat joutuivat odottamaan ulkopuolella ja tilat desifioitiin ennen uudelleen avaamista.",
        "Donald Trump ja Volodymyr Zelenskyi tapasivat Vatikaanissa ennen paavi Franciscuksen hautajaisia. Poliittisen viestinnän tutkija Elisa Kannasto arvioi tapaamisen olleen tietoisesti rakennettu. Trump torjui elekielellään Ranskan presidentin Emmanuel Macronin ja keskittyi kahdenkeskiseen tapaamiseen Zelenskyin kanssa.",
        "Vuosaaren metroliikenne katkeaa viideksi kuukaudeksi 5. toukokuuta alkaen metrosillan peruskorjauksen vuoksi. Yli 31 000 päivittäistä matkustajaa korvataan tiheällä bussilinjalla 99V Vuosaaren ja Itäkeskuksen välillä. Samalla Vuosaaren ja Rastilan metroasemilla tehdään remonttia ja uudistetaan teknisiä järjestelmiä.",
        "Monet ravintolat pääkaupunkiseudulla kieltävät sisäänpääsyn opiskelijahaalareissa liiketoiminnan kannattavuuden vuoksi.  Helsinkiläisen Bierhaus München -olutravintolan ravintolapäällikkö Simo Kärki kertoo opiskelijoiden ostavan vähän ja vievän tilaa maksavilta asiakkailta.  Metropolia-ammattikorkeakoulun opiskelijat ymmärtävät haalarikiellon, sillä suuret opiskelijaryhmät häiritsevät muita asiakkaita erityisesti viikonloppuisin.",
        "Kansanedustaja Päivi Räsänen (kd) kritisoi Alkon suunnitelmaa myydä vanhenevia alkoholituotteita alennettuun hintaan.  Räsänen pitää parempana vanhentuneiden juomien hävittämistä kuin myymistä alennettuun hintaan.  Alko aloitti maanantaina kokeilun, jossa poistotuotteita myydään 20 prosentin alennuksella kolmessa Tampereen myymälässä.",
        "Juttelevan botin ohjelmia voidaan käyttää myös salattuihin viesteihin. Viesti voidaan piilottaa arkisen keskustelun lomaan. Oslon yliopiston tekoälyn tutkija kehitti ohjelman, joka upottaa salattuja viestejä tekoälyn keskusteluihin. Salattu viesti toistuu jaksoissa. Menetelmä voisi auttaa viestimään maissa, joissa yksilö kokee sortoa ja haluaa salata viestinsä.",
        "Britannian NHS ryhtyy tutkimaan sukupuolenkorjausta haluavat alaikäiset autismin ja adhd:n varalta. Uudet sukupuoli-identiteettiklinikat korvaavat Tavistockin klinikan, jonka hoitojen epäillään vahingoittaneen potilaita. Lastenlääkäri Hilary Cass korostaa, että ahdistuneet lapset tulee nähdä kokonaisina ihmisinä.",
        "Detroitin oopperassa esitetään teos viidestä syyttömänä tuomitusta newyorkilaisnuoresta vuoden 1989 raiskauksessa. Presidentti Donald Trump vaati aikoinaan kuolemantuomiota nuorille ja pitää heitä edelleen syyllisinä todisteiden vastaisesti. Oopperan tekijät ovat varautuneet Trumpin hallinnon mahdollisiin vastatoimiin esityksen vuoksi.",
        "Tutkijat ovat selvittäneet muinaisen Deinosuchuksen kehittymistä. Communications Biology -lehdessä kerrotaan, että Deinosuchuksella oli suolarauhasia, kuten nykykrokotiileilla. Suolaveden sietäminen mahdollisti Deinosuchuksen leviämisen laajalle alueelle ja kasvamisen valtavaksi."
    ]
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
        "https://www.iltalehti.fi/kuninkaalliset/a/7369dde1-9349-4ce1-8788-1c35bf19514f",
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
        "https://www.mtvuutiset.fi/artikkeli/nyt-se-on-varmaa-ville-peltoselle-potkut/9143752",
        "https://www.mtvuutiset.fi/artikkeli/erika-vikman-tekee-paljastuksen-uudesta-viisuvaatetuksestaan-maailmanluokan-asu/9143654",
        "https://www.mtvuutiset.fi/artikkeli/trump-venaja-tehnyt-isoja-myonnytyksia/9143508",
        "https://www.mtvuutiset.fi/artikkeli/trumpin-vihjailu-kolmannesta-kaudesta-yltyy-myynnissa-hammastyttava-tuote/9143602",
        "https://www.mtvuutiset.fi/artikkeli/suomalaisopiskelija-aku-seuraa-aitiopaikalta-trumpin-harvard-hyokkaysta-pelottava-tilanne/9143368",
        "https://www.mtvuutiset.fi/artikkeli/suomalaisyritykset-ovat-puhuneet-murskaluku-kertoo-paljon-luottamuksesta-usa-an/9143634",
        "https://www.mtvuutiset.fi/artikkeli/paavin-ruumista-kaynyt-katsomassa-yli-128-000-ihmista/9143636",
        "https://www.mtvuutiset.fi/artikkeli/cbs-lavrov-sanoi-venajan-olevan-valmis-sopimukseen-yhdysvaltojen-kanssa-tiettyja-elementteja-jotka-vaativat-hienosaatoa/9143652",
        "https://www.mtvuutiset.fi/artikkeli/venajan-ammusvaraston-rajahdys-nakyi-sysmassa/9143734",
        "https://www.mtvuutiset.fi/artikkeli/kuukausiennuste-kesa-nakyvissa/9143612",
        "https://www.mtvuutiset.fi/artikkeli/kristen-stewartin-intiimit-haakuvat-julki/9143542",
        "https://www.mtvuutiset.fi/artikkeli/yokylassa-maria-veitola-jatkuu-juhlakauden-merkeissa/9143326",
        "https://www.mtvuutiset.fi/artikkeli/seiska-erika-vikman-on-eronnut/9131098",
        "https://www.mtvuutiset.fi/artikkeli/gasellit-yhtyeelta-yllatysilmoitus/9143598",
        "https://www.mtvuutiset.fi/artikkeli/sorrutko-tahan-harhaluuloon-punkeista-valitettavasti-niin-ei-ole/9143272",
        "https://www.mtvuutiset.fi/artikkeli/tassa-ovat-love-island-suomi-sinkut/9124560",
        "https://www.mtvuutiset.fi/artikkeli/toimittaja-ida-kukkapuron-aiti-on-myos-hanen-siskonsa-se-oli-kaytannon-jarjestely/9135810",
        "https://www.mtvuutiset.fi/artikkeli/veera-jarkyttyi-iphonen-kuvahaun-tuloksesta-lihavuusstigma-on-terveysriski-johon-ministeriokin-nyt-puuttuu/9139542",
        "https://www.mtvuutiset.fi/artikkeli/asiantuntija-varoittaa-mokkihajusta-vaatteissa-monesti-viite-siita-etta-jotain-on-pielessa/9139652"
    ],
    [
        "Donald Trump on vihjaillut olevansa avoin kolmannelle presidenttikaudelle.",
        "Helsingin IFK on vapauttanut päävalmentaja Ville Peltosen sekä apuvalmentajat Samuel Tilkasen ja Marko Ojasen tehtävistään. Peltosen alaisuudessa HIFK:n paras saavutus oli neljäs sija, mutta kolmesti joukkue putosi jo puolivälierissä. Kannattajat vaativat Peltosen eroa jo kauden aikana, erityisesti SaiPa-sarjan aikana. Seura tiedotti asiasta perjantaina.",
        "Erika Vikman valmistautuu edustamaan Suomea Baselin Euroviisuissa kappaleellaan Ich komme, ja hänen esiintymisasunsa on parhaillaan työn alla. Muotisuunnittelija Anna Sarasojan suunnittelema asu on Vikmanin mukaan maailmanluokan luomus, jossa on paljon asennetta. Euroopan yleisradiounioni EBU on kuitenkin toivonut asuun muutoksia sen seksuaalisen sävyn vuoksi, erityisesti takapuolen peittämistä, mutta Vikman vakuuttaa, ettei tämä hidasta hänen menoaan. Ainoana yksityiskohtana hän paljastaa, että asussa on mustaa nahkaa.",
        "Yhdysvaltain presidentti Donald Trump väittää painostavansa Venäjää lopettamaan sodan Ukrainassa ja pitää Venäjän päätöstä olla valtaamatta koko maata suurena myönnytyksenä. Trumpin mukaan Venäjä on valmis sopimukseen, mutta Ukrainan kanssa neuvottelut ovat olleet vaikeampia. Naton pääsihteeri Mark Rutte korostaa, että neuvottelupallo on nyt Venäjällä, ja pitää maata pitkän aikavälin uhkana euroatlanttiselle alueelle. Samaan aikaan Venäjä teki mittavan ilmaiskun Kiovaan, jossa kuoli ainakin 12 ihmistä ja loukkaantui yli 90, mikä herätti Trumpin kritiikin Putinin suuntaan.",
        "Donald Trump on jälleen vihjannut mahdollisuudesta kolmannelle presidenttikaudelle, vaikka Yhdysvaltain perustuslaki sallii vain kaksi kautta. Hänen verkkokauppaansa on ilmestynyt myyntiin punainen Trump2028-lippalakki, jonka mainoskuvissa esiintyy hänen poikansa Eric Trump. Trump on aiemmin ehdottanut strategiaa, jossa hän toimisi varapresidenttinä ja nousisi presidentiksi, jos valittu presidentti eroaisi. Tällaiset vihjailut ovat herättäneet huolta hänen pyrkimyksistään kiertää perustuslaillisia rajoituksia.",
        "Suomalaisyritysten luottamus Yhdysvaltoihin on heikentynyt merkittävästi, mikä näkyy vientilukujen laskuna. Yritykset ovat huolissaan poliittisista jännitteistä ja kauppasuhteiden epävarmuudesta.",
        "Pietarinkirkossa esillä olevaa paavi Franciscuksen ruumista on käynyt katsomassa yli 128 000 ihmistä. Hautajaiset pidetään lauantaina, ja paikalle odotetaan lukuisia valtionpäämiehiä ja monarkkeja.",
        "Venäjän ulkoministeri Sergei Lavrov ilmoitti, että Venäjä on valmis tekemään sopimuksen Yhdysvaltojen kanssa Ukrainan sodan lopettamiseksi. Hän kuitenkin totesi, että jotkin sopimuksen yksityiskohdat vaativat vielä hienosäätöä.",
        "Venäjällä Kirzhatshskissa tapahtunut suuri ammusvaraston räjähdys havaittiin myös Suomessa, muun muassa Sysmässä ja Kangasniemellä. Seismologian instituutin mukaan räjähdyksen voimakkuus oli Suomessa 3,2–3,4. Räjähdyksessä tuhoutui yli 100 000 tonnia sotatarvikkeita.",
        "Vaikka vappuviikolla voi esiintyä vielä viileitä jaksoja, kuukausiennuste ennustaa keski- ja eteläiseen Suomeen keskimääräistä lämpimämpää säätä toukokuun aikana. Kesäiset lämpötilat voivat saapua jo toukokuun puolivälin jälkeen.",
        "Näyttelijä Kristen Stewart ja Dylan Meyer avioituivat Meksikossa 20. huhtikuuta. Meyer jakoi sosiaalisessa mediassa intiimejä kuvia seremoniasta, jossa pariskunta juhli läheisten ystävien ja perheen kanssa.",
        "Maria Veitolan suosittu ohjelma Yökylässä Maria Veitola palaa ruutuihin juhlistaen 10. tuotantokauttaan. Uudella kaudella Veitola vierailee jälleen tunnettujen suomalaisten kodeissa intiimien keskustelujen merkeissä.",
        "Artisti Erika Vikman on eronnut pohjanmaalaisesta lääkärimiehestään, jonka kanssa hän seurusteli parin vuoden ajan. Vikman kertoo eron olevan jo käsitelty ja molempien jatkaneen eteenpäin elämässään.",
        "Rap-yhtye Gasellit ilmoitti jäävänsä parin vuoden keikkatauolle syksyllä 2025. Ennen taukoa yhtye kiertää Suomea 26 keikan verran toukokuusta syyskuuhun.",
        "Punkkikausi on alkanut vilkkaasti, ja havaintoja on tehty jo yli 13 000 kertaa. Puutiaisia esiintyy yhä enemmän myös kaupunkien puistoissa, eikä niiden levinneisyys rajoitu enää vain maaseudulle. Ilmaston lämpeneminen on laajentanut punkkien esiintymisalueita pohjoisemmaksi. Pureman jälkeen punkki tulisi poistaa heti, ja borrelioosin sekä puutiaisaivokuumeen riski on hyvä tiedostaa.",
        "Love Island Suomi palaa viidennellä tuotantokaudellaan, ja mukana on kymmenen uutta sinkkua, kuten muusikko Benjamin ja thainyrkkeilijä Emma. Ohjelmassa seurataan heidän ihmissuhteitaan, parinvalintojaan ja mahdollisia romansseja. Katsojat voivat vaikuttaa tapahtumiin äänestämällä, ja kauden lopuksi valitaan voittajapari.",
        "Toimittaja-kirjailija Ida Kukkapuron isovanhemmat adoptoivat hänet alle 10-vuotiaana, jolloin hänen biologisesta äidistään tuli juridisesti hänen siskonsa. Kukkapuro kertoo, että järjestely oli käytännön ratkaisu, eikä se vaikuttanut hänen arkeensa merkittävästi. Hän käsittelee aihetta esikoiskirjassaan Sisaruuksia.",
        "Somevaikuttaja Veera Bianca huomasi, että iPhonen kuvahaku näytti hakusanalla valas kuvia hänestä, mutta ei hoikemmasta ystävästään. Tapaus nosti esiin tekoälyn mahdollisen lihavuusstigman, johon sosiaali- ja terveysministeriökin aikoo puuttua.",
        "Rakennusterveysasiantuntija Riikka Hopealinna varoittaa, että mökiltä palaamisen jälkeen vaatteisiin jäävä tunkkainen haju voi viitata sisäilmaongelmiin, kuten mikrobikasvustoon tai pieneläinten aiheuttamiin epäpuhtauksiin. Säännöllinen ilmanvaihto ja huolellinen huolto ovat avainasemassa ongelmien ehkäisyssä."
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
