# PRD TEMPLATE – Product Requirements Document

**Projekt:** [PROJEKTNAME]  
**Version:** 1.0  
**Datum:** [DATUM]  
**Autor:** [NAME]  
**Status:** Draft | In Review | Approved

---

## Nutzungshinweise

> **Vor dem Ausfüllen:** PROMPT_PREREQUISITES.md durchlaufen
> 
> **Platzhalter:** `[TEXT]` = Muss ersetzt werden
> 
> **Optionale Sektionen:** Mit `(Optional)` markiert – entfernen wenn nicht relevant

---

## Inhaltsverzeichnis

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Ziele & Erfolgskriterien](#3-ziele--erfolgskriterien)
4. [Nutzer & Personas](#4-nutzer--personas)
5. [Funktionale Anforderungen](#5-funktionale-anforderungen)
6. [Nicht-funktionale Anforderungen](#6-nicht-funktionale-anforderungen)
7. [Datenmodell](#7-datenmodell)
8. [Tech Stack](#8-tech-stack)
9. [Architektur](#9-architektur)
10. [UI/UX Spezifikation](#10-uiux-spezifikation)
11. [API-Design](#11-api-design)
12. [Security](#12-security)
13. [Testing](#13-testing)
14. [Deployment](#14-deployment)
15. [Projektstruktur](#15-projektstruktur)
16. [Anhang](#16-anhang)

---

## 1. Executive Summary

### 1.1 Projektziel

[1-3 Sätze: Was wird gebaut und warum?]

### 1.2 Kernprinzip

> **"[Design-Philosophie in einem Satz]"**

### 1.3 Scope

**IN SCOPE:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**OUT OF SCOPE:**
- [Ausgeschlossen 1] – [Begründung]
- [Ausgeschlossen 2] – [Begründung]

**PHASE 2+ (Später):**
- [Zukünftig 1]
- [Zukünftig 2]

### 1.4 Budget

| Posten | Monatlich | Jährlich |
|--------|-----------|----------|
| Hosting | €[X] | €[X] |
| Datenbank | €[X] | €[X] |
| Sonstiges | €[X] | €[X] |
| **Gesamt** | **€[X]** | **€[X]** |

---

## 2. Problem Statement

### 2.1 Ausgangssituation

[Beschreibung des aktuellen Zustands]

**Aktuell genutzte Lösung:** [Tool/Prozess oder "Keine"]

### 2.2 Problem-Definition

| Problem | Auswirkung | Priorität |
|---------|------------|-----------|
| [Problem 1] | [Auswirkung] | 🔴 Hoch |
| [Problem 2] | [Auswirkung] | 🟡 Mittel |
| [Problem 3] | [Auswirkung] | 🟢 Niedrig |

### 2.3 Gewünschte Lösung

[Beschreibung der idealen Lösung]

---

## 3. Ziele & Erfolgskriterien

### 3.1 Primäre Ziele

| Prio | Ziel | Messbar durch |
|------|------|---------------|
| 1 | [Ziel 1] | [Metrik] |
| 2 | [Ziel 2] | [Metrik] |
| 3 | [Ziel 3] | [Metrik] |

### 3.2 Erfolgskriterien ([X] Monate nach Launch)

- [ ] [Kriterium 1]
- [ ] [Kriterium 2]
- [ ] [Kriterium 3]

### 3.3 KPIs (Optional)

| KPI | Aktuell | Ziel |
|-----|---------|------|
| [KPI 1] | [Wert] | [Ziel] |
| [KPI 2] | [Wert] | [Ziel] |

---

## 4. Nutzer & Personas

### 4.1 Primärer Nutzer: [NAME]

| Attribut | Wert |
|----------|------|
| Rolle | [Jobtitel/Rolle] |
| Technische Affinität | [1-10] |
| Nutzungshäufigkeit | [Täglich/Wöchentlich/etc.] |
| Primäres Gerät | [Desktop/Mobile/Beides] |

**Bedürfnisse:**
- [Bedürfnis 1]
- [Bedürfnis 2]

**Frustrationen:**
- [Frustration 1]
- [Frustration 2]

### 4.2 Sekundärer Nutzer: [NAME] (Optional)

| Attribut | Wert |
|----------|------|
| Rolle | [Rolle] |
| Zugriffslevel | [Voll/Eingeschränkt/Nur Lesen] |

### 4.3 Authentifizierung

| Aspekt | Entscheidung |
|--------|--------------|
| Auth-Methode | [Passwort/SSO/Magic Link] |
| Nutzerkonten | [Individuell/Geteilt] |
| Session-Dauer | [X Tage] |
| Rollen | [Ja/Nein] |

**Rollen-Matrix (falls Rollen = Ja):**

| Rolle | Lesen | Erstellen | Bearbeiten | Löschen | Admin |
|-------|-------|-----------|------------|---------|-------|
| [Rolle 1] | ✅ | ✅ | ✅ | ✅ | ✅ |
| [Rolle 2] | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 5. Funktionale Anforderungen

### 5.1 Modul-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                      [APP NAME]                             │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│ [Modul 1]   │ [Modul 2]   │ [Modul 3]   │ [Modul 4]        │
└─────────────┴─────────────┴─────────────┴──────────────────┘
```

### 5.2 Feature-Priorisierung

| Feature | Priorität | Phase |
|---------|-----------|-------|
| [Feature 1] | Must-Have | MVP |
| [Feature 2] | Must-Have | MVP |
| [Feature 3] | Should-Have | MVP |
| [Feature 4] | Could-Have | Phase 2 |
| [Feature 5] | Won't-Have | Backlog |

---

### 5.3 Modul: [NAME]

**Zweck:** [Beschreibung]

#### Liste/Übersicht

**Funktionen:**
- [Funktion 1]
- [Funktion 2]

**Spalten:**

| Spalte | Sortierbar | Filterbar |
|--------|------------|-----------|
| [Spalte 1] | Ja | Ja |
| [Spalte 2] | Ja | Nein |

**Wireframe:**

```
┌─────────────────────────────────────────────────────────────┐
│ [TITEL]                                    [+ Neu] [Export] │
├─────────────────────────────────────────────────────────────┤
│ 🔍 [Suche...]           [Filter 1 ▾]  [Filter 2 ▾]         │
├─────────────────────────────────────────────────────────────┤
│ [Spalte 1]  │ [Spalte 2]  │ [Spalte 3]  │ Aktionen         │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ [Daten]     │ [Daten]     │ [Daten]     │ [→]              │
├─────────────────────────────────────────────────────────────┤
│ Zeige 1-20 von X                         [<] 1 2 3 [>]     │
└─────────────────────────────────────────────────────────────┘
```

#### Formular (Neu/Bearbeiten)

**Felder:**

| Feld | Typ | Pflicht | Validierung |
|------|-----|---------|-------------|
| [Feld 1] | Text | Ja | [Regel] |
| [Feld 2] | Zahl | Nein | >= 0 |
| [Feld 3] | Dropdown | Ja | Aus Liste |
| [Feld 4] | Datum | Nein | - |
| [Feld 5] | Textarea | Nein | Max. 2000 Zeichen |

---

### 5.4 Modul: Dashboard (Optional)

**Inhalte:**

| Widget | Beschreibung |
|--------|--------------|
| [Widget 1] | [Was zeigt es] |
| [Widget 2] | [Was zeigt es] |
| Schnellaktionen | [Buttons] |

---

### 5.5 Import/Export (Optional)

**Export:**
- Format: [CSV/Excel/PDF]
- Umfang: [Was wird exportiert]

**Import:**
- Format: [CSV]
- Pflichtfelder: [Felder]

---

## 6. Nicht-funktionale Anforderungen

### 6.1 Performance

| Metrik | Zielwert |
|--------|----------|
| Seitenladezeit | < [X] Sekunden |
| API Response | < [X] ms |
| Max. gleichzeitige Nutzer | [X] |

### 6.2 Verfügbarkeit

| Metrik | Zielwert |
|--------|----------|
| Uptime | [99%/99.9%] |
| Backup-Frequenz | [Täglich/Stündlich] |

### 6.3 Skalierbarkeit

| Metrik | Aktuell | Kapazität |
|--------|---------|-----------|
| [Entität 1] | ~[X] | [X]+ |
| [Entität 2] | ~[X] | [X]+ |

### 6.4 Benutzerfreundlichkeit

| Anforderung | Umsetzung |
|-------------|-----------|
| Sprache | [Deutsch/Englisch] |
| Zielgruppe Tech-Level | [1-10] |
| Mobile-Support | [Ja/Nein/Responsive] |

### 6.5 Browser-Support

| Browser | Version |
|---------|---------|
| Chrome | Letzte 2 |
| Firefox | Letzte 2 |
| Safari | Letzte 2 |
| Edge | Letzte 2 |

---

## 7. Datenmodell

### 7.1 ER-Diagramm

```
[Entität 1] ─── 1:n ───► [Entität 2]
     │
     └── n:m ───► [Entität 3]
```

### 7.2 Tabellen

#### [tabelle_1]

```sql
CREATE TABLE [tabelle_1] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    [feld_1] VARCHAR(255) NOT NULL,
    [feld_2] INTEGER DEFAULT 0,
    [feld_3] BOOLEAN DEFAULT FALSE,
    [fk_id] UUID REFERENCES [andere_tabelle](id),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Constraints
ALTER TABLE [tabelle_1] ADD CONSTRAINT chk_status 
    CHECK (status IN ('active', 'archived'));

-- Indizes
CREATE INDEX idx_[tabelle]_[feld] ON [tabelle_1]([feld]);
```

#### [tabelle_2]

[Wiederhole für jede Tabelle]

### 7.3 Stammdaten (Lookup Tables)

```sql
CREATE TABLE [stammdaten] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

INSERT INTO [stammdaten] (name, sort_order) VALUES
    ('[Wert 1]', 1),
    ('[Wert 2]', 2),
    ('[Wert 3]', 3);
```

---

## 8. Tech Stack

### 8.1 Übersicht

| Kategorie | Technologie | Begründung |
|-----------|-------------|------------|
| Framework | [Next.js/React/Vue] | [Warum] |
| Sprache | [TypeScript/JavaScript] | [Warum] |
| Datenbank | [PostgreSQL/MySQL/MongoDB] | [Warum] |
| Backend | [Supabase/Firebase/Custom] | [Warum] |
| Auth | [Supabase Auth/NextAuth/etc.] | [Warum] |
| UI Library | [shadcn/MUI/etc.] | [Warum] |
| Styling | [Tailwind/CSS Modules] | [Warum] |
| State | [TanStack Query/Redux/Zustand] | [Warum] |
| Forms | [React Hook Form/Formik] | [Warum] |
| Validation | [Zod/Yup] | [Warum] |
| Testing | [Playwright/Cypress] | [Warum] |
| Hosting | [Vercel/Netlify/AWS] | [Warum] |

### 8.2 Dependencies

```json
{
  "dependencies": {
    "[package]": "^X.X.X"
  }
}
```

---

## 9. Architektur

### 9.1 System-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Pages  │  Components  │  Hooks  │  API Routes            │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND/API                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │    Auth     │  │  Database   │  │       Storage           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Datenfluss

```
Nutzer-Aktion → Validierung → API/DB → Cache Update → UI Update → Feedback
```

### 9.3 Event-System (Optional)

| Event | Trigger | Aktion |
|-------|---------|--------|
| [event.type] | [Wann] | [Was passiert] |

---

## 10. UI/UX Spezifikation

### 10.1 Design-Prinzipien

| Prinzip | Umsetzung |
|---------|-----------|
| [Prinzip 1] | [Wie] |
| [Prinzip 2] | [Wie] |

### 10.2 Farbschema

| Farbe | Hex | Verwendung |
|-------|-----|------------|
| Primary | #[HEX] | Buttons, Links |
| Success | #[HEX] | Erfolgsmeldungen |
| Warning | #[HEX] | Warnungen |
| Error | #[HEX] | Fehler |
| Background | #[HEX] | Hintergrund |

### 10.3 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                          │
├────────────┬────────────────────────────────────────────────────┤
│  SIDEBAR   │              MAIN CONTENT                          │
│ (optional) │                                                    │
└────────────┴────────────────────────────────────────────────────┘
```

### 10.4 Komponenten

**Buttons:**
- Primary: Hauptaktionen
- Secondary: Nebenaktionen
- Danger: Löschaktionen

**Formulare:**
- Labels: Oberhalb
- Pflichtfelder: Mit *
- Fehler: Unter Feld, rot

**Feedback (Toasts):**
- Erfolg: Grün, 3 Sek
- Fehler: Rot, 5 Sek
- Warnung: Gelb, 4 Sek

---

## 11. API-Design

### 11.1 Stil

- [ ] REST
- [ ] GraphQL
- [ ] Direct DB (Supabase Client)

### 11.2 Endpunkte (falls REST)

| Methode | Endpunkt | Beschreibung |
|---------|----------|--------------|
| GET | /api/[resource] | Liste |
| GET | /api/[resource]/:id | Einzeln |
| POST | /api/[resource] | Erstellen |
| PUT | /api/[resource]/:id | Update |
| DELETE | /api/[resource]/:id | Löschen |

### 11.3 Webhooks (Optional)

| Event | Payload |
|-------|---------|
| [event] | [Daten] |

---

## 12. Security

### 12.1 Authentifizierung

| Aspekt | Lösung |
|--------|--------|
| Methode | [Passwort/OAuth/SSO] |
| Session | [X Tage] |
| Token-Speicherung | [Cookie/Memory] |

### 12.2 Autorisierung

```sql
-- Row Level Security
ALTER TABLE [tabelle] ENABLE ROW LEVEL SECURITY;

CREATE POLICY "[name]" ON [tabelle]
    FOR ALL TO authenticated
    USING (true);
```

### 12.3 Datenschutz

| Bereich | Maßnahme |
|---------|----------|
| Transport | HTTPS |
| Datenbank | Verschlüsselung at rest |
| Passwörter | bcrypt/argon2 |

### 12.4 Input-Validierung

| Bereich | Tool |
|---------|------|
| Frontend | [Zod/Yup] |
| Datei-Upload | Max [X] MB, Typen: [.pdf, .jpg] |

---

## 13. Testing

### 13.1 Strategie

| Test-Art | Anzahl | Tool |
|----------|--------|------|
| E2E | ~[X] | [Playwright/Cypress] |
| Integration | ~[X] | [Vitest/Jest] |
| Unit | ~[X] | [Vitest/Jest] |

### 13.2 E2E-Szenarien

| # | Szenario |
|---|----------|
| 1 | [Login funktioniert] |
| 2 | [CRUD für Hauptentität] |
| 3 | [Kritischer Workflow] |

### 13.3 CI/CD

- [ ] Tests bei Push
- [ ] Tests bei Pull Request
- [ ] Deployment-Block bei Fehlern

---

## 14. Deployment

### 14.1 Umgebungen

| Umgebung | URL | Zweck |
|----------|-----|-------|
| Production | [URL] | Live |
| Preview | [Pattern] | PR-Reviews |
| Local | localhost:[PORT] | Entwicklung |

### 14.2 Umgebungsvariablen

```bash
# .env.example
[VAR_1]=[Beschreibung]
[VAR_2]=[Beschreibung]
```

### 14.3 Prozess

```
Push → Tests → Build → Deploy
```

### 14.4 Backup

| Typ | Frequenz | Aufbewahrung |
|-----|----------|--------------|
| DB | [Täglich] | [X Tage] |

---

## 15. Projektstruktur

```
/[project]
├── /app                     # Seiten
│   ├── layout.tsx
│   ├── page.tsx
│   ├── /[route]
│   └── /api
├── /components
│   ├── /ui                  # UI-Basis
│   ├── /[feature]           # Feature-spezifisch
│   ├── /layout              # Layout
│   └── /shared              # Geteilt
├── /lib
│   ├── /[db-client]         # DB-Konfig
│   ├── /validations         # Zod Schemas
│   ├── /errors              # Error Handling
│   ├── utils.ts
│   └── constants.ts
├── /hooks                   # Custom Hooks
├── /types                   # TypeScript
├── /__tests__               # Tests
├── .env.example
├── CLAUDE.md
└── README.md
```

---

## 16. Anhang

### 16.1 Glossar

| Begriff | Bedeutung |
|---------|-----------|
| [Begriff] | [Definition] |

### 16.2 Referenzen

| Ressource | URL |
|-----------|-----|
| [Name] | [URL] |

### 16.3 Änderungshistorie

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0 | [DATUM] | Initial |

### 16.4 Offene Fragen

| # | Frage | Status |
|---|-------|--------|
| 1 | [Frage] | ⬜ Offen |

---

## ✅ PRD Completion Checklist

- [ ] Executive Summary vollständig
- [ ] Problem klar definiert
- [ ] Alle Must-Have Features beschrieben
- [ ] Datenmodell vollständig
- [ ] Tech Stack festgelegt
- [ ] Security-Konzept vorhanden
- [ ] Alle Platzhalter ersetzt
- [ ] Review durchgeführt
- [ ] Status auf "Approved"

---

**Ende des PRD Templates**
