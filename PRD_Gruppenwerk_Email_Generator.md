# PRD: Automatisierter E-Mail-Generator für Gruppenwerk Baufirma

## Projektübersicht

**Projektname:** Gruppenwerk Lead-E-Mail-Generator
**Version:** 1.0
**Erstellt von:** Axel Seehafer
**Datum:** 17. Februar 2026
**Ziel:** Ein Python-basiertes CLI-Tool, das aus einer Apollo.io-CSV-Datei personalisierte Kaltakquise-E-Mails für alle Gruppenwerk-Unternehmen generiert und als Instantly.ai-kompatible CSV exportiert — als Ersatz für Clay.

---

## 1. Problemstellung

Gruppenwerk ist eine wachsende Unternehmensgruppe aus Hamburg (gegründet 2010), die sich an Unternehmen der Handwerks- und Immobilienwirtschaft beteiligt. Die Gruppe vereint derzeit acht Unternehmen unter einer Dachgesellschaft. Für die Neukundenakquise über Kaltakquise-E-Mails fehlt ein automatisierter Prozess, der:

- Leads aus Apollo.io importiert
- Leads nach Branche, Unternehmensgröße und Bedarf segmentiert
- Personalisierte E-Mails je Gruppenwerk-Unternehmen generiert
- Relevante Referenzmaterialien (PDF-Links) automatisch zuordnet
- Eine fertige CSV für Instantly.ai exportiert

Aktuell wird dafür Clay verwendet, was durch dieses Tool ersetzt werden soll.

---

## 2. Unternehmensprofile der Gruppenwerk-Firmen

### 2.1 Seehafer Elemente (Alfred Seehafer GmbH)
- **Branche:** Bauelemente — Türen, Fenster, Wartung & Reparatur
- **Standort:** Hamburg
- **Gegründet:** 1948 (75+ Jahre Erfahrung)
- **Website:** https://seehafer-elemente.de
- **Kernleistungen:**
  - Objekttüren (Schallschutz, Einbruchhemmung, Brandschutz)
  - Fenster & Fenstersanierung
  - Wartung & Instandhaltung aller Bauelemente
  - Reparaturservice (Beschläge, Schlösser, Dichtungen, Mechaniken)
  - Komplettservice von Erstberatung bis Montage
- **Zielkunden:** Hausverwaltungen, Gewerbeimmobilien, öffentliche Gebäude, Wohnanlagen, Hotels, Kliniken, Schulen, Kitas, Seniorenheime
- **Referenzprojekte:**
  - Universitätsklinikum SH Lübeck (1.350 Türen)
  - Cremon Insel Hamburg Wohnungsbau (1.108 Türen)
  - ADAC Hotel Ramada Hamburg (580 Türen)
- **USPs:** Keine langen Wartezeiten, alles aus einer Hand, 75+ Jahre Erfahrung, maßgeschneiderte Konzepte

### 2.2 Karl Brink Tischlereibetrieb GmbH
- **Branche:** Tischlerei / Bautischlerei
- **Standort:** Heselstücken 10, 22453 Hamburg Groß Borstel
- **Geschäftsführer:** Axel Seehafer
- **HRB:** 26761 (Amtsgericht Hamburg)
- **Telefon:** 040/35703272
- **Website:** https://tischlerei-brink.de
- **Kernleistungen:**
  - Schreinerei / Tischlerarbeiten
  - Bautischlerei (Fenster, Türen)
  - Einbaumöbel & Maßanfertigungen
  - Holzhandel (Groß- und Einzelhandel für Holz & Latten)
- **Zielkunden:** Hausverwaltungen, Bauunternehmen, Immobilienentwickler, Privatkunden mit Sanierungsbedarf

### 2.3 Tomas Hantke Malermeister GmbH (Maler Hantke)
- **Branche:** Maler- und Lackiererarbeiten
- **Standort:** Sylvesterallee 2, 22525 Hamburg
- **Gegründet:** 1990 (35+ Jahre Erfahrung)
- **Telefon:** 040 - 879 31 31
- **Website:** https://www.maler-hantke.de
- **Geschäftsführer:** Fabian (Nachname aus Recherche: eigenständige Leitung)
- **Kernleistungen:**
  - Innen- und Außenanstriche
  - Fassadengestaltung & Fassadensanierung (inkl. denkmalgeschützte Gebäude)
  - Raumgestaltung & Farbberatung
  - Lackierarbeiten
  - Bodenbeläge (Parkett, Vinyl, Teppich, Designböden)
  - Tapezierarbeiten
  - Schimmelsanierung & Wasserschadensanierung
  - Möbelrestaurierung (Beizen, Kalken, Laugen, Krakelieren)
- **Besonderheiten:** Umweltfreundliche Produkte, allergikerfreundliche Farben & Materialien
- **Zielkunden:** Hausverwaltungen, Gewerbeimmobilien, Privatkunden, öffentliche Einrichtungen, denkmalgeschützte Objekte

### 2.4 J. Werner Gerüstbau GmbH & Co. KG
- **Branche:** Gerüstbau
- **Standort:** Hamburg
- **Erfahrung:** 40+ Jahre
- **Telefon:** 040 / 732 10 — 91
- **E-Mail:** info@j-werner-geruestbau.de
- **Website:** https://www.j-werner-geruestbau.de
- **Kernleistungen:**
  - Fassadengerüste (Einfamilienhäuser bis Großprojekte)
  - Gerüstbau für Wohnanlagen & öffentliche Einrichtungen
  - Wetterschutzdächer
  - Planung ab Projektbeginn (durchdachte Lösungen)
- **Mitgliedschaften:** Bundesverband Gerüstbau
- **Zertifizierungen:** Präqualifiziert für öffentliche Vergabeverfahren (PQ VOB)
- **USPs:** Zuverlässigkeit, Pünktlichkeit, Sicherheit als oberste Priorität, schnelle Reaktionsfähigkeit
- **Zielkunden:** Bauunternehmen, Hausverwaltungen, öffentliche Auftraggeber, Fassadensanierer

### 2.5 Werner GmbH Bauunternehmung (Werner Bau)
- **Branche:** Bauunternehmen / Gebäudesanierung
- **Standort:** Hamburg
- **Erfahrung:** Fast 100 Jahre (traditionsreiches Unternehmen)
- **Telefon:** 040 / 35 70 32 — 74
- **E-Mail:** info@werner-bau.eu
- **Website:** https://www.werner-bau.eu
- **Kernleistungen:**
  - Fassadensanierung (Fachgerechte Erhaltung, Holzschutz, Balkonsanierung)
  - Gebäudesanierung (Innen- und Außen)
  - Mauerarbeiten, Putzarbeiten, Malerarbeiten
  - Tür- und Fenstermontage
  - Heizungs-, Elektro- und Sanitärarbeiten
  - Spezialisierung auf denkmalgeschützte Gebäude (z.B. Hamburger Schulen mit historischen Klinkerfassaden)
- **Zertifizierungen:** Präqualifiziert für öffentliche Vergabeverfahren (PQ VOB)
- **Zielkunden:** Öffentliche Auftraggeber, Hausverwaltungen, Schulen, denkmalgeschützte Gebäude, Wohnanlagen

---

## 3. Gruppenwerk als Dachmarke

- **Gegründet:** 2010 in Hamburg
- **Geschäftsmodell:** Spezialisierter Investor im Handwerks- und Immobiliensektor. Beteiligt sich an Unternehmen und stärkt diese als festen Bestandteil der Gruppe nachhaltig.
- **Philosophie:** Moderne Unternehmenskulturen ohne veraltete Hierarchien. Menschen im Mittelpunkt. Unternehmerischer Freiraum für Führungskräfte.
- **Bilanz 2023:** 9 Mio. € (Gruppenwerk Projektentwicklung GmbH), +55,6% zum Vorjahr
- **Weitere Unternehmen im Portfolio:** Tischlerei Mehlig, Trappe Hausverwaltung (+ weitere)
- **Networking:** Betreibt "Gruppenwerk Networking" — einen Coworking-Space für branchenspezifisches Networking
- **Website:** https://gruppenwerk.de
- **LinkedIn:** https://de.linkedin.com/company/gruppenwerk

---

## 4. Technische Anforderungen

### 4.1 Input: Apollo.io CSV

Das Programm muss folgende Apollo.io-Felder verarbeiten können (Mindestfelder mit `*` markiert):

| Feldname | Beschreibung | Beispiel |
|---|---|---|
| `first_name` * | Vorname | Max |
| `last_name` * | Nachname | Müller |
| `email` * | E-Mail-Adresse | max@example.de |
| `title` * | Jobtitel | Facility Manager |
| `company_name` * | Firmenname | ABC Hausverwaltung GmbH |
| `industry` * | Branche | Real Estate |
| `company_size` | Mitarbeiterzahl oder Range | 51-200 |
| `company_revenue` | Umsatz | $10M-$50M |
| `city` | Stadt | Hamburg |
| `state` | Bundesland | Hamburg |
| `country` | Land | Germany |
| `company_linkedin_url` | LinkedIn der Firma | https://linkedin.com/... |
| `person_linkedin_url` | LinkedIn der Person | https://linkedin.com/in/... |
| `technologies` | Eingesetzte Technologien | SAP, Salesforce |
| `keywords` | Schlagwörter | Immobilien, Verwaltung |
| `seniority` | Hierarchie-Level | Manager |
| `departments` | Abteilung | Operations |
| `company_website` | Website | https://abc-hv.de |

### 4.2 Output: Instantly.ai CSV

Das exportierte CSV muss folgende Spalten enthalten:

| Feldname | Beschreibung | Pflicht |
|---|---|---|
| `email` | E-Mail-Adresse des Leads | Ja |
| `first_name` | Vorname | Ja |
| `last_name` | Nachname | Ja |
| `company_name` | Firmenname | Ja |
| `personalization` | Kompletter, personalisierter E-Mail-Body (HTML oder Plain Text) | Ja |
| `icebreaker` | Personalisierter erster Satz / Aufhänger | Ja |
| `subject_line` | Betreffzeile | Ja |
| `pdf_link` | Link zum relevanten Promo-Material | Ja |
| `campaign_id` | Identifier für die Instantly-Kampagne (= Gruppenwerk-Firma) | Ja |
| `segment` | Lead-Segment für Tracking | Optional |
| `custom_variable_1` | Frei belegbar (z.B. Referenzprojekt) | Optional |
| `custom_variable_2` | Frei belegbar (z.B. Branche des Leads) | Optional |

### 4.3 Programmstruktur

```
gruppenwerk-email-generator/
├── main.py                     # Haupteinstiegspunkt / CLI
├── config.yaml                 # Konfigurationsdatei
├── requirements.txt            # Python-Abhängigkeiten
├── README.md                   # Anleitung
│
├── data/
│   ├── input/                  # Apollo.io CSV-Dateien hier ablegen
│   └── output/                 # Generierte Instantly-CSVs
│
├── templates/
│   ├── seehafer_elemente/
│   │   ├── hausverwaltung.txt  # Template für Hausverwaltungen
│   │   ├── gewerbe.txt         # Template für Gewerbeobjekte
│   │   └── oeffentlich.txt     # Template für öffentliche Auftraggeber
│   ├── brink_tischlerei/
│   │   ├── hausverwaltung.txt
│   │   ├── bauunternehmen.txt
│   │   └── privat.txt
│   ├── maler_hantke/
│   │   ├── hausverwaltung.txt
│   │   ├── gewerbe.txt
│   │   ├── denkmalschutz.txt
│   │   └── privat.txt
│   ├── werner_geruestbau/
│   │   ├── bauunternehmen.txt
│   │   ├── hausverwaltung.txt
│   │   └── oeffentlich.txt
│   └── werner_bau/
│       ├── hausverwaltung.txt
│       ├── oeffentlich.txt
│       └── denkmalschutz.txt
│
├── promo_materials/
│   └── links.yaml              # PDF-Links pro Firma & Segment
│
├── segments/
│   └── rules.yaml              # Segmentierungsregeln
│
├── generator/
│   ├── __init__.py
│   ├── csv_reader.py           # Apollo CSV einlesen & validieren
│   ├── segmenter.py            # Lead-Segmentierung
│   ├── template_engine.py      # Template-Auswahl & Personalisierung
│   ├── ai_personalizer.py      # KI-basierte Personalisierung (Claude API)
│   ├── pdf_linker.py           # Promo-Material-Zuordnung
│   └── csv_exporter.py         # Instantly CSV Export
│
└── tests/
    ├── test_segmenter.py
    ├── test_template_engine.py
    └── test_csv_exporter.py
```

---

## 5. Segmentierungslogik

### 5.1 Primärsegmentierung nach Lead-Branche

Das Programm muss Leads automatisch den richtigen Gruppenwerk-Firmen zuordnen. Ein Lead kann für **mehrere Firmen relevant** sein (z.B. eine Hausverwaltung braucht Maler UND Tischler UND Gerüstbau).

```yaml
# segments/rules.yaml

segmentierung:
  seehafer_elemente:
    branchen:
      - "Real Estate"
      - "Property Management"
      - "Facility Management"
      - "Hospital & Health Care"
      - "Hospitality"
      - "Education"
      - "Construction"
    jobtitel_keywords:
      - "Facility"
      - "Hausverwalt"
      - "Property"
      - "Objektleiter"
      - "technisch"
      - "Gebäudemanag"
      - "Instandhaltung"
    unternehmensgröße_min: 10

  brink_tischlerei:
    branchen:
      - "Real Estate"
      - "Property Management"
      - "Construction"
      - "Architecture & Planning"
      - "Interior Design"
    jobtitel_keywords:
      - "Facility"
      - "Hausverwalt"
      - "Property"
      - "Bau"
      - "Architekt"
      - "Innenausbau"
      - "Projektleiter"
    unternehmensgröße_min: 5

  maler_hantke:
    branchen:
      - "Real Estate"
      - "Property Management"
      - "Facility Management"
      - "Construction"
      - "Architecture & Planning"
      - "Government"
    jobtitel_keywords:
      - "Facility"
      - "Hausverwalt"
      - "Property"
      - "Objektleiter"
      - "Bau"
      - "Sanierung"
      - "Denkmalschutz"
    unternehmensgröße_min: 5

  werner_geruestbau:
    branchen:
      - "Construction"
      - "Real Estate"
      - "Property Management"
      - "Architecture & Planning"
      - "Government"
    jobtitel_keywords:
      - "Bau"
      - "Projektleiter"
      - "Bauleiter"
      - "Facility"
      - "Hausverwalt"
      - "Sanierung"
      - "Fassade"
    unternehmensgröße_min: 10

  werner_bau:
    branchen:
      - "Real Estate"
      - "Property Management"
      - "Government"
      - "Education"
      - "Construction"
    jobtitel_keywords:
      - "Facility"
      - "Hausverwalt"
      - "Property"
      - "Bau"
      - "Sanierung"
      - "Denkmal"
      - "öffentlich"
    unternehmensgröße_min: 10
```

### 5.2 Sekundärsegmentierung (Template-Auswahl)

Innerhalb jeder Firma wird das passende Template gewählt:

| Segment-ID | Beschreibung | Template-Trigger |
|---|---|---|
| `hausverwaltung` | Hausverwaltungen & Property Manager | Branche enthält "Real Estate" ODER "Property" |
| `gewerbe` | Gewerbliche Immobilienbesitzer | Branche enthält "Commercial" ODER Firmengröße > 200 |
| `oeffentlich` | Öffentliche Auftraggeber / Behörden | Branche enthält "Government" ODER "Education" |
| `bauunternehmen` | Bauunternehmen & Generalunternehmer | Branche enthält "Construction" UND Titel enthält "Bau" |
| `denkmalschutz` | Denkmalschutz-Spezialisten | Keywords/Branche enthält "Denkmal" ODER "Heritage" |
| `privat` | Privatpersonen (nur Tischlerei & Maler) | Firmengröße < 5 ODER kein Firmenname |

---

## 6. E-Mail-Templates (Beispiele)

### 6.1 Grundstruktur jeder E-Mail

```
Betreffzeile: {subject_line}

{icebreaker}

{haupttext}

{cta_mit_pdf_link}

{signatur}
```

### 6.2 Beispiel: Seehafer Elemente → Hausverwaltung

```
Betreff: Türen & Fenster für {{company_name}} — schneller Service, keine Wartezeiten

Hallo {{first_name}},

{{icebreaker}}

als Hausverwaltung kennen Sie das Problem: defekte Türen oder Fenster in Mietobjekten erfordern schnelle, zuverlässige Lösungen — ohne wochenlange Wartezeiten.

Seit 1948 ist Seehafer Elemente der Partner für Hausverwaltungen in Hamburg. Wir bieten:

→ Reparaturservice innerhalb kurzer Reaktionszeiten
→ Wartungsverträge für Türen & Fenster Ihres gesamten Bestands
→ Komplettservice von Beratung bis Montage — alles aus einer Hand

Für die Cremon Insel in Hamburg haben wir z.B. über 1.100 Türen geliefert und montiert.

Ich habe eine kurze Übersicht unserer Leistungen für Hausverwaltungen zusammengestellt:
{{pdf_link}}

Hätten Sie in den nächsten Wochen Zeit für ein kurzes Gespräch?

Beste Grüße
[Absendername]
Seehafer Elemente | Ein Unternehmen von Gruppenwerk
```

### 6.3 Beispiel: Werner Gerüstbau → Bauunternehmen

```
Betreff: Gerüstbau für {{company_name}} — zuverlässig, pünktlich, sicher

Hallo {{first_name}},

{{icebreaker}}

wenn beim Bauprojekt das Gerüst nicht steht, steht alles still. Genau deshalb setzen Bauunternehmen in Hamburg seit über 40 Jahren auf J. Werner Gerüstbau.

Was uns auszeichnet:
→ Planung ab Projektbeginn — wir denken mit, bevor gebaut wird
→ Präqualifiziert für öffentliche Vergabeverfahren (PQ VOB)
→ Mitglied im Bundesverband Gerüstbau
→ Fassadengerüste, Wetterschutzdächer & Sonderkonstruktionen

Hier finden Sie eine Übersicht unserer Leistungen:
{{pdf_link}}

Haben Sie aktuell Projekte in Planung, bei denen wir Sie unterstützen können?

Beste Grüße
[Absendername]
J. Werner Gerüstbau | Ein Unternehmen von Gruppenwerk
```

### 6.4 Beispiel: Maler Hantke → Denkmalschutz

```
Betreff: Denkmalgerechte Fassadensanierung für {{company_name}}

Hallo {{first_name}},

{{icebreaker}}

denkmalgeschützte Gebäude verlangen einen Malermeister, der das historische Material versteht und gleichzeitig moderne Standards erfüllt.

Maler Hantke arbeitet seit über 35 Jahren an Fassaden in Hamburg — auch an Objekten unter Denkmalschutz. Wir verwenden umweltfreundliche, materialschonende Produkte und beraten Sie individuell zu Farbkonzepten, die zum Charakter Ihres Gebäudes passen.

Unsere Referenzen und Leistungen im Bereich Denkmalschutz finden Sie hier:
{{pdf_link}}

Darf ich Ihnen ein unverbindliches Angebot erstellen?

Beste Grüße
[Absendername]
Maler Hantke | Ein Unternehmen von Gruppenwerk
```

---

## 7. KI-Personalisierung (Icebreaker-Generierung)

### 7.1 Prompt-Template für Claude API

Das Programm nutzt die Claude API, um für jeden Lead einen personalisierten Icebreaker (1–2 Sätze) zu generieren. Der Prompt:

```python
ICEBREAKER_PROMPT = """
Du bist ein deutscher Vertriebstexter für ein Handwerksunternehmen aus Hamburg.

Schreibe einen personalisierten ersten Satz (maximal 2 Sätze) für eine Kaltakquise-E-Mail.

Empfänger:
- Name: {first_name} {last_name}
- Titel: {title}
- Firma: {company_name}
- Branche: {industry}
- Firmengröße: {company_size}
- Stadt: {city}

Absender-Firma: {gruppenwerk_firma}
Absender-Leistung: {kernleistung}

Regeln:
- Auf Deutsch schreiben
- Professionell aber warmherzig — nicht steif oder formell
- Beziehe dich auf die Branche oder den Jobtitel des Empfängers
- Nenne KEINEN konkreten Preis oder Prozentsatz
- Stelle keine Frage im Icebreaker
- Maximal 2 Sätze
- Kein "Sehr geehrte/r" — starte direkt mit dem Inhalt nach "Hallo {first_name},"

Beispiele für gute Icebreaker:
- "als Facility Manager bei einer der größeren Hamburger Hausverwaltungen wissen Sie, wie wichtig kurze Reaktionszeiten bei Reparaturen sind."
- "wir arbeiten bereits mit mehreren Hausverwaltungen im Raum Hamburg zusammen und haben gesehen, dass bei der Fassadensanierung häufig Gerüstbau-Kapazitäten der Engpass sind."
- "mit über 200 Mitarbeitern und einem wachsenden Immobilienbestand stehen bei {company_name} vermutlich regelmäßig Instandhaltungsthemen auf der Agenda."
"""
```

### 7.2 Fallback ohne API

Falls die Claude API nicht verfügbar ist oder Kosten gespart werden sollen, generiert das Programm regelbasierte Icebreaker:

```python
FALLBACK_ICEBREAKERS = {
    "hausverwaltung": "als {title} bei {company_name} haben Sie sicher regelmäßig mit Instandhaltungsthemen zu tun — von Türen über Fenster bis zur Fassade.",
    "bauunternehmen": "bei Bauprojekten in Hamburg kommt es auf zuverlässige Partner an, die pünktlich liefern und Qualität garantieren.",
    "oeffentlich": "öffentliche Gebäude stellen besondere Anforderungen an Qualität, Sicherheit und Vergabekonformität — genau darauf haben wir uns spezialisiert.",
    "denkmalschutz": "die Arbeit an denkmalgeschützten Gebäuden erfordert besonderes Fingerspitzengefühl und Erfahrung — beides bringen wir seit Jahrzehnten mit.",
    "gewerbe": "für gewerbliche Immobilien mit hoher Nutzungsfrequenz sind schnelle und professionelle Handwerksleistungen unverzichtbar.",
    "privat": "für Ihr Bau- oder Sanierungsprojekt möchten wir Ihnen eine unkomplizierte und professionelle Zusammenarbeit anbieten."
}
```

---

## 8. Promo-Material-Zuordnung

### 8.1 PDF-Links Konfiguration

```yaml
# promo_materials/links.yaml

seehafer_elemente:
  default: "https://link.gruppenwerk.de/seehafer-leistungen"
  hausverwaltung: "https://link.gruppenwerk.de/seehafer-hausverwaltung"
  gewerbe: "https://link.gruppenwerk.de/seehafer-gewerbe"
  oeffentlich: "https://link.gruppenwerk.de/seehafer-oeffentlich"
  referenzen: "https://link.gruppenwerk.de/seehafer-referenzen"

brink_tischlerei:
  default: "https://link.gruppenwerk.de/brink-leistungen"
  hausverwaltung: "https://link.gruppenwerk.de/brink-hausverwaltung"
  bauunternehmen: "https://link.gruppenwerk.de/brink-bau"
  privat: "https://link.gruppenwerk.de/brink-privat"

maler_hantke:
  default: "https://link.gruppenwerk.de/hantke-leistungen"
  hausverwaltung: "https://link.gruppenwerk.de/hantke-hausverwaltung"
  denkmalschutz: "https://link.gruppenwerk.de/hantke-denkmal"
  fassade: "https://link.gruppenwerk.de/hantke-fassade"

werner_geruestbau:
  default: "https://link.gruppenwerk.de/werner-geruestbau-leistungen"
  bauunternehmen: "https://link.gruppenwerk.de/werner-geruestbau-bau"
  oeffentlich: "https://link.gruppenwerk.de/werner-geruestbau-oeffentlich"

werner_bau:
  default: "https://link.gruppenwerk.de/werner-bau-leistungen"
  fassade: "https://link.gruppenwerk.de/werner-bau-fassade"
  denkmalschutz: "https://link.gruppenwerk.de/werner-bau-denkmal"
  oeffentlich: "https://link.gruppenwerk.de/werner-bau-oeffentlich"
```

> **Hinweis:** Die URLs sind Platzhalter. Vor dem Produktivbetrieb müssen echte, trackbare Links eingerichtet werden (z.B. über DocSend, Google Drive mit Tracking, oder eine eigene Landing Page). Keine PDFs direkt an E-Mails anhängen — das zerstört die Zustellbarkeit.

---

## 9. Konfigurationsdatei

```yaml
# config.yaml

# === API-Einstellungen ===
anthropic_api_key: "${ANTHROPIC_API_KEY}"  # Aus Umgebungsvariable
ai_model: "claude-sonnet-4-5-20250929"
ai_enabled: true                            # false = nur regelbasierte Icebreaker
ai_max_retries: 3
ai_rate_limit_delay_seconds: 1              # Pause zwischen API-Calls

# === Pfade ===
input_directory: "./data/input"
output_directory: "./data/output"
templates_directory: "./templates"
promo_materials_config: "./promo_materials/links.yaml"
segments_config: "./segments/rules.yaml"

# === E-Mail-Einstellungen ===
default_sender_name: "Axel Seehafer"
default_language: "de"
email_format: "plain_text"                  # "plain_text" oder "html"

# === Instantly.ai Einstellungen ===
instantly_csv_separator: ","
instantly_csv_encoding: "utf-8"
campaign_prefix: "gruppenwerk"              # Prefix für campaign_id

# === Verarbeitung ===
batch_size: 50                              # Leads pro Batch (API-Kostenkontrolle)
duplicate_check: true                       # Doppelte E-Mails filtern
log_level: "INFO"                           # DEBUG, INFO, WARNING, ERROR
```

---

## 10. CLI-Befehle

```bash
# Standard-Durchlauf: Apollo CSV → Segmentierung → E-Mail-Generierung → Instantly CSV
python main.py generate --input data/input/apollo_export.csv

# Nur Segmentierung anzeigen (ohne E-Mails zu generieren)
python main.py segment --input data/input/apollo_export.csv

# Ohne KI-Personalisierung (nur Templates + Fallback-Icebreaker)
python main.py generate --input data/input/apollo_export.csv --no-ai

# Nur für bestimmte Firma generieren
python main.py generate --input data/input/apollo_export.csv --company seehafer_elemente

# Dry Run: Zeigt Vorschau für die ersten 5 Leads
python main.py preview --input data/input/apollo_export.csv --count 5

# Export-Statistiken anzeigen
python main.py stats --output data/output/
```

---

## 11. Ablauf (Flowchart)

```
1. Apollo CSV einlesen & validieren
   ↓
2. Duplikate entfernen (basierend auf E-Mail)
   ↓
3. Leads segmentieren (Primär: Firma-Zuordnung)
   ↓
4. Für jeden Lead + Firma-Kombination:
   a. Sekundärsegment bestimmen (Template-Auswahl)
   b. Template laden
   c. Icebreaker generieren (KI oder Fallback)
   d. PDF-Link zuordnen
   e. Template mit Variablen füllen
   f. Betreffzeile generieren
   ↓
5. Instantly-CSV pro Kampagne exportieren
   ↓
6. Zusammenfassung & Statistiken ausgeben
```

---

## 12. Qualitätssicherung

### 12.1 Validierungsregeln

- E-Mail-Adressen werden auf Format geprüft (RFC 5322)
- Leere Pflichtfelder (`first_name`, `email`, `company_name`) führen zum Überspringen des Leads
- Generierte E-Mails werden auf Mindestlänge geprüft (> 100 Zeichen)
- Icebreaker dürfen maximal 2 Sätze / 200 Zeichen lang sein
- Keine doppelten E-Mails in der Ausgabe-CSV

### 12.2 Logging

- Jeder Durchlauf erzeugt eine Log-Datei unter `data/output/logs/`
- Enthält: Anzahl verarbeiteter Leads, Segmentverteilung, Fehler, API-Kosten
- Format: `{datum}_{zeit}_generation.log`

### 12.3 Tests

```bash
# Unit-Tests ausführen
pytest tests/ -v

# Integrations-Test mit Beispiel-CSV
python main.py generate --input tests/fixtures/sample_apollo.csv --no-ai
```

---

## 13. Abhängigkeiten

```
# requirements.txt
pandas>=2.0.0
pyyaml>=6.0
anthropic>=0.40.0
jinja2>=3.1.0
click>=8.0.0
email-validator>=2.0.0
pytest>=7.0.0
```

---

## 14. Sicherheitshinweise

- API-Keys niemals hardcoden — immer über Umgebungsvariablen (`ANTHROPIC_API_KEY`)
- Apollo-Exportdaten enthalten personenbezogene Daten → DSGVO beachten
- Generierte CSVs sicher speichern und nach Upload in Instantly löschen
- E-Mail-Versand nur an Business-Adressen (keine Privatadressen ohne Einwilligung)
- Opt-out-Mechanismus in jeder E-Mail (wird über Instantly gehandhabt)

---

## 15. Erweiterungsmöglichkeiten (v2.0)

- **Apollo API-Integration:** Leads direkt aus Apollo ziehen statt CSV-Export
- **Instantly API-Integration:** CSVs direkt hochladen statt manueller Import
- **A/B-Testing:** Mehrere Betreffzeilen/Templates pro Segment generieren
- **Follow-up-Sequenzen:** Nicht nur E-Mail 1, sondern E-Mails 2–4 generieren
- **CRM-Anbindung:** Antworten direkt in ein CRM (z.B. HubSpot) pushen
- **Dashboard:** Web-Interface für Statistiken und Kampagnen-Übersicht
- **Webhook-Automatisierung:** Apollo → Generator → Instantly komplett automatisch

---

## 16. Erfolgskennzahlen

| KPI | Zielwert | Messung |
|---|---|---|
| Öffnungsrate | > 45% | Instantly Analytics |
| Antwortrate | > 5% | Instantly Analytics |
| Positiv-Antwortrate | > 2% | Manuelles Tracking |
| Leads pro Stunde verarbeitet | > 500 | Tool-Statistik |
| Kosten pro Lead (API) | < 0,02 € | API-Kosten / Lead-Anzahl |
| Clay-Kosten-Ersparnis | 100% | Kein Clay-Abo mehr nötig |
