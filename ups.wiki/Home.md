Welcome to the ups wiki!

# UPS CORP
Projekt který se zaměřuje na sledování užití UPS bytu, pomocí několika jednoduchých nástrojů, jako je RFID čtečka či v budoucnu phybový detektor. Je cílem, aby prostředí mělo možnost dát o “sobě” vědět, jak moc se používá, za účelem zlepšení a řešení. Dát prostředí vidění, sluch a hmat (u tohohle si nejsem jist jsem tím myslel). Možná, pokud bude i možnost v budoucnu přidat chuť a čich.

## UPS USER
uživatel = člověk, který vlastní USP CORP kartičku

## K ANÁLY
kanály, kterými lze komunikovat. Vnitřní a Externí.

### UPS CHAT
propojení s telegramem, kde si bude člověk moci vytáhnout jakékoliv data, které se zpracují z UPS ANAL a zeptat se na svoje data, které má zaznamenané v UPS CORP.

### UPS WEB
stránky, které budou obecné informace o užívání bytu. např. kolikrát byl vynesen koš tenhle měsíc. kolik se kumulativně strávilo času na WC. Kolik lidí je nejvíce v kuchyňi? Kdy je chodba nejvíce využívaná? atd.

## DATA
veškeré zpracování dat, které se zaznamenají do jednotlivých modulů.

### UPS ANAL
aka UPS ANALYTICS. Analýza dat, které jsou nasbírané z podpůrných modůlu, které se postupně naimplementují do UPS bytu. grafy. Zde by měli být veškeré nástoroje na analýzu dat, které by ten byt mohl vyprodukovat. Zatím máme 3 grafické zobrazení dat.
- ups pie (koláčový graf každého uživatele s poměřem IN v OUT)
- ups bar (sloupcový graf srovnání všech uživatelů UPS)
- ups bar count (sloupcový graf na počet IN a OUT, tenhle je takový zbytečný, pokud není v kontextu s dalšími)

### UPS DATA
databáze, která obahuje veškeré logy, které půjdou z modulu

## MODULY

### UPS IN/OUT
logování příchodu a odchodu člověka

- každý člen má UPS CARD a tou se může pípat u vstupu do bytu. zaznamenává se vstupní či odchozí čas
- později použít lepší řešení než je RFID karta a RFID čtečka. možná RFID brána? :D

### UPS POOP
prvně kumulativní čas použití WC, později bude POOP SCORE. Každý bude mít logovanej čas na sebe a bude se logovat. první místo bude mít titul **POOP LORD**.

- pomocí detekce pohybu a později nějaké řešení, aby se dalo párovat s člověkem

### UPS TRASH
vynášení odpadů je zatím dost old school. přehazujeme si kousek papíru a není to efektivní, jelikož na to zapomínáme. mnohdy, také nevím co vlastně vynášíme. možná bych to chtělo ještě analyzování toho jaký odpoad se vynáší.

- prvotně udělat mechanismus, na přepínání povinnosti vynášet odpad. (tlačítko?)

### UPS HOST
systém pro hosty. za každou návštěvu by mohli dostat nějaké speciální věci. 

- 5návštěva 5-ti vrstvý toaletní papír 
- 9návštěva úklid random části bytu 
- 10návštěva večeře podle přání. 
- 500návštěva stříbný host 
- 1000návštěva zlatý host 
- 2000návštěva platinový host 
- atd.

### UPS CERTIFICATE
certifikát pro lidi co byli flashnuti Andrejem

- Roman
- Linh (nejsem si jist, zda to bylo legit, takže možná znovu…)