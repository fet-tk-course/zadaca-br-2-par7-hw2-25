[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Ovaj repozitorij sadrži backend aplikaciju za sistem dostave hrane, razvijenu pomoću **FastAPI** okvira i **SQLModel** biblioteke za upravljanje bazom podataka.

## Domena i svrha aplikacije
**Domena:** Ova aplikacija pripada domeni dostave hrane i upravljanja ugostiteljskim resursima. Sistem je dizajniran da simulira backend platforme za naručivanje hrane.

**Svrha:** 
Glavna svrha aplikacije je omogućiti **digitalnu evidenciju i upravljanje podacima o restoranima i njihovoj ponudi jela**. API je dizajniran da administratorima i partnerima omogući:

* **Upravljanje restoranima:** Praćenje informacija o radnom vremenu, lokaciji, tipu kuhinje i ocjenama korisnika.
* **Upravljanje ponudom jela:** Evidenciju dostupnih jela, njihovih cijena, kategorija i nutritivnih informacija.
* **Pretragu i filtriranje:** Brzi uvid u to koji su restorani trenutno otvoreni ili koja su jela dostupna u određenom cjenovnom rangu.

## Tim

- **Student A**: Lamija Altumbabić - resurs: `/restaurants`
- **Student B**: Hedija Šišić - resurs: `/foods`

## Instalacija i pokretanje

### Preduvjeti

- Python 3.10 ili noviji
- pip

### Koraci

1. Klonirajte repozitorij:
```bash
git clone <url-repozitorija>
cd <naziv-repozitorija>
```

2. Kreirajte virtuelno okruženje:
```bash
python -m venv venv
```

3. Aktivirajte virtuelno okruženje:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalirajte zavisnosti:
```bash
pip install -r requirements.txt
```

5. Pokrenite aplikaciju:
```bash
uvicorn main:app --reload
```

6. Otvorite browser na adresi: `http://localhost:8000/docs`

## API Endpointi

### Resurs A: `/restaurants`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/restaurants` | Lista svih resursa (sa query filterom) |
| GET | `/restaurants/{id}` | Dohvatanje resursa po ID-u |
| POST | `/restaurants` | Kreiranje novog resursa |
| PUT | `/restaurants/{id}` | Potpuna zamjena resursa |
| PATCH | `/restaurants/{id}` | Djelimično ažuriranje resursa |
| DELETE | `/restaurants/{id}` | Brisanje resursa |

**Primjer zahtjeva:**
```bash
# Kreiranje novog restorana
curl -X POST "http://localhost:8000/restaurants" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Limenka", 
        "cuisine_type": "Cevapi", 
        "delivery_fee": 3.5, 
        "rating": 5, 
        "is_open": true, 
        "address": "Patriotske lige 24"
}'
```

### Resurs B: `/foods`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/foods?restaurant_id=3` | Lista svih jela sa opcionalnim query parametrom |
| GET | `/foods/{id}` | Dohvatanje jela po ID-u |
| POST | `/foods` | Kreiranje novog jela |
| PUT | `/foods/{id}` | Potpuna zamjena jela |
| PATCH | `/foods/{id}` | Djelimično ažuriranje jela |
| DELETE | `/foods/{id}` | Brisanje jela |

**Primjer zahtjeva:**
```bash
# Potpuna zamjena jela
curl -X PUT "http://localhost:8000/foods/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Pica Margherita", "restaurant_id": 1, "category": "pizza", "price": 9.00, "calories": 780, "available": true, "description": "Azurirana pica s mocarelom"}'
```

## Korištenje AI alata
### Student A
### Alat: Gemini
**Model:** Gemini 3 pro

**Primjer 1:**
- **Prompt:** "Pokušavam implementirati DELETE rutu za restorane, ali dobijam grešku 404 čak i kada ID postoji. Možeš li provjeriti logiku pretrage objekta u bazi prije samog brisanja?"
- **Kako je pomoglo:** AI je identifikovao logičku grešku u poretku komandi – pokušavala sam obrisati objekat prije nego što je sesija ```(session.exec) ```zapravo potvrdila njegovo postojanje.
- **Prilagodbe:** Ispravljena je logika brisanja u routes_a.py, dodavanjem provjere ```if not restaurant: raise HTTPException.```

**Primjer 2:**
- **Prompt:** "Imam Restaurant model u SQLModel-u. Želim da spriječim korisnika da prilikom kreiranja restorana (POST) ručno šalje id, jer to baza treba sama generisati. Također, želim da polje rating bude vidljivo kada se restoran čita (GET), ali da ga nije moguće direktno unijeti pri kreiranju.
- **Kako je pomoglo:** Predložio je kreiranje bazne klase ```RestaurantBase``` sa zajedničkim poljima, a zatim dvije odvojene klase: ```Restaurant``` (koja je table=True i ima id) i ```RestaurantCreate``` (koja se koristi samo za unos podataka). Objasnio je kako ovo razdvajanje modela povećava sigurnost API-ja.
- **Prilagodbe:** Ovu arhitekturu sam primijenila u ```models_a.py```. Rezultat je sigurniji kod gdje FastAPI automatski filtrira polja koja korisnik ne smije slati, dok baza i dalje ispravno čuva sve podatke.

### Student B
### Alat: Claude
**Model:** claude-sonnet-4

**Primjer 1:**
- **Prompt:** U SQLModel-u, ako imam Food entitet koji ima foreign key prema Restaurant tabeli, da li je bitno u kojem redoslijedu su polja definisana unutar klase? Treba li restaurant_id biti odmah nakon id ili može biti bilo gdje?"
- **Kako je pomoglo:** AI je potvrdio da redoslijed polja u SQLModel klasi ne utiče na funkcionalnost baze, ali je preporučio da se restaurant_id stavi odmah nakon id zbog čitljivosti.
- **Prilagodbe:** Dati prijedlog je primjenjen u finalnoj verziji models_b.py

**Primjer 2:**
- **Prompt:** U FastAPI ruteru imam dvije GET rute: /{food_id} i /restaurants/{restaurant_id}. Aplikacija se pokreće bez greške ali ruta za restorane nikad ne vraća rezultate. Zašto?
- **Kako je pomoglo:** AI je objasnio da FastAPI čita rute odozgo prema dolje i da specifičnije rute moraju biti definirane prije generalnih. Budući da je /{food_id} bila iznad /restaurants/{restaurant_id}, FastAPI je svaki zahtjev prema /restaurants/2 tumačio kao food_id = "restaurants"
- **Prilagodbe:** Problem je riješen premještanjem get_foods_by_restaurant funkcije iznad get_food u routes_b.py.


## Napomene

[Dodatne napomene specifične za vašu implementaciju]
