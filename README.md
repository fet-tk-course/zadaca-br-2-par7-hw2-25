[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

[Ovdje ukratko opišite domenu vaše aplikacije i njenu svrhu]

## Tim

- **Student A**: [Lamija Altumbabić] - resurs: `/restaurants`
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
| GET | `/foods` | Lista svih resursa |
| GET | `/foods/{id}` | Dohvatanje jela po ID-u |
| GET | `//foods/restaurants/{restaurant_id}` | Dohvatanje svih jela određenog restorana |
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
