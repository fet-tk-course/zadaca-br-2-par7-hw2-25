[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

[Ovdje ukratko opišite domenu vaše aplikacije i njenu svrhu]

## Tim

- **Student A**: [Ime Prezime] - resurs: `/resursi_a`
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

### Resurs A: `/resursi_a`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/resursi_a` | Lista svih resursa (sa query filterom) |
| GET | `/resursi_a/{id}` | Dohvatanje resursa po ID-u |
| POST | `/resursi_a` | Kreiranje novog resursa |
| PUT | `/resursi_a/{id}` | Potpuna zamjena resursa |
| PATCH | `/resursi_a/{id}` | Djelimično ažuriranje resursa |
| DELETE | `/resursi_a/{id}` | Brisanje resursa |

**Primjer zahtjeva:**
```bash
# Kreiranje novog resursa
curl -X POST "http://localhost:8000/resursi_a" \
  -H "Content-Type: application/json" \
  -d '{"polje1": "vrijednost", "polje2": 123}'
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

**Primjer 3:**
- **Prompt:** Imam FastAPI endpoint koji vraća svu hranu. Kako da ga proširim da može filtrirati hranu po restaurant_id, ali da restaurant_id bude opcionalan parametar?
- **Kako je pomoglo:** AI je predložio spajanje dva endpointa u jedan koristeći Optional[int] kao tip parametra, gdje se filtriranje primjenjuje samo ako je parametar proslijeđen.
- **Prilagodbe:** AI-jev prijedlog nije uključivao provjeru slučaja kada restoran postoji, ali nema registriranih jela. Kako bi endpoint bio robusniji, dodala sam 404 provjeru kao dodan sloj validacije. Ova provjera osigurava da se greška vraća samo kada je filter aktivan — odnosno kada korisnik traži jela konkretnog restorana, a lista je prazna. Na taj način endpoint i dalje ispravno vraća praznu listu kada se dohvaća sva hrana bez filtera.

### Provjera zadaće

U dijelu pod a prvog zadatka, dodali smo tri validatora, dva za ime i jedan za cijenu hrane. Prvi provjerava da li je naziv prazan string, i ukoliko jeste isisuje adevkvatnu poruku. Drugi provjerava da li je duzina imena manja od dva karaktera, sto isto tako nije moguce. Treci validator prvjerava da li je cijena manja ili jednaka nuli, sto takodje nije moguce.

Tako da prilikom izvršavanja endpointa, ukoliko je i jedan od uslova u validatorima ispunjen, ispisat ce se adekvatna poruka.

U zadatku 1 u dijelu pod b, dodana je provjera vec postojece hrane u post endpointu. Na taj nacin se nece moci kreirati hrana sa istim id-em i bacit ce se iznimka prilikom kreiranja.

Model Food ima strani ključ restaurant_id koji povezuje resurs Food sa resursom Restaurant. Svako jelo mora pripadati postojećem restoranu. Mogu nastati greske u kreiranju ako ne znamo tacan id restorana u kojem pravimo jelo, jer su dva modela odvojena. Morali bi prvo naci tacan id restorana za koji pravimo jelo, pa onda napraviti dato jelo, obzirom da baza sama pravi id-eve. 