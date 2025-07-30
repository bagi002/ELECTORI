# ELECTORI Task Agent - Dokumentacija

## Pregled

ELECTORI Task Agent je Python modul koji automatski izvršava TASK 2 iz fajla DEVELOPMENT_TASKS.md. Agent omogućava sekvencijalno izvršavanje pod-taskova sa automatskim testiranjem i praćenjem progresije.

## Struktura Agenta

### Glavne komponente

1. **TaskAgent** (`task_agent.py`) - Glavni agent za upravljanje task-ovima
2. **BaseTaskImplementation** (`task_implementations/__init__.py`) - Bazna klasa za implementacije
3. **Task Implementations** - Specifične implementacije za svaki pod-task
4. **IntegrationTester** - Sistem za integracione testove

### Task 2 Implementacije

- **Task 2.1**: Frontend Framework i Layout (`task_2_1_frontend.py`)
- **Task 2.2**: Simulation Management UI (`task_2_2_simulation.py`)
- **Task 2.3**: City Management System (`task_2_3_city.py`)
- **Task 2.4**: Party Management System (`task_2_4_party.py`)

## Upotreba Agenta

### Osnovne komande

```bash
# Pokretanje Task 2
python task_agent.py run

# Prikazivanje progresije
python task_agent.py progress

# Resetovanje progresije
python task_agent.py reset

# Detaljno logovanje
python task_agent.py run --verbose

# Forsirani restart
python task_agent.py run --force
```

### Parametri

- `--task TASK`: ID taska za izvršavanje (default: task_2)
- `--sub-task SUB_TASK`: ID pod-taska za reset ili pojedinačno pokretanje
- `--force`: Preskoči završene taskove i izvršava ih ponovo
- `--progress-file FILE`: Fajl za čuvanje progresije (default: task_progress.json)
- `--verbose`: Detaljno logovanje

## Funkcionalnosti Task 2

### Task 2.1: Frontend Framework i Layout

**Vreme**: 90 minuta

**Kreira**:
- `templates/dashboard.html` - Glavni dashboard
- `templates/simulation_manager.html` - Upravljanje simulacijama
- `templates/base.html` - Bazni template sa navigacijom
- `static/css/dashboard.css` - Dashboard stilovi
- `static/css/style.css` - Glavni CSS
- `static/js/api.js` - API komunikacija
- `static/js/dashboard.js` - Dashboard funkcionalnost

**Funkcionalnosti**:
- Responsive navigation sa Bootstrap
- Dashboard sa statistikama i brzim akcijama
- API klasa za komunikaciju sa backend-om
- Utility funkcije za UI

### Task 2.2: Simulation Management UI

**Vreme**: 75 minuta

**Kreira**:
- `static/css/simulation.css` - Simulation manager stilovi
- `static/js/simulation_manager.js` - Funkcionalnost upravljanja

**Funkcionalnosti**:
- Lista simulacija sa preview
- Kreiranje nove simulacije
- Modal za brisanje simulacije
- Import/Export funkcionalnost (placeholder)
- Session management

### Task 2.3: City Management System

**Vreme**: 60 minuta

**Kreira**:
- `templates/city_manager.html` - City manager interface
- `static/js/city_manager.js` - City management logika

**Funkcionalnosti**:
- CRUD operacije za gradove
- Validacija populacije (100 - 10,000,000)
- Sortiranje i pretraga
- Koordinate (opciono)
- Statistike gradova

### Task 2.4: Party Management System

**Vreme**: 90 minuta

**Kreira**:
- `templates/party_manager.html` - Party manager interface
- `templates/party_profile.html` - Detaljni prikaz partije
- `static/js/party_manager.js` - Party management logika
- `static/css/party.css` - Party stilovi

**Funkcionalnosti**:
- CRUD operacije za partije
- Color picker za boje partija
- Ideology selector
- Party profile view
- Validacija jedinstvenih imena
- Podrška po gradovima

## Arhitektura

### Tracking Progresije

Agent koristi JSON fajl (`task_progress.json`) za čuvanje stanja:

```json
{
  "task_2": {
    "task_2_1": {
      "status": "completed",
      "timestamp": "2025-07-30T13:58:17",
      "error_message": null
    }
  }
}
```

### Status vrednosti

- `pending` - Čeka izvršavanje
- `running` - U toku
- `completed` - Završeno uspešno
- `failed` - Neuspešno
- `skipped` - Preskočeno

### Automatsko Testiranje

Agent automatski testira svaki korak:

1. **Unit testovi** za kreiranje fajlova
2. **Validacija** HTML/CSS/JavaScript fajlova
3. **Integracioni testovi** za cel Task 2
4. **Flask aplikacija startup** test
5. **API endpoints** testovi
6. **Frontend-backend integracija**

## Dodavanje Novih Taskova

### 1. Kreiranje Task Implementacije

```python
from task_implementations import BaseTaskImplementation

class NewTaskImplementation(BaseTaskImplementation):
    def execute(self) -> bool:
        # Implementacija logike
        return True
```

### 2. Registracija u TaskAgent

```python
def _execute_new_task(self) -> bool:
    from task_implementations.new_task import NewTaskImplementation
    impl = NewTaskImplementation(self.logger)
    return impl.execute()
```

### 3. Definisanje Task Structure

```python
SubTask(
    id="new_task_id",
    name="Naziv novog taska",
    description="Opis funkcionalnosti",
    estimated_time=60,  # minuti
    dependencies=["dependency_task_id"]
)
```

## Proširivanje za Nova Funkcionalnosti

### Dodavanje Validacija

U `BaseTaskImplementation`:

```python
def validate_my_file(self, content: str) -> bool:
    # Custom validation logic
    return True
```

### Dodavanje Helper Metoda

```python
def my_helper_method(self, param: str) -> bool:
    try:
        # Helper logic
        self.logger.info(f"Executing {param}")
        return True
    except Exception as e:
        self.logger.error(f"Error: {e}")
        return False
```

### Dodavanje Testova

U `IntegrationTester`:

```python
def _test_my_functionality(self) -> bool:
    self.logger.info("Testing my functionality...")
    # Test logic
    return True
```

## Najbolje Prakse

### 1. Error Handling

```python
try:
    # Task logic
    result = self.do_something()
    if result:
        self.logger.info("Success")
        return True
    else:
        self.logger.error("Failed")
        return False
except Exception as e:
    self.logger.error(f"Error: {e}")
    return False
```

### 2. Backup Strategija

```python
if not self.backup_file(file_path):
    return False
```

### 3. Validation Pattern

```python
def _test_components(self) -> bool:
    required_files = [...]
    
    for file_path in required_files:
        if not file_path.exists():
            self.logger.error(f"Missing: {file_path}")
            return False
        
        # Content validation
        if not self.validate_content(file_path):
            return False
    
    return True
```

## Troubleshooting

### Česti Problemi

1. **Import Errors**: Proverite da su svi dependency moduli instalirani
2. **Permission Errors**: Agent potreban write access za kreiranje fajlova
3. **Flask Errors**: Duplikacija routes ili template grešaka

### Debug Opcije

```bash
# Detaljno logovanje
python task_agent.py run --verbose

# Resetovanje specifičnog pod-taska
python task_agent.py reset --sub-task task_2_1

# Provera progresije
python task_agent.py progress
```

### Log Files

Agent koristi standard Python logging sa formatom:
```
YYYY-MM-DD HH:MM:SS,mmm - TaskAgent - LEVEL - Message
```

## Rezultati Task 2

### Kreirani Fajlovi

```
templates/
  ├── dashboard.html
  ├── simulation_manager.html
  ├── city_manager.html
  ├── party_manager.html
  ├── party_profile.html
  └── base.html (ažuriran)

static/
  ├── css/
  │   ├── style.css (ažuriran)
  │   ├── dashboard.css
  │   ├── simulation.css
  │   └── party.css
  └── js/
      ├── api.js
      ├── dashboard.js
      ├── simulation_manager.js
      ├── city_manager.js
      └── party_manager.js

app.py (ažuriran sa routes)
```

### Nove Routes

- `/dashboard` - Dashboard stranica
- `/simulation-manager` - Upravljanje simulacijama
- `/city-manager` - Upravljanje gradovima
- `/party-manager` - Upravljanje partijama
- `/party-profile` - Profil partije

### Funkcionalnosti

- ✅ Responsive navigation
- ✅ Dashboard sa statistikama
- ✅ CRUD operacije za simulacije
- ✅ CRUD operacije za gradove
- ✅ CRUD operacije za partije
- ✅ Color picker za partije
- ✅ Search i filtering
- ✅ Modal dialogs
- ✅ API integration
- ✅ Error handling
- ✅ Loading states

## Zaključak

ELECTORI Task Agent uspešno automatizuje kompletan razvoj Task 2 funkcionalnosti sa:

- **Automatskim izvršavanjem** svih pod-taskova
- **Integracionim testiranjem** kompletnog sistema
- **Praćenjem progresije** sa mogućnošću nastavka
- **Dokumentacijom** za proširivanje
- **Validacijom** svih kreiranih komponenti

Agent je spreman za proširivanje novim taskovima iz DEVELOPMENT_TASKS.md fajla.