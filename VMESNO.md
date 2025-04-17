## Kje danes kolesarim? 
#### Geografska analiza rekreativnega kolesarjenja v Sloveniji

---

**Problem**

Cilj projekta je analiza rekreativnega kolesarjenja v Sloveniji z uporabo podatkov iz aplikacije Strava. Glavni problem je pridobiti, očistiti in analizirati podatke o kolesarskih segmentih, ki so relevantni za območje Slovenije, ter iz njih izluščiti zanimive ugotovitve glede geografskega razporeda, dolžine, težavnosti in priljubljenosti segmentov.

---

**Podatki**

Podatke pridobivamo prek Strava API, ki omogoča dostop do informacij o kolesarskih segmentih. Za zajem podatkov smo razdelili območje Slovenije na mrežo pravokotnikov dveh velikosti, da zajamemo vse segmente, ki so popolnoma znotraj posameznih območij. Ta pristop omogoča zajem segmentov, tudi če prečkajo meje posameznih mrežnih celic. Skupno je bilo generiranih 495 manjših in 32 večjih celic za pridobivanje podatkov.

Pridobljeni surovi podatki so bili združeni in očiščeni, odstranjeni so bili podvojeni segmenti. Nato smo s pomočjo geojson datoteke slovenske meje izločili segmente, ki se nahajajo popolnoma zunaj Slovenije. Po čiščenju je ostalo 1526 unikatnih segmentov znotraj Slovenije.

Segmentom smo zbrisali za nadaljno analizo nepotrebne atribute in izračunali dodatne, po lastni presoji. Glavni povdarek na spreminjanju kategorije vzponov, z namenom pridobiti lestvico relevantno za področje Slovenije in pa določanju regije oz. občine, kateri segment pripada (ključno za nadaljno prostorsko analizo). Končni "čisti" podatki vsebujejo atribute:
```['id', 'name', 'activity_type', 'distance', 'average_grade', 'maximum_grade', 'elevation_high', 'elevation_low', 'start_latlng', 'end_latlng', 'elevation_profile', 'elevation_profiles', 'country', 'total_elevation_gain', 'map', 'effort_count', 'kom', 'qom', 'climb_score', 'is_flat', 'custom_climb_category', 'region']```

---

**Izvedene analize**

1. Osnovne ugotovitve:
- 1526 segmentov.
- 14874530 zabeleženih voženj na teh segmentih.
- 9747 voženj povprečno na segment.
- Večina segmentov v okolici povprečja, veliko osamelcev z visoko nadpovprečnim številom voženj, maximalno "Ruda sprint" s 128925 vožnjami.

![alt text](image.png)

2. Povezava regij oz. občin in števila voženj:
- Zaradi metode pridobivanja podatkov so ti približno enakomerno razpršeni, upoštevajoč velikost posamezne občine.
- Najbol prevožene so pričakovane občine npr. Ljubljana, Koper, Bovec, Kranjska Gora.

| Rank | Municipality     | Total Effort Count |
|------|------------------|--------------------|
| 1    | Ljubljana        | 1,033,332          |
| 2    | Koper            | 738,828            |
| 3    | Bovec            | 512,133            |
| 4    | Kranjska Gora    | 451,758            |

- Porazdelitev povprečnega števila voženj na segment (po občinah) približno eksponentno pada.

![alt text](image-1.png)

- Vizualizacija povprečnega števila voženj po posameznih slovenskih občinah nazorno prikazuje neenakomerno prostorsko porazdelitev, območje okoli glavnega mesta Ljubljane, obala, primorska ob meji z Italijo, turistično močnejši deli gorenjske in okolice mestnih občin beležijo več rekreativnega kolesarjenja, medtem ko je to v južnem, jugovzhodnem delu, na koroškem, prekmurju, ... slabše zastopano.

![alt text](image-2.png)

- Porazdelitev je sicer dokaj vzporedna porazdelitvi slovenskega prebivalstva a vseeno prikazuje območja, kjer bi bilo dobro rekreativno kolesarstvo na različne načine vzpodbujati.

3. Povezava med številom voženj in kategorijo vzpona
- Pričakovano so najbolj prevoženi ravninski segmenti in segmenti 1. kategorije (najlažji, najbolj dostopni, povezovalni).
- Pri višjih kategorijah je opazen rahel padajoč trend, vendar tudi visokokategorizirani oz. težki segmenti premorejo veliko voženj, kar lahko namiguje na naravo rekreativnih kolesarjev, ki niso le "turistični športniki" vendar se radi preizkusijo tudi na težjih izzivih.

![alt text](image-3.png)

---

**Glavne ugotovitve**

- Segmenti so razporejeni po celotni Sloveniji, kar kaže na raznolikost in dostopnost kolesarskih poti.
- Segmenti so v aplikaciji ocenjeni glede na priljubljenost (število zvezdic uporabnikov), kar omogoča identifikacijo najbolj zanimivih in pogosto voženih poti.
- Kljub enakomerni razporejenosti, segmenti niso enakomerno prevoženi kar nakazuje na različno kolesarsko aktivne regije.
- Najbolj priljubljeni so ravni oz. lahki segmenti, priljubljenost s težavnostjo pada.

---

**Uporabljena izvorna koda**

Za analizo podatkov smo uporabili Python Jupyter zvezke:

- `data_extraction.ipynb`: za pridobivanje, združevanje in čiščenje segmentov iz Strava API.
- `data_transform.ipynb`: za nadaljno urejanje podatkov, dodajanje lastnih atributov, odstranjanje nepotrebnih.
- `visualizations_analysis1.ipynb`: osnone analize in vizualizacije podatkov.
- Dodatno smo uporabili geojson datoteko slovenske meje in slovenskih občinza geografsko filtracijo segmentov.

---

**Nadaljnje delo in vprašanja**

- 10 občin nima niti enega segmenta, morebiti slabost metode pridobivanja podatkov, mogoče tam res segmentov ni. V nadaljne bi lahko cel data pipeline za pridobivanje in urejanje podatkov izvedli še enkrat, večkratni prehod območja Slovenije, na najnižjem nivoju s še manjšimi območji in več prekrivanja, da bi ulovili še več segmentov.
- Nadaljevanje analize segmenotv glede na dolžino, višinsko spremembo in najbolši čas na segmentu; računanje VAM (average ascent speed oz. povprečna hitrost vzpenjanja), kateri vzponi so prevoženi najbolje, kje so vozili boljši kolesarji.
- Določanje tipa podlage poti, kjer je segment in razvrščanje teh med cestne in "gozdne" oz. "makadamske", analiza kako to vpliva na priljubljenost, čas.
- Pridobivanje podatkov o kolesarstvu iz drugih virov, npr. Komoot routes in primerjava, integracija.*
- Izdelava interaktivnega orodja za prikaz zbranih podatkov in t.i. priporočilni sistem za kolesarsko pot glede na vnos uporabnika. Regija, cestna površina, težavnost, dolžina -> pot.*