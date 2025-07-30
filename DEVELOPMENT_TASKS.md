# ELECTORI - Plan Zadataka za Razvoj
## Development Task Breakdown

### 📋 Pregled
Ovaj dokument sadrži strukturiran plan zadataka za kreiranje ELECTORI aplikacije. Zadaci su organizovani po prioritetu i međusobnoj zavisnosti, omogućavajući model AI-u da ih izvršava iterativno.

---

## 🎯 FAZA 1: OSNOVNO PODEŠAVANJE (Foundation Setup)

### Task 1.1: Kreiranje Projekta i Strukture
**Prioritet**: Kritičan  
**Vreme**: 30 minuta  
**Zavisnosti**: Nema

**Opis**: Kreiranje osnovne strukture Flask aplikacije
- Kreiranje osnovne folder strukture
- Kreiranje requirements.txt sa potrebnim bibliotekama
- Kreiranje osnovnog Flask app.py fajla
- Kreiranje config.py za konfiguracije
- Kreiranje .gitignore fajla

**Očekivani rezultat**: Osnovna Flask aplikacija koja može da se pokrene

**Fajlovi za kreiranje**:
- `app.py`
- `config.py`
- `requirements.txt`
- `static/css/style.css`
- `static/js/main.js`
- `templates/base.html`
- `models/`
- `routes/`
- `utils/`

---

### Task 1.2: Database Setup i Models
**Prioritet**: Kritičan  
**Vreme**: 45 minuta  
**Zavisnosti**: Task 1.1

**Opis**: Kreiranje SQLAlchemy modela i database setup
- Kreiranje SQLAlchemy modela za sve entitete
- Database init script
- Osnovni CRUD operacije
- Seed data za testiranje

**Očekivani rezultat**: Funkcionalna baza podataka sa svim tabelama

**Fajlovi za kreiranje**:
- `models/__init__.py`
- `models/simulation.py`
- `models/city.py`
- `models/party.py`
- `models/election.py`
- `models/parliament.py`
- `database.py`
- `seed_data.py`

---

### Task 1.3: Osnovni API Endpoints
**Prioritet**: Kritičan  
**Vreme**: 60 minuta  
**Zavisnosti**: Task 1.2

**Opis**: Kreiranje osnovnih REST API endpoint-a
- CRUD operacije za simulacije
- CRUD operacije za gradove
- CRUD operacije za partije
- Osnovni error handling
- JSON serialization

**Očekivani rezultat**: API koji može da prima i vraća podatke u JSON formatu

**Fajlovi za kreiranje**:
- `routes/__init__.py`
- `routes/simulation_routes.py`
- `routes/city_routes.py`
- `routes/party_routes.py`
- `utils/helpers.py`
- `utils/validators.py`

---

## 🎯 FAZA 2: OSNOVNA FUNKCIONALNOST (Core Features)

### Task 2.1: Frontend Framework i Layout
**Prioritet**: Visok  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 1.3

**Opis**: Kreiranje osnovnog frontend-a
- HTML template za glavnu stranicu
- CSS styling sa Bootstrap
- JavaScript module setup
- Responsive navigation
- Basic dashboard layout

**Očekivani rezultat**: Funkcionaln frontend koji prikazuje podatke iz API-ja

**Fajlovi za kreiranje**:
- `templates/index.html`
- `templates/dashboard.html`
- `templates/simulation_manager.html`
- `static/css/dashboard.css`
- `static/js/api.js`
- `static/js/dashboard.js`

---

### Task 2.2: Simulation Management UI
**Prioritet**: Visok  
**Vreme**: 75 minuta  
**Zavisnosti**: Task 2.1

**Opis**: Kompletna funkcionalnost za upravljanje simulacijama
- Lista simulacija sa preview
- Form za kreiranje nove simulacije
- Modal za brisanje simulacije
- Import/Export funkcionalnost
- Session management

**Očekivani rezultat**: Potpuno funkcionalno upravljanje simulacijama

**Fajlovi za kreiranje**:
- `templates/simulation_list.html`
- `templates/create_simulation.html`
- `static/js/simulation_manager.js`
- `static/css/simulation.css`

---

### Task 2.3: City Management System
**Prioritet**: Visok  
**Vreme**: 60 minuta  
**Zavisnosti**: Task 2.2

**Opis**: Kompletno upravljanje gradovima
- Lista gradova sa statistikama
- Add/Edit/Delete gradova
- Validacije za broj stanovnika
- Sortiranje i filtering

**Očekivani rezultat**: Potpuno funkcionalno upravljanje gradovima

**Fajlovi za kreiranje**:
- `templates/city_manager.html`
- `static/js/city_manager.js`
- `routes/city_routes.py` (proširiti)

---

### Task 2.4: Party Management System
**Prioritet**: Visok  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 2.3

**Opis**: Kompletan sistem za upravljanje partijama
- CRUD operacije za partije
- Color picker za boje partija
- Ideology selector
- Party profile view
- Validacije jedinstvenih imena

**Očekivani rezultat**: Potpuno funkcionalno upravljanje partijama

**Fajlovi za kreiranje**:
- `templates/party_manager.html`
- `templates/party_profile.html`
- `static/js/party_manager.js`
- `static/css/party.css`

---

## 🎯 FAZA 3: SISTEM PODRŠKE (Support System)

### Task 3.1: Support Matrix Implementation
**Prioritet**: Visok  
**Vreme**: 120 minuta  
**Zavisnosti**: Task 2.4

**Opis**: Implementacija matrice podrške partija po gradovima
- Tabela sa partijama i gradovima
- Inline editing podrške
- Validacija 100% limit po gradu
- Auto-normalizacija opcija
- Bulk edit funkcionalnost

**Očekivani rezultat**: Potpuno funkcionalan sistem podrške

**Fajlovi za kreiranje**:
- `templates/support_matrix.html`
- `static/js/support_matrix.js`
- `routes/support_routes.py`
- `models/party_support.py`
- `static/css/support_matrix.css`

---

### Task 3.2: Support Analytics i Visualizations
**Prioritet**: Srednji  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 3.1

**Opis**: Analitika i grafikoni za podršku
- Chart.js implementacija
- Pie charts za podršku po gradu
- Bar charts za poređenje partija
- Trend analysis
- Export funkcionalnosti

**Očekivani rezultat**: Vizuelni prikaz podataka o podršci

**Fajlovi za kreiranje**:
- `static/js/charts.js`
- `templates/support_analytics.html`
- `utils/chart_data.py`

---

## 🎯 FAZA 4: SISTEM IZBORA (Election System)

### Task 4.1: Election Management
**Prioritet**: Kritičan  
**Vreme**: 150 minuta  
**Zavisnosti**: Task 3.1

**Opis**: Kreiranje i upravljanje izborima
- Form za kreiranje izbora (tip, datum, cenzus)
- Kandidature - samostalne i koalicije
- Validacije za tipove izbora
- Election schedule viewer

**Očekivani rezultat**: Potpuno funkcionalno kreiranje izbora

**Fajlovi za kreiranje**:
- `templates/election_manager.html`
- `templates/create_election.html`
- `static/js/election_manager.js`
- `routes/election_routes.py`
- `models/election.py` (proširiti)
- `utils/election_utils.py`

---

### Task 4.2: Election Simulation Engine
**Prioritet**: Kritičan  
**Vreme**: 180 minuta  
**Zavisnosti**: Task 4.1

**Opis**: Algoritam za simulaciju izbora
- Algoritam kalkulacije rezultata
- D'Hondt metoda za mandate
- Random faktori i modifikatori
- Results calculation engine
- Vote counting simulation

**Očekivani rezultat**: Funkcionalni algoritam za računanje rezultata

**Fajlovi za kreiranje**:
- `utils/election_algorithm.py`
- `utils/dhondt_algorithm.py`
- `models/election_result.py`
- Test scripts za algoritme

---

### Task 4.3: Election Day Simulation
**Prioritet**: Visok  
**Vreme**: 120 minuta  
**Zavisnosti**: Task 4.2

**Opis**: UI za dan izbora
- Animirani prikaz dolaska rezultata
- Real-time grafikoni
- Progress bar za prebrojavanje
- Mapa rezultata po gradovima
- Winners announcement

**Očekivani rezultat**: Impresivan UI za dan izbora

**Fajlovi za kreiranje**:
- `templates/election_day.html`
- `static/js/election_simulation.js`
- `static/css/election_day.css`
- `routes/election_simulation.py`

---

### Task 4.4: Presidential Elections Special Logic
**Prioritet**: Visok  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 4.3

**Opis**: Specifična logika za predsedničke izbore
- Dva kruga glasanja
- Transfer glasova između krugova
- UI za izbor podrške po partijama
- Second round calculation
- Special visualization

**Očekivani rezultat**: Potpuno funkcionalni predsednički izbori

**Fajlovi za kreiranje**:
- `utils/presidential_elections.py`
- `templates/presidential_runoff.html`
- `static/js/presidential.js`

---

## 🎯 FAZA 5: PARLAMENTARNI SISTEM (Parliament System)

### Task 5.1: Parliament Composition
**Prioritet**: Visok  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 4.2

**Opis**: Prikaz sastava parlamenta
- Lista poslanika po partijama
- Hemicycle visualization
- Statistics dashboard
- Seat allocation display
- MPs management

**Očekivani rezultat**: Vizuelni prikaz parlamenta

**Fajlovi za kreiranje**:
- `templates/parliament.html`
- `static/js/parliament_viz.js`
- `models/mp.py`
- `routes/parliament_routes.py`
- `static/css/parliament.css`

---

### Task 5.2: Coalition Management
**Prioritet**: Srednji  
**Vreme**: 75 minuta  
**Zavisnosti**: Task 5.1

**Opis**: Upravljanje koalicijama u parlamentu
- Kreiranje koalicija
- Dodavanje/uklanjanje partija
- Coalition agreements
- Visual coalition mapper

**Očekivani rezultat**: Sistem za upravljanje koalicijama

**Fajlovi za kreiranje**:
- `templates/coalition_manager.html`
- `static/js/coalition.js`
- `models/parliament_coalition.py`
- `utils/coalition_utils.py`

---

### Task 5.3: Law Creation System
**Prioritet**: Visok  
**Vreme**: 120 minuta  
**Zavisnosti**: Task 5.2

**Opis**: Sistem za kreiranje i upravljanje zakonima
- Form za kreiranje zakona
- Law proposal workflow
- Status tracking
- Predefined laws system
- Law library

**Očekivani rezultat**: Potpun sistem za upravljanje zakonima

**Fajlovi za kreiranje**:
- `templates/law_manager.html`
- `templates/create_law.html`
- `static/js/law_manager.js`
- `models/law.py`
- `utils/predefined_laws.py`

---

### Task 5.4: Voting Simulation
**Prioritet**: Kritičan  
**Vreme**: 150 minuta  
**Zavisnosti**: Task 5.3

**Opis**: Simulacija glasanja u parlamentu
- Party position setting
- Individual MP voting with RNG
- Real-time voting visualization
- Results calculation
- Voting history tracking

**Očekivani rezultat**: Potpuno funkcionalna simulacija glasanja

**Fajlovi za kreiranje**:
- `templates/voting_chamber.html`
- `static/js/voting_simulation.js`
- `utils/voting_algorithm.py`
- `models/vote.py`
- `static/css/voting.css`

---

## 🎯 FAZA 6: ANALITIKA I IZVJEŠTAJI (Analytics & Reports)

### Task 6.1: Dashboard Analytics
**Prioritet**: Srednji  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 5.4

**Opis**: Komprehensivni dashboard sa analiticima
- Key metrics cards
- Trending data
- Recent activity timeline
- Quick statistics
- Performance indicators

**Očekivani rezultat**: Informativan dashboard

**Fajlovi za kreiranje**:
- `templates/analytics_dashboard.html`
- `static/js/analytics.js`
- `utils/analytics_engine.py`
- `static/css/analytics.css`

---

### Task 6.2: Historical Analysis
**Prioritet**: Srednji  
**Vreme**: 75 minuta  
**Zavisnosti**: Task 6.1

**Opis**: Istorijska analiza i trendovi
- Election history timeline
- Swing analysis
- Party performance tracking
- Trend predictions
- Comparative analysis

**Očekivani rezultat**: Sistem za istorijsku analizu

**Fajlovi za kreiranje**:
- `templates/historical_analysis.html`
- `static/js/historical_charts.js`
- `utils/trend_analysis.py`

---

### Task 6.3: Export System
**Prioritet**: Nizak  
**Vreme**: 60 minuta  
**Zavisnosti**: Task 6.2

**Opis**: Export funkcionalnosti
- PDF reports generation
- Excel exports
- CSV data exports
- JSON backup/restore
- Print-friendly views

**Očekivani rezultat**: Kompletan export sistem

**Fajlovi za kreiranje**:
- `utils/export_utils.py`
- `templates/reports/`
- Export API endpoints

---

## 🎯 FAZA 7: POLIRANJE I OPTIMIZACIJA (Polish & Optimization)

### Task 7.1: UI/UX Improvements
**Prioritet**: Srednji  
**Vreme**: 120 minuta  
**Zavisnosti**: Task 6.3

**Opis**: Poboljšanja korisničkog interfejsa
- Responsive design fixes
- Loading states i spinners
- Error message improvements
- Toast notifications
- Accessibility improvements

**Očekivani rezultat**: Poliran i user-friendly interfejs

**Fajlovi za unapređenje**: Većina postojećih template i CSS fajlova

---

### Task 7.2: Performance Optimization
**Prioritet**: Srednji  
**Vreme**: 90 minuta  
**Zavisnosti**: Task 7.1

**Opis**: Optimizacija performansi
- Database query optimization
- JavaScript bundle optimization
- Caching implementation
- Lazy loading implementation
- Pagination systems

**Očekivani rezultat**: Brža i responsive aplikacija

---

### Task 7.3: Testing Suite
**Prioritet**: Visok  
**Vreme**: 120 minuta  
**Zavisnosti**: Task 7.2

**Opis**: Kreiranje test suite-a
- Unit tests za algoritme
- Integration tests za API
- Frontend testing setup
- Test data generators
- Automated testing setup

**Očekivani rezultat**: Comprehensive test coverage

**Fajlovi za kreiranje**:
- `tests/`
- `test_algorithms.py`
- `test_api.py`
- `test_models.py`

---

### Task 7.4: Documentation i Deployment
**Prioritet**: Srednji  
**Vreme**: 60 minuta  
**Zavisnosti**: Task 7.3

**Opis**: Finalna dokumentacija i deployment
- User manual
- API documentation
- Installation guide
- Deployment scripts
- Production configuration

**Očekivani rezultat**: Produkcijski spremna aplikacija

**Fajlovi za kreiranje**:
- `README.md`
- `INSTALLATION.md`
- `API_DOCS.md`
- `deploy.sh`
- `docker-compose.yml` (opciono)

---

## 📊 Sažetak Zadataka

### Po Fazama:
- **Faza 1**: 4 zadatka - Osnovno podešavanje (3.5h)
- **Faza 2**: 4 zadatka - Osnovna funkcionalnost (5.25h)
- **Faza 3**: 2 zadatka - Sistem podrške (3.5h)
- **Faza 4**: 4 zadatka - Sistem izbora (8.5h)
- **Faza 5**: 4 zadatka - Parlamentarni sistem (7.25h)
- **Faza 6**: 3 zadatka - Analitika (3.75h)
- **Faza 7**: 4 zadatka - Poliranje (6.5h)

### Ukupno: 25 zadataka, približno 38 sati rada

### Po Prioritetu:
- **Kritičan**: 6 zadataka
- **Visok**: 10 zadataka
- **Srednji**: 7 zadataka
- **Nizak**: 1 zadatak

---

## 🚀 Instrukcije za Izvršavanje

### Za AI Model:
1. **Redosled izvršavanja**: Uvek poštovati zavisnosti između zadataka
2. **Testiranje**: Nakon svakog zadatka, testirati funkcionalnost
3. **Iterativni pristup**: Jedan zadatak po iteraciji
4. **Dokumentacija**: Ažurirati komentare i dokumentaciju
5. **Validacija**: Proveriti da sve radi pre prelaska na sledeći zadatak

### Napomene:
- Svaki zadatak je osmišljen da bude nezavisan koliko god je moguće
- Vremenske procene su okvirne i mogu da variraju
- Prioritet određuje redosled kada postoji izbor između zadataka
- Neki zadaci mogu da se izvršavaju paralelno unutar iste faze

---

*Task Plan verzija 1.0 - Juli 2025*  
*Ukupno zadataka: 25*  
*Ukupno vreme: ~38 sati*
