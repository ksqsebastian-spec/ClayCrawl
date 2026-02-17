# Architecture: Gruppenwerk Lead-E-Mail-Generator

## System Overview

A Python CLI pipeline that transforms Apollo.io lead CSVs into personalized, segmented cold emails exported as Instantly.ai-compatible CSVs — one per Gruppenwerk company campaign.

---

## 1. Data Flow

```
                          config.yaml
                              │
                              ▼
┌──────────┐   ┌───────────┐   ┌────────────┐   ┌─────────────────────────────┐   ┌──────────────┐
│ Apollo   │──▶│ CSV       │──▶│ Segmenter  │──▶│ Email Builder               │──▶│ CSV Exporter │
│ CSV      │   │ Reader &  │   │            │   │ ┌───────────┐ ┌───────────┐ │   │ (Instantly)  │
│          │   │ Validator │   │ Primary:   │   │ │ Template  │ │ AI Pers.  │ │   │              │
│          │   │           │   │  Company   │   │ │ Engine    │ │ (Claude)  │ │   │ 1 CSV per    │
│          │   │ - pandas  │   │ Secondary: │   │ │ (Jinja2)  │ │ or        │ │   │ campaign_id  │
│          │   │ - dedup   │   │  Template  │   │ │           │ │ Fallback  │ │   │              │
│          │   │ - validate│   │  type      │   │ └───────────┘ └───────────┘ │   └──────┬───────┘
└──────────┘   └───────────┘   └────────────┘   │ ┌───────────┐               │          │
                                                │ │ PDF       │               │          ▼
                                                │ │ Linker    │               │   data/output/
                                                │ └───────────┘               │   ├── seehafer_elemente_2026-02-17.csv
                                                └─────────────────────────────┘   ├── brink_tischlerei_2026-02-17.csv
                                                                                  ├── maler_hantke_2026-02-17.csv
                   ┌─────────────┐                                                ├── werner_geruestbau_2026-02-17.csv
                   │ segments/   │                                                ├── werner_bau_2026-02-17.csv
                   │ rules.yaml  │──── drives segmentation logic                  └── logs/
                   └─────────────┘                                                    └── 2026-02-17_143000_generation.log
                   ┌──────────────────┐
                   │ promo_materials/  │
                   │ links.yaml       │──── drives PDF link assignment
                   └──────────────────┘
                   ┌──────────────────┐
                   │ templates/       │
                   │ {company}/       │
                   │   {segment}.txt  │──── Jinja2 email templates
                   └──────────────────┘
```

---

## 2. Directory Structure

```
gruppenwerk-email-generator/
├── main.py                         # Click CLI entry point
├── config.yaml                     # App configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore
├── CLAUDE.md                       # Coding rules for Claude Code
├── README.md
│
├── data/
│   ├── input/                      # Drop Apollo.io CSVs here
│   │   └── .gitkeep
│   └── output/                     # Generated Instantly CSVs land here
│       ├── logs/                   # Run logs
│       └── .gitkeep
│
├── templates/                      # Jinja2 email templates
│   ├── seehafer_elemente/
│   │   ├── hausverwaltung.txt
│   │   ├── gewerbe.txt
│   │   └── oeffentlich.txt
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
│   └── links.yaml                  # PDF links per company & segment
│
├── segments/
│   └── rules.yaml                  # Segmentation rules (YAML, not code)
│
├── generator/                      # Core Python package
│   ├── __init__.py
│   ├── csv_reader.py               # Step 1: Read & validate Apollo CSV
│   ├── segmenter.py                # Step 2: Assign companies + template types
│   ├── template_engine.py          # Step 3a: Load & render Jinja2 templates
│   ├── ai_personalizer.py          # Step 3b: Claude API icebreaker generation
│   ├── pdf_linker.py               # Step 3c: Assign promo material links
│   └── csv_exporter.py             # Step 4: Export Instantly-compatible CSVs
│
└── tests/
    ├── __init__.py
    ├── conftest.py                 # Shared fixtures (sample DataFrames, configs)
    ├── fixtures/
    │   └── sample_apollo.csv       # Test input data
    ├── test_csv_reader.py
    ├── test_segmenter.py
    ├── test_template_engine.py
    ├── test_ai_personalizer.py
    ├── test_pdf_linker.py
    └── test_csv_exporter.py
```

---

## 3. Module Design

### 3.1 `main.py` — CLI Entry Point

**Responsibility:** Orchestrate the pipeline, handle CLI arguments via Click.

```python
# Commands (Click groups):
#
# python main.py generate --input <csv> [--no-ai] [--company <name>]
#   → Full pipeline: read → segment → build emails → export
#
# python main.py segment --input <csv>
#   → Dry run: show segmentation results only (no emails)
#
# python main.py preview --input <csv> --count 5
#   → Generate first N leads and print to stdout
#
# python main.py stats --output <dir>
#   → Show statistics from previous runs
```

**Pipeline orchestration (pseudocode):**

```python
def generate(input_path, no_ai, company_filter):
    config = load_config("config.yaml")

    # Step 1: Read & validate
    leads_df = csv_reader.read_and_validate(input_path)

    # Step 2: Deduplicate
    leads_df = csv_reader.deduplicate(leads_df)

    # Step 3: Segment
    rules = load_yaml("segments/rules.yaml")
    assignments = segmenter.assign_all(leads_df, rules, company_filter)
    # assignments = list of (lead_row, company_id, segment_id) tuples

    # Step 4: Build emails (async batch)
    pdf_links = load_yaml("promo_materials/links.yaml")
    results = []
    for batch in chunked(assignments, config.batch_size):
        icebreakers = ai_personalizer.generate_batch(batch, config) if not no_ai
                      else ai_personalizer.fallback_batch(batch)
        for (lead, company, segment), icebreaker in zip(batch, icebreakers):
            template = template_engine.render(company, segment, lead, icebreaker)
            pdf_link = pdf_linker.resolve(company, segment, pdf_links)
            results.append(build_output_row(lead, template, icebreaker, pdf_link, company, segment))

    # Step 5: Export
    output_df = pd.DataFrame(results)
    csv_exporter.export(output_df, config.output_directory)

    # Step 6: Log summary
    log_summary(output_df)
```

---

### 3.2 `generator/csv_reader.py` — Input Handling

**Responsibility:** Read Apollo.io CSV, validate required fields, clean data.

| Function | Input | Output | Notes |
|----------|-------|--------|-------|
| `read_and_validate(path)` | File path | `pd.DataFrame` | Validates required cols exist |
| `deduplicate(df)` | DataFrame | DataFrame | Dedup on `email` column |
| `validate_emails(df)` | DataFrame | DataFrame | RFC 5322 check, drops invalid |
| `clean_data(df)` | DataFrame | DataFrame | Strip whitespace, normalize nulls |

**Required columns (fail if missing):** `first_name`, `last_name`, `email`, `title`, `company_name`, `industry`

**Optional columns (fill with empty if missing):** `company_size`, `city`, `state`, `country`, `company_linkedin_url`, `person_linkedin_url`, etc.

---

### 3.3 `generator/segmenter.py` — Lead Segmentation

**Responsibility:** Two-pass segmentation driven entirely by `segments/rules.yaml`.

**Pass 1 — Primary (which companies?):**
- For each lead, check against each company's rules
- A lead can match **multiple** companies → produces multiple output rows
- Matching criteria: `branchen` (industry list), `jobtitel_keywords` (substring match on title), `unternehmensgröße_min` (company_size threshold)
- All three criteria are OR'd within a category but the result is a weighted score

**Pass 2 — Secondary (which template within that company?):**
- Based on industry, company_size, keywords, title
- Template hierarchy with fallback: try specific match first, fall back to `hausverwaltung` as default

| Function | Input | Output |
|----------|-------|--------|
| `assign_all(df, rules, filter)` | DataFrame + rules dict | `list[Assignment]` |
| `match_company(lead, company_rules)` | Series + dict | `bool` + score |
| `determine_segment(lead, company_id)` | Series + str | segment_id string |

**`Assignment` dataclass:**
```python
@dataclass
class Assignment:
    lead: pd.Series          # Original lead data
    company_id: str          # e.g. "seehafer_elemente"
    segment_id: str          # e.g. "hausverwaltung"
    match_score: float       # Confidence score for sorting/debugging
```

---

### 3.4 `generator/template_engine.py` — Email Rendering

**Responsibility:** Load Jinja2 templates, render with lead data + icebreaker.

**Template location convention:** `templates/{company_id}/{segment_id}.txt`

**Template format (Jinja2):**
```
Betreff: {{ subject_line }}

Hallo {{ first_name }},

{{ icebreaker }}

{{ body }}

{{ pdf_link }}

Beste Grüße
{{ sender_name }}
{{ company_display_name }} | Ein Unternehmen von Gruppenwerk
```

| Function | Input | Output |
|----------|-------|--------|
| `render(company_id, segment_id, lead, icebreaker, pdf_link, config)` | IDs + data | `RenderedEmail` |
| `load_template(company_id, segment_id)` | IDs | Jinja2 Template |
| `extract_subject(rendered)` | Rendered text | subject_line string |

**`RenderedEmail` dataclass:**
```python
@dataclass
class RenderedEmail:
    subject_line: str
    body: str                # Full email body (without subject)
    icebreaker: str
    pdf_link: str
```

---

### 3.5 `generator/ai_personalizer.py` — Icebreaker Generation

**Responsibility:** Generate personalized icebreakers via Claude API with async batching, or fall back to rule-based templates.

**Architecture:**
- Uses `anthropic.AsyncAnthropic` client for parallel API calls
- Processes leads in configurable batches (default: 50)
- Rate limiting: configurable delay between batches
- Retry logic: 3 retries with exponential backoff per call
- Graceful fallback: if API call fails after retries, use rule-based icebreaker for that lead

| Function | Input | Output |
|----------|-------|--------|
| `generate_batch(assignments, config)` | list[Assignment] + config | list[str] (icebreakers) |
| `generate_single(assignment, client)` | Assignment + client | str |
| `fallback_batch(assignments)` | list[Assignment] | list[str] |
| `fallback_single(assignment)` | Assignment | str |
| `build_prompt(assignment)` | Assignment | str (prompt text) |

**API details:**
- Model: `claude-sonnet-4-5-20250929` (configurable in config.yaml)
- Max tokens: 150 (icebreakers are short)
- Temperature: 0.7 (some creativity, but controlled)

**Async flow:**
```python
async def generate_batch(assignments, config):
    client = anthropic.AsyncAnthropic()
    semaphore = asyncio.Semaphore(config.batch_size)

    async def generate_one(assignment):
        async with semaphore:
            try:
                response = await client.messages.create(...)
                return response.content[0].text
            except Exception:
                return fallback_single(assignment)

    tasks = [generate_one(a) for a in assignments]
    return await asyncio.gather(*tasks)
```

---

### 3.6 `generator/pdf_linker.py` — Promo Material Assignment

**Responsibility:** Resolve the correct PDF link for a company + segment combo from `promo_materials/links.yaml`.

**Logic:** Try segment-specific link first, fall back to company `default`.

| Function | Input | Output |
|----------|-------|--------|
| `resolve(company_id, segment_id, links_config)` | IDs + config dict | URL string |

```python
def resolve(company_id: str, segment_id: str, links: dict) -> str:
    company_links = links.get(company_id, {})
    return company_links.get(segment_id, company_links.get("default", ""))
```

---

### 3.7 `generator/csv_exporter.py` — Output

**Responsibility:** Export results as Instantly.ai-compatible CSV files, one per campaign.

**Output columns (per PRD §4.2):**
`email`, `first_name`, `last_name`, `company_name`, `personalization`, `icebreaker`, `subject_line`, `pdf_link`, `campaign_id`, `segment`, `custom_variable_1`, `custom_variable_2`

| Function | Input | Output |
|----------|-------|--------|
| `export(df, output_dir)` | DataFrame + path | Writes CSV files |
| `split_by_campaign(df)` | DataFrame | dict[campaign_id, DataFrame] |
| `validate_output(df)` | DataFrame | bool + errors |

**File naming:** `{company_id}_{date}.csv` (e.g., `seehafer_elemente_2026-02-17.csv`)

---

## 4. Configuration Architecture

All business logic is **data-driven via YAML**, not hardcoded.

### 4.1 `config.yaml` — App Settings

Controls API behavior, paths, processing parameters. See PRD §9 for full spec.

### 4.2 `segments/rules.yaml` — Segmentation Rules

Defines which industries, job title keywords, and company sizes map to which Gruppenwerk company. Adding a new company = adding a new YAML block, zero code changes.

### 4.3 `promo_materials/links.yaml` — PDF Links

Maps (company, segment) pairs to URLs. Adding new materials = editing YAML.

### 4.4 `templates/{company}/{segment}.txt` — Email Templates

Jinja2 plain text files. Each template is self-contained with subject line + body. Non-developers can edit these without touching Python.

---

## 5. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **1:N lead expansion** | One lead can produce multiple output rows (one per matching company) | PRD §5.1: "Ein Lead kann für mehrere Firmen relevant sein" |
| **Async API calls** | `asyncio` + `anthropic.AsyncAnthropic` with semaphore-based concurrency | Needed for 500+ leads/hour target (KPI from PRD §16) |
| **Config over code** | All segmentation rules, PDF links, and templates are external files | Non-developers (Axel) can adjust targeting without code changes |
| **Graceful degradation** | AI failure → rule-based fallback per individual lead, not entire batch | Never lose a lead due to API issues |
| **pandas throughout** | DataFrame is the core data structure from input to output | Natural fit for CSV-to-CSV pipeline, easy filtering/grouping |
| **One CSV per campaign** | Separate output file per Gruppenwerk company | Maps directly to Instantly.ai campaign structure |
| **Jinja2 templates** | Full template engine with conditionals/filters | Templates can grow in complexity without code changes |

---

## 6. Error Handling Strategy

```
Level 1: Validation errors (bad CSV, missing fields)
    → Log warning, skip individual lead, continue processing
    → Summary at end: "Skipped 12 leads (3 missing email, 9 invalid format)"

Level 2: API errors (Claude API failures)
    → Retry 3x with exponential backoff
    → After 3 failures: fall back to rule-based icebreaker for THAT lead
    → Log warning, never abort the batch

Level 3: Configuration errors (missing template, broken YAML)
    → Fail fast with clear error message
    → These are setup problems, not runtime problems

Level 4: Fatal errors (no input file, no API key when ai_enabled=true)
    → Exit with non-zero code and descriptive message
```

---

## 7. Testing Strategy

| Layer | What | How |
|-------|------|-----|
| **Unit tests** | Each module in isolation | pytest + fixtures with sample DataFrames |
| **Integration test** | Full pipeline with `--no-ai` | `sample_apollo.csv` → expected output CSV |
| **AI mock test** | Pipeline with mocked Claude API | Verify prompt construction, response handling |

**Key test fixtures:**
- `tests/fixtures/sample_apollo.csv` — 10-20 representative leads covering all segments
- `tests/conftest.py` — Shared DataFrame fixtures, mock configs

**Test commands:**
```bash
pytest tests/ -v                                              # All tests
pytest tests/test_segmenter.py -v                             # Single module
python main.py generate --input tests/fixtures/sample_apollo.csv --no-ai  # E2E smoke test
```

---

## 8. Dependencies

```
pandas>=2.0.0           # CSV read/write, DataFrame operations
pyyaml>=6.0             # Config and rules parsing
anthropic>=0.40.0       # Claude API client (includes async)
jinja2>=3.1.0           # Email template rendering
click>=8.0.0            # CLI framework
email-validator>=2.0.0  # RFC 5322 email validation
pytest>=7.0.0           # Testing
```

No web framework, no database, no ORM. This is a lean CLI tool.
