"""Apollo.io CSV einlesen, validieren und bereinigen."""

import logging
from pathlib import Path

import pandas as pd
from email_validator import EmailNotValidError, validate_email

logger = logging.getLogger(__name__)

# Pflichtfelder — ohne diese wird der Lead übersprungen
REQUIRED_COLUMNS = [
    "first_name",
    "last_name",
    "email",
    "title",
    "company_name",
    "industry",
]

# Optionale Felder — werden mit leerem String aufgefüllt falls fehlend
OPTIONAL_COLUMNS = [
    "company_size",
    "company_revenue",
    "city",
    "state",
    "country",
    "company_linkedin_url",
    "person_linkedin_url",
    "technologies",
    "keywords",
    "seniority",
    "departments",
    "company_website",
]


def read_and_validate(path: str | Path) -> pd.DataFrame:
    """Liest Apollo.io CSV ein und validiert die Struktur.

    Args:
        path: Pfad zur CSV-Datei.

    Returns:
        Bereinigter DataFrame mit allen Pflicht- und optionalen Spalten.

    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert.
        ValueError: Wenn Pflichtspalten fehlen.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Eingabedatei nicht gefunden: {path}")

    logger.info(f"Lese CSV: {path}")
    df = pd.read_csv(path, dtype=str)
    df = df.fillna("")

    # Pflichtspalten prüfen
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Pflichtspalten fehlen in der CSV: {', '.join(missing)}"
        )

    # Optionale Spalten ergänzen
    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = clean_data(df)
    df = validate_emails(df)

    logger.info(f"{len(df)} gültige Leads geladen")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bereinigt Daten: Whitespace entfernen, leere Pflichtfelder filtern.

    Args:
        df: Roher DataFrame.

    Returns:
        Bereinigter DataFrame (Leads mit leeren Pflichtfeldern entfernt).
    """
    # Whitespace entfernen
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    # Leads ohne Pflichtfelder entfernen
    initial_count = len(df)
    for col in ["first_name", "email", "company_name"]:
        df = df[df[col] != ""]

    skipped = initial_count - len(df)
    if skipped > 0:
        logger.warning(
            f"{skipped} Leads übersprungen — fehlende Pflichtfelder "
            f"(first_name, email oder company_name)"
        )

    return df.reset_index(drop=True)


def validate_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Prüft E-Mail-Adressen auf gültiges Format (RFC 5322).

    Args:
        df: DataFrame mit 'email' Spalte.

    Returns:
        DataFrame nur mit gültigen E-Mail-Adressen.
    """
    valid_mask = df["email"].apply(_is_valid_email)
    invalid_count = (~valid_mask).sum()

    if invalid_count > 0:
        invalid_emails = df.loc[~valid_mask, "email"].tolist()
        logger.warning(
            f"{invalid_count} Leads übersprungen — ungültiges E-Mail-Format: "
            f"{', '.join(invalid_emails[:5])}{'...' if invalid_count > 5 else ''}"
        )

    return df[valid_mask].reset_index(drop=True)


def _is_valid_email(email: str) -> bool:
    """Prüft eine einzelne E-Mail-Adresse."""
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Entfernt doppelte Leads basierend auf E-Mail-Adresse.

    Args:
        df: DataFrame mit 'email' Spalte.

    Returns:
        DataFrame ohne Duplikate (erster Eintrag wird behalten).
    """
    initial_count = len(df)
    df = df.drop_duplicates(subset=["email"], keep="first").reset_index(drop=True)
    removed = initial_count - len(df)

    if removed > 0:
        logger.info(f"{removed} Duplikate entfernt (basierend auf E-Mail)")

    return df
