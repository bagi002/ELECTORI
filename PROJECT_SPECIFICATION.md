# ELECTORI - Simulacija Političkih Izbora
## Specifikacija Projekta

### 📋 Pregled Projekta
**ELECTORI** je simulaciona igra za jednog igrača koja omogućava kreiranje i upravljanje političkim sistemom fiktivne države. Igra omogućava kompletnu kontrolu nad svim aspektima političke scene - od kreiranja partija do sprovođenja izbora i donošenja zakona.

### 🎯 Glavni Ciljevi
- Kreiranje i upravljanje višestrukim simulacijama
- Potpuna kontrola nad političkim sistemom fiktivne države
- Realistična simulacija izbora sa statističkim rezultatima
- Upravljanje parlamentom i donošenje zakona
- Intuitivni vizuelni interfejs

---

## 🏗️ Arhitektura Aplikacije

### Backend (Flask)
- **Jezik**: Python 3.8+
- **Framework**: Flask
- **Baza podataka**: SQLite (za jednostavnost)
- **API**: RESTful endpoints
- **Struktura**: MVC pattern

### Frontend
- **HTML5**: Semantička struktura
- **CSS3**: Responsive design, flexbox/grid
- **JavaScript**: Vanilla JS, Chart.js za grafikone
- **UI Framework**: Bootstrap 5 (opciono)

---

## 📊 Struktura Podataka

### 1. Simulacija (Simulation)
```
- id (int, primary key)
- name (string, 100 chars)
- country_name (string, 100 chars)
- created_at (datetime)
- last_played (datetime)
- status (enum: active, paused, completed)
```

### 2. Grad (City)
```
- id (int, primary key)
- simulation_id (foreign key)
- name (string, 50 chars)
- population (int, min: 100, max: 10,000,000)
- coordinates_x (float, opciono)
- coordinates_y (float, opciono)
```

### 3. Partija (Party)
```
- id (int, primary key)
- simulation_id (foreign key)
- name (string, 50 chars)
- color (string, hex color)
- ideology (enum: levi, centar-levi, centar, centar-desni, desni)
- leader_name (string, 50 chars)
- founded_date (date)
- description (text, 500 chars)
```

### 4. Podrška Partije (PartySupport)
```
- id (int, primary key)
- party_id (foreign key)
- city_id (foreign key)
- support_percentage (float, 0-100)
- last_updated (datetime)
```

### 5. Izbori (Election)
```
- id (int, primary key)
- simulation_id (foreign key)
- name (string, 100 chars)
- type (enum: parliamentary, municipal, presidential)
- election_date (date)
- status (enum: scheduled, ongoing, completed)
- census_threshold (float, 0-50) - za parlamentarne i opštinske
- round_number (int, 1 ili 2) - za predsedničke
```

### 6. Kandidatura (Candidacy)
```
- id (int, primary key)
- election_id (foreign key)
- name (string, 100 chars)
- type (enum: party, coalition)
- city_id (foreign key, nullable) - za opštinske izbore
```

### 7. Članstvo u Kandidaturi (CandidacyMembership)
```
- id (int, primary key)
- candidacy_id (foreign key)
- party_id (foreign key)
- is_lead_party (boolean)
```

### 8. Rezultati Izbora (ElectionResult)
```
- id (int, primary key)
- election_id (foreign key)
- candidacy_id (foreign key)
- city_id (foreign key, nullable)
- votes_count (int)
- vote_percentage (float)
- seats_won (int, nullable)
```

### 9. Poslanik (MP)
```
- id (int, primary key)
- simulation_id (foreign key)
- party_id (foreign key)
- city_id (foreign key, nullable)
- name (string, 50 chars)
- parliament_type (enum: national, municipal)
- elected_date (date)
- active (boolean)
```

### 10. Koalicija u Parlamentu (ParliamentCoalition)
```
- id (int, primary key)
- simulation_id (foreign key)
- name (string, 100 chars)
- parliament_type (enum: national, municipal)
- city_id (foreign key, nullable)
- formed_date (date)
- active (boolean)
```

### 11. Zakon (Law)
```
- id (int, primary key)
- simulation_id (foreign key)
- title (string, 200 chars)
- description (text)
- parliament_type (enum: national, municipal)
- city_id (foreign key, nullable)
- proposed_date (date)
- voting_date (date, nullable)
- status (enum: proposed, voting, passed, rejected)
- proposer_party_id (foreign key)
```

### 12. Glasanje (Vote)
```
- id (int, primary key)
- law_id (foreign key)
- mp_id (foreign key)
- vote_type (enum: for, against, abstain)
- vote_date (datetime)
```

---

## 🎮 Funkcionalnosti

### 1. Upravljanje Simulacijama
- **Kreiranje nove simulacije**
  - Unos imena države
  - Definisanje početnih gradova (ime, broj stanovnika)
  - Automatsko kreiranje osnovnih partija
- **Lista simulacija** sa preview informacijama
- **Učitavanje postojeće simulacije**
- **Brisanje simulacije** sa konfirmacijom
- **Eksport/Import simulacija** (JSON format)

### 2. Upravljanje Gradovima
- **Dodavanje novih gradova**
- **Uređivanje postojećih** (ime, populacija)
- **Brisanje gradova** (sa validacijom dependencies)
- **Mapa gradova** (opciono, vizuelni prikaz)

### 3. Upravljanje Partijama
- **Kreiranje partija**
  - Ime partije (validacija jedinstvenosti)
  - Boja (color picker)
  - Ideologija (dropdown)
  - Lider partije
  - Opis partije
- **Uređivanje postojećih partija**
- **Brisanje partija** (sa validacijom dependencies)
- **Mass support editing** - bulk uređivanje podrške

### 4. Sistem Podrške
- **Matrica podrške** - tabela partija vs gradovi
- **Validacija** - zbir podrške po gradu ne sme prelaziti 100%
- **Auto-normalizacija** - opcija za automatsko prilagođavanje
- **Import/Export podrške** iz CSV fajla
- **Random generator** podrške sa parametrima

### 5. Sistem Izbora

#### 5.1 Kreiranje Izbora
- **Tip izbora**: Parlamentarni, Opštinski, Predsednički
- **Datum izbora**
- **Cenzus** (za parlamentarne i opštinske)
- **Kandidature**:
  - Samostalne partije
  - Koalicije (multi-select partija)

#### 5.2 Simulacija Izbora
- **Pre-election polling** - prikaz projekcija
- **Dan izbora**:
  - Animirani prikaz dolaska rezultata
  - Real-time grafikoni
  - Mapa rezultata po gradovima
- **Kalkulacija rezultata**:
  - Bazna podrška + RNG faktor (±5-15%)
  - D'Hondt metoda za raspodelu mandata
  - Specijalne regule za predsedničke izbore

#### 5.3 Predsednički Izbori
- **Prvi krug** - svi kandidati
- **Drugi krug** - dva najbolja
- **Podrška između krugova**:
  - Partije biraju koga podržavaju
  - Transfer glasova sa koeficijentom (70-90%)

### 6. Parlament

#### 6.1 Sastav Parlamenta
- **Prikaz poslanika** po partijama
- **Hemicycle view** - vizuelni prikaz raspored
- **Statistike** - brojevi, procenti, grafikoni

#### 6.2 Koalicije
- **Kreiranje koalicija** između partija
- **Upravljanje koalicijama** - dodavanje/uklanjanje partija
- **Koalicijski sporazumi** - definisanje ciljeva

#### 6.3 Glasanje o Zakonima
- **Kreiranje zakona**:
  - Naslov i opis
  - Partija predlagač
  - Tip parlamenta (državni/opštinski)
- **Pozicioniranje partija** - kako će glasati
- **Simulacija glasanja**:
  - Bazno pozicioniranje partije
  - RNG faktor za pojedinačne poslanike (±10%)
  - Real-time prikaz glasanja
- **Unapred definisani zakoni**:
  - Izbor predsednika parlamenta
  - Budzet države
  - Ustav (kvalifikovana većina)

### 7. Analitika i Izveštaji
- **Dashboard simulacije** - key metrics
- **Istorija izbora** - trend analysis
- **Stranke u fokusu** - detaljni profili
- **Geografska analiza** - podrška po regijama
- **Export izveštaja** (PDF, Excel)

---

## 🎨 Korisnički Interfejs

### 1. Layout
- **Header**: Logo, naziv simulacije, navigacija
- **Sidebar**: Glavni meni (Dashboard, Partije, Izbori, Parlament)
- **Main Area**: Dinamički sadržaj
- **Footer**: Status bar, quick actions

### 2. Dashboard
- **Quick Stats** cards
- **Recent Activity** timeline
- **Upcoming Elections** lista
- **Popular Charts** - trending data

### 3. Responsive Design
- **Desktop**: Full feature set
- **Tablet**: Adaptirani layout
- **Mobile**: Osnovne funkcionalnosti

### 4. Teme
- **Light mode** (default)
- **Dark mode**
- **High contrast** (accessibility)

---

## 🔧 Algoritmi

### 1. Kalkulacija Rezultata Izbora
```python
def calculate_election_results(election, city):
    results = {}
    total_randomness = random.uniform(0.05, 0.15)  # 5-15% randomness
    
    for candidacy in election.candidacies:
        base_support = get_candidacy_support(candidacy, city)
        random_factor = random.uniform(-total_randomness, total_randomness)
        final_support = max(0, base_support + random_factor)
        results[candidacy.id] = final_support
    
    # Normalize to 100%
    total = sum(results.values())
    if total > 0:
        results = {k: (v/total) * 100 for k, v in results.items()}
    
    return results
```

### 2. D'Hondt Algoritam
```python
def allocate_seats_dhondt(results, total_seats, census_threshold=0):
    # Filter parties above census
    eligible = {k: v for k, v in results.items() if v >= census_threshold}
    
    seats = {party: 0 for party in eligible}
    quotients = list(eligible.items())
    
    for _ in range(total_seats):
        # Find highest quotient
        max_party = max(quotients, key=lambda x: x[1] / (seats[x[0]] + 1))
        seats[max_party[0]] += 1
    
    return seats
```

### 3. Transfer Glasova (Predsednički)
```python
def transfer_votes_presidential(first_round, eliminated_parties, support_decisions):
    second_round = {party: votes for party, votes in first_round.items() 
                   if party not in eliminated_parties}
    
    for eliminated_party, votes in first_round.items():
        if eliminated_party in eliminated_parties:
            supported_party = support_decisions.get(eliminated_party)
            if supported_party:
                transfer_rate = random.uniform(0.7, 0.9)  # 70-90% transfer
                second_round[supported_party] += votes * transfer_rate
    
    return second_round
```

---

## 🛡️ Validacije i Ograničenja

### 1. Validacije Podataka
- **Imena**: Jedinstvenost u okviru simulacije
- **Podrška**: Suma po gradu ≤ 100%
- **Populacija**: Pozitivni brojevi
- **Datumi**: Logički redosled
- **Cenzus**: 0-50% za izbore

### 2. Business Logic Validacije
- **Brisanje**: Provera dependencies
- **Izbori**: Minimum jedna kandidatura
- **Glasanje**: Poslanik može glasati samo jednom
- **Koalicije**: Partija može biti u jednoj koaliciji

### 3. Sistem Grešaka
- **User-friendly poruke**
- **Logging** za debug
- **Recovery mehanizmi**
- **Data backup** pre kritičnih operacija

---

## 🔒 Bezbednost i Performance

### 1. Bezbednost
- **Input sanitization**
- **SQL injection prevention**
- **XSS protection**
- **CSRF tokens**

### 2. Performance
- **Database indexing**
- **Query optimization**
- **Lazy loading**
- **Caching** (za kalkulacije)
- **Pagination** za velike liste

### 3. Data Integrity
- **Foreign key constraints**
- **Transaction management**
- **Backup strategija**
- **Data validation layers**

---

## 🧪 Testiranje

### 1. Unit Tests
- **Model validacije**
- **Algoritmi kalkulacije**
- **Business logic**

### 2. Integration Tests
- **API endpoints**
- **Database operacije**
- **Workflow testovi**

### 3. Manual Testing
- **UI/UX scenarios**
- **Browser compatibility**
- **Performance testing**

---

## 📈 Dodatne Funkcionalnosti (Buduće Verzije)

### 1. Napredna Analitika
- **Swing analysis** - promena glasova između izbora
- **Demografska analiza** - podrška po grupama
- **Prediction models** - AI-powered projekcije

### 2. Događaji i Krize
- **Random eventi** koji utiču na popularnost
- **Ekonomske krize**
- **Skandali partija**
- **Prirodne katastrofe**

### 3. Medijski Sistem
- **TV debati** - uticaj na popularnost
- **Reklame** - kampanje partija
- **Društvene mreže** - online prisutnost

### 4. Napredni Parlament
- **Amandmani** na zakone
- **Komisije** parlamenta
- **Interpelacije** i pitanja poslanika
- **Vote trading** sistem

### 5. Multi-player Mode
- **Online simulacije**
- **Kompetitivne igre**
- **Cooperative mode**

---

## 📋 Zakljucak

ELECTORI predstavlja kompleksnu simulacionu igru koja kombinuje realne političke procese sa gamification elementima. Projektovan je da bude edukativan, zabavan i realistican prikaz demokratskih procesa.

Koristeći Flask backend sa SQLite bazom podataka i moderan frontend sa JavaScript bibliotekama, aplikacija će pružiti stabilno i responsivno korisničko iskustvo.

Modularni pristup development-u omogućava postupno dodavanje funkcionalnosti i lako održavanje koda, dok jasno definisana struktura podataka osigurava skalabilnost sistema.

---

*Specifikacija verzija 1.0 - Juli 2025*
*Autor: GitHub Copilot*
