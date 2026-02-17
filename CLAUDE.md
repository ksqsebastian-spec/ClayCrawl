# CLAUDE.md – Verbindliche Regeln für Claude Code

**Projekt:** Gruppenwerk Lead-E-Mail-Generator
**Version:** 1.0
**Status:** VERBINDLICH – Keine Ausnahmen

---

## KRITISCHE ANWEISUNG

Diese Regeln sind **ABSOLUT VERBINDLICH**. Bei jeder Code-Änderung MÜSSEN diese Regeln befolgt werden. Es gibt **KEINE AUSNAHMEN**.

**Bei Unsicherheit:** FRAGEN, nicht raten.

---

## 1. SPRACHE & LOKALISIERUNG

### 1.1 Code-Sprache

| Bereich | Sprache |
|---------|---------|
| CLI-Ausgaben / Logs | Deutsch |
| E-Mail-Templates | Deutsch |
| Kommentare | Deutsch |
| Variablen / Funktionen | Englisch |
| Klassen / Typen | Englisch |
| Config-Keys | Englisch |

### 1.2 Kommentar-Beispiel

```python
# Lädt alle Segmentierungsregeln aus der YAML-Datei
def load_segmentation_rules(path: str) -> dict[str, SegmentRule]:
    # Filtert nach aktiven Firmen
    rules = yaml.safe_load(open(path))
    return {k: SegmentRule(**v) for k, v in rules["segmentierung"].items()}
```

---

## 2. CODE-ARCHITEKTUR

### 2.1 Datei-Organisation

```
REGEL: Ein Modul = Eine Verantwortlichkeit
REGEL: Keine Datei über 300 Zeilen
REGEL: Bei >300 Zeilen → Aufteilen
```

**Dateinamen:** snake_case

```
✅ RICHTIG:
csv_reader.py
template_engine.py
ai_personalizer.py

❌ FALSCH:
CsvReader.py        (Kein PascalCase)
csvreader.py        (Nicht zusammen)
csv-reader.py       (Keine Bindestriche)
```

### 2.2 Ordnerstruktur – VERBINDLICH

```
/main.py                → CLI-Einstiegspunkt (nur Click-Definitionen)
/generator/             → Kernlogik (alle Verarbeitungsmodule)
/templates/             → Jinja2 E-Mail-Templates
/segments/              → Segmentierungsregeln (YAML)
/promo_materials/       → PDF-Link-Konfiguration (YAML)
/data/input/            → Apollo.io CSV-Eingabe
/data/output/           → Instantly CSV-Ausgabe + Logs
/tests/                 → pytest-Tests + Fixtures
```

**VERBOTEN:**
- Neue Top-Level-Ordner ohne Absprache
- `/utils`, `/helpers`, `/services` (→ gehört in `/generator`)
- Dateien außerhalb der Struktur

### 2.3 Import-Reihenfolge

```python
# 1. Standardbibliothek
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path

# 2. Externe Packages
import click
import pandas as pd
import yaml
from jinja2 import Environment, FileSystemLoader

# 3. Interne Module
from generator.csv_reader import read_and_validate
from generator.segmenter import assign_all
```

---

## 3. PYTHON TYPE HINTS

### 3.1 Keine fehlenden Type Hints – NIEMALS

```python
# ✅ RICHTIG
def process_leads(df: pd.DataFrame, rules: dict[str, SegmentRule]) -> list[Assignment]:
    ...

# ❌ VERBOTEN
def process_leads(df, rules):
    ...
```

### 3.2 Explizite Return Types – IMMER

```python
# ✅ RICHTIG
def resolve_pdf_link(company_id: str, segment_id: str, links: dict) -> str:
    ...

async def generate_icebreaker(assignment: Assignment, client: AsyncAnthropic) -> str:
    ...

# ❌ FALSCH
def resolve_pdf_link(company_id, segment_id, links):  # Fehlende Types
    ...
```

### 3.3 Dataclasses für strukturierte Daten

```python
# ✅ RICHTIG
@dataclass
class Assignment:
    lead: pd.Series
    company_id: str
    segment_id: str
    match_score: float

@dataclass
class RenderedEmail:
    subject_line: str
    body: str
    icebreaker: str
    pdf_link: str

# ❌ FALSCH: Dicts statt typisierter Strukturen
result = {"company": "seehafer", "segment": "hv", "score": 0.8}
```

### 3.4 Null-Safety

```python
# ✅ RICHTIG
company_links = links.get(company_id)
if company_links is None:
    logger.warning(f"Keine Links für {company_id} konfiguriert")
    return ""

# ❌ FALSCH
company_links = links[company_id]  # Kann KeyError werfen!
```

---

## 4. KONFIGURATION

### 4.1 Geschäftslogik in YAML, nicht in Code

```
REGEL: Segmentierungsregeln → segments/rules.yaml
REGEL: PDF-Links → promo_materials/links.yaml
REGEL: App-Einstellungen → config.yaml
REGEL: E-Mail-Texte → templates/{company}/{segment}.txt
```

### 4.2 API-Keys NIEMALS im Code

```python
# ✅ RICHTIG
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise click.ClickException("ANTHROPIC_API_KEY Umgebungsvariable nicht gesetzt")

# ❌ VERBOTEN
api_key = "sk-ant-..."
```

### 4.3 YAML laden – IMMER mit yaml.safe_load

```python
# ✅ RICHTIG
with open(path) as f:
    config = yaml.safe_load(f)

# ❌ VERBOTEN (Sicherheitsrisiko)
config = yaml.load(f)
config = yaml.load(f, Loader=yaml.FullLoader)
```

---

## 5. ERROR HANDLING

### 5.1 Fehler-Hierarchie

```
1. Validierungsfehler (fehlende Felder, ungültige E-Mails)
   → Lead überspringen, Warning loggen, weitermachen
2. API-Fehler (Claude API)
   → 3x Retry mit Backoff, dann Fallback-Icebreaker
3. Konfigurationsfehler (fehlendes Template, kaputte YAML)
   → Sofort abbrechen mit klarer Fehlermeldung
4. Fatale Fehler (keine Input-Datei, kein API-Key)
   → Exit mit Non-Zero Code
```

### 5.2 Logging – IMMER mit Python logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ RICHTIG
logger.info(f"Verarbeite {len(df)} Leads aus {input_path}")
logger.warning(f"Lead übersprungen: {email} — ungültiges E-Mail-Format")
logger.error(f"Claude API Fehler: {e}")

# ❌ VERBOTEN
print("Verarbeite Leads...")  # Kein print() für Logs
```

### 5.3 Keine leeren except-Blöcke

```python
# ✅ RICHTIG
try:
    response = await client.messages.create(...)
except anthropic.APIError as e:
    logger.error(f"API-Fehler für {lead.email}: {e}")
    return fallback_icebreaker(assignment)

# ❌ VERBOTEN
try:
    response = await client.messages.create(...)
except:
    pass
```

---

## 6. CLI (CLICK)

### 6.1 Kommandos klar strukturieren

```python
@click.group()
def cli():
    """Gruppenwerk Lead-E-Mail-Generator"""
    pass

@cli.command()
@click.option("--input", required=True, type=click.Path(exists=True))
@click.option("--no-ai", is_flag=True, default=False)
@click.option("--company", default=None)
def generate(input, no_ai, company):
    """Apollo CSV → Segmentierung → E-Mails → Instantly CSV"""
    ...
```

### 6.2 CLI-Feedback auf Deutsch

```python
# ✅ RICHTIG
click.echo(f"✓ {count} Leads verarbeitet")
click.echo(f"⚠ {skipped} Leads übersprungen")
click.echo(f"→ Ausgabe: {output_path}")

# ❌ FALSCH
click.echo(f"Processed {count} leads")
```

---

## 7. TESTING

### 7.1 pytest – Konventionen

```python
# Dateinamen: test_{modul}.py
# Funktionsnamen: test_{was_getestet_wird}

def test_segmenter_assigns_hausverwaltung_to_real_estate():
    ...

def test_csv_reader_skips_invalid_emails():
    ...

def test_fallback_icebreaker_returns_german_text():
    ...
```

### 7.2 Fixtures in conftest.py

```python
@pytest.fixture
def sample_lead() -> pd.Series:
    return pd.Series({
        "first_name": "Max",
        "last_name": "Müller",
        "email": "max@example.de",
        "title": "Facility Manager",
        "company_name": "ABC Hausverwaltung GmbH",
        "industry": "Real Estate",
        "company_size": "51-200",
    })
```

---

## 8. VERBOTENE PRAKTIKEN

| Verboten | Warum | Stattdessen |
|----------|-------|-------------|
| Fehlende Type Hints | Keine Type-Safety | Typen immer angeben |
| `print()` für Logging | Nicht konfigurierbar | `logging` Modul |
| `yaml.load()` | Sicherheitsrisiko | `yaml.safe_load()` |
| Hardcoded API Keys | Sicherheitsrisiko | Umgebungsvariablen |
| `except: pass` | Fehler versteckt | Fehler loggen |
| Magic Numbers | Unklar | Benannte Konstanten oder Config |
| >300 Zeilen/Datei | Unwartbar | Aufteilen |
| Geschäftslogik in Code | Nicht änderbar | YAML-Konfiguration |
| `*` Imports | Namespace-Verschmutzung | Explizite Imports |

---

## 9. CHECKLISTE

### Vor jedem Commit

- [ ] Alle Type Hints vorhanden
- [ ] Alle Funktionen haben Return Types
- [ ] Error Handling vorhanden
- [ ] Logging statt print()
- [ ] Keine hardcoded Werte
- [ ] Modul <300 Zeilen
- [ ] Imports sortiert (stdlib → extern → intern)
- [ ] Tests vorhanden und grün

### Vor Feature-Abschluss

- [ ] Feature funktioniert wie im PRD
- [ ] Edge Cases behandelt (leere CSV, fehlende Felder)
- [ ] CLI-Feedback auf Deutsch
- [ ] Dokumentation/Kommentare auf Deutsch

---

**DIESE REGELN SIND NICHT VERHANDELBAR.**

Bei Fragen: **FRAGE NACH** statt zu raten.
