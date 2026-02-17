"""Gemeinsame Fixtures für alle Tests."""

from pathlib import Path

import pandas as pd
import pytest
import yaml


FIXTURES_DIR = Path(__file__).parent / "fixtures"
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def sample_csv_path() -> Path:
    """Pfad zur Beispiel-Apollo-CSV."""
    return FIXTURES_DIR / "sample_apollo.csv"


@pytest.fixture
def sample_lead() -> pd.Series:
    """Ein einzelner Beispiel-Lead als pd.Series."""
    return pd.Series({
        "first_name": "Max",
        "last_name": "Müller",
        "email": "max.mueller@abc-hausverwaltung.de",
        "title": "Facility Manager",
        "company_name": "ABC Hausverwaltung GmbH",
        "industry": "Real Estate",
        "company_size": "51-200",
        "company_revenue": "$10M-$50M",
        "city": "Hamburg",
        "state": "Hamburg",
        "country": "Germany",
        "company_linkedin_url": "",
        "person_linkedin_url": "",
        "technologies": "",
        "keywords": "",
        "seniority": "Manager",
        "departments": "Operations",
        "company_website": "https://abc-hv.de",
    })


@pytest.fixture
def sample_leads_df(sample_csv_path: Path) -> pd.DataFrame:
    """DataFrame mit Beispiel-Leads (roh, nicht bereinigt)."""
    return pd.read_csv(sample_csv_path, dtype=str).fillna("")


@pytest.fixture
def segmentation_rules() -> dict:
    """Geladene Segmentierungsregeln."""
    rules_path = PROJECT_ROOT / "segments" / "rules.yaml"
    with open(rules_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def pdf_links() -> dict:
    """Geladene PDF-Links-Konfiguration."""
    links_path = PROJECT_ROOT / "promo_materials" / "links.yaml"
    with open(links_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def config() -> dict:
    """Geladene App-Konfiguration."""
    config_path = PROJECT_ROOT / "config.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
