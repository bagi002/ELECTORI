# ELECTORI - Simulacija Političkih Izbora

## 📋 O Projektu
ELECTORI je simulaciona igra za jednog igrača koja omogućava kreiranje i upravljanje političkim sistemom fiktivne države. Igra omogućava kompletnu kontrolu nad svim aspektima političke scene - od kreiranja partija do sprovođenja izbora i donošenja zakona.

## 🚀 Pokretanje Aplikacije

### Preduslovi
- Python 3.8 ili noviji
- pip (Python package manager)

### Instalacija

1. **Klonirajte ili preuzmite projekat**
```bash
cd /home/bagi/Desktop/ELECTORI
```

2. **Kreirajte virtuelno okruženje**
```bash
python3 -m venv venv
```

3. **Aktivirajte virtuelno okruženje**
```bash
source venv/bin/activate  # Linux/Mac
# ili
venv\Scripts\activate     # Windows
```

4. **Instalirajte zavisnosti**
```bash
pip install -r requirements.txt
```

5. **Pokrenite aplikaciju**
```bash
python app.py
```

6. **Otvorite browser**
Idite na `http://127.0.0.1:5000`

## 📂 Struktura Projekta

```
ELECTORI/
├── app.py                 # Glavna Flask aplikacija
├── config.py              # Konfiguracije aplikacije
├── requirements.txt       # Python zavisnosti
├── .gitignore            # Git ignore fajl
├── models/               # Database modeli
│   ├── __init__.py
│   ├── simulation.py
│   ├── city.py
│   ├── party.py
│   ├── election.py
│   └── parliament.py
├── routes/               # API rute
│   ├── __init__.py
│   ├── simulation_routes.py
│   ├── city_routes.py
│   └── party_routes.py
├── templates/            # HTML template-i
│   ├── base.html
│   ├── index.html
│   └── errors/
│       ├── 404.html
│       ├── 500.html
│       └── 400.html
├── static/               # Statični fajlovi
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── utils/               # Pomoćni moduli
    ├── __init__.py
    ├── helpers.py
    └── validators.py
```

## ✅ Task 1.1 - Kompletiran

### Završeno:
- ✅ Osnovna Flask aplikacija struktura
- ✅ Configuration setup (development, production, testing)
- ✅ Requirements.txt sa potrebnim bibliotekama
- ✅ Osnovni HTML template sistem (base.html, index.html)
- ✅ CSS styling sa custom varijablama i responsive design
- ✅ JavaScript foundation sa ELECTORI namespace
- ✅ Model placeholder struktura
- ✅ Route placeholder struktura
- ✅ Utility funkcije i validatori
- ✅ Error handling template-i (404, 500, 400)
- ✅ Pokretanje i testiranje aplikacije

### Funkcionalnosti:
- Osnovna Flask aplikacija koja se pokreće na portu 5000
- Responsive web interface sa custom CSS
- JavaScript framework za frontend funkcionalnosti
- API struktura spremna za implementaciju
- Error handling za sve HTTP greške
- Health check endpoint-i za sve module

## 🔄 Sledeći Koraci

Sledeći zadatak je **Task 1.2: Database Setup i Models** koji uključuje:
- Implementaciju SQLAlchemy modela
- Database initialization
- CRUD operacije
- Seed data za testiranje

## 🏛️ Arhitektura

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM za bazu podataka
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Semantička struktura
- **CSS3** - Custom styling sa CSS varijablama
- **Vanilla JavaScript** - Bez spoljnih framework-a
- **Chart.js** - Spremno za grafikone

### Database
- **SQLite** - Za development (jednostavnost)
- Mogu se lako promeniti na PostgreSQL ili MySQL

## 📞 Podrška

Za pitanja i probleme, kreirajte issue ili kontaktirajte developers.

---

*Verzija: 1.0.0*  
*Datum: Juli 2025*  
*Status: Task 1.1 Kompletiran ✅*
