"""Export der generierten E-Mails als Instantly.ai-kompatible CSV-Dateien."""

import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Spaltenreihenfolge für Instantly.ai CSV
INSTANTLY_COLUMNS = [
    "email",
    "first_name",
    "last_name",
    "company_name",
    "personalization",
    "icebreaker",
    "subject_line",
    "pdf_link",
    "campaign_id",
    "segment",
    "custom_variable_1",
    "custom_variable_2",
]


def build_output_row(
    lead: dict,
    rendered_body: str,
    subject_line: str,
    icebreaker: str,
    pdf_link: str,
    company_id: str,
    segment_id: str,
    campaign_prefix: str = "gruppenwerk",
) -> dict:
    """Baut eine Ausgabezeile für die Instantly CSV.

    Args:
        lead: Lead-Daten als Dict.
        rendered_body: Gerenderter E-Mail-Body.
        subject_line: Betreffzeile.
        icebreaker: Icebreaker-Text.
        pdf_link: URL zum Promo-Material.
        company_id: Firma-ID.
        segment_id: Segment-ID.
        campaign_prefix: Prefix für die Campaign-ID.

    Returns:
        Dict mit allen Instantly-Spalten.
    """
    return {
        "email": lead.get("email", ""),
        "first_name": lead.get("first_name", ""),
        "last_name": lead.get("last_name", ""),
        "company_name": lead.get("company_name", ""),
        "personalization": rendered_body,
        "icebreaker": icebreaker,
        "subject_line": subject_line,
        "pdf_link": pdf_link,
        "campaign_id": f"{campaign_prefix}_{company_id}",
        "segment": segment_id,
        "custom_variable_1": lead.get("industry", ""),
        "custom_variable_2": lead.get("city", ""),
    }


def export(
    df: pd.DataFrame,
    output_dir: str | Path,
    separator: str = ",",
    encoding: str = "utf-8",
) -> list[Path]:
    """Exportiert die Ergebnisse als Instantly-CSVs, eine pro Kampagne.

    Args:
        df: DataFrame mit allen generierten E-Mails.
        output_dir: Ausgabeverzeichnis.
        separator: CSV-Trennzeichen.
        encoding: Datei-Encoding.

    Returns:
        Liste der geschriebenen Dateipfade.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if df.empty:
        logger.warning("Keine Daten zum Exportieren")
        return []

    # Validierung
    valid_df = validate_output(df)

    # Nach Kampagne aufteilen
    campaigns = split_by_campaign(valid_df)
    date_str = datetime.now().strftime("%Y-%m-%d")
    written_files: list[Path] = []

    for campaign_id, campaign_df in campaigns.items():
        # Firmen-ID aus campaign_id extrahieren (z.B. "gruppenwerk_seehafer_elemente")
        filename = f"{campaign_id}_{date_str}.csv"
        filepath = output_dir / filename

        # Nur definierte Spalten exportieren
        export_df = campaign_df.reindex(columns=INSTANTLY_COLUMNS, fill_value="")
        export_df.to_csv(filepath, index=False, sep=separator, encoding=encoding)

        logger.info(f"Exportiert: {filepath} ({len(export_df)} Leads)")
        written_files.append(filepath)

    logger.info(f"Gesamt: {len(valid_df)} E-Mails in {len(written_files)} Dateien exportiert")
    return written_files


def split_by_campaign(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Teilt einen DataFrame nach campaign_id auf.

    Args:
        df: DataFrame mit 'campaign_id' Spalte.

    Returns:
        Dict mit campaign_id als Key und Teil-DataFrame als Value.
    """
    campaigns: dict[str, pd.DataFrame] = {}
    for campaign_id, group_df in df.groupby("campaign_id"):
        campaigns[str(campaign_id)] = group_df.reset_index(drop=True)
    return campaigns


def validate_output(df: pd.DataFrame) -> pd.DataFrame:
    """Validiert die Ausgabedaten vor dem Export.

    Prüft:
    - Pflichtfelder vorhanden
    - E-Mail-Body Mindestlänge (100 Zeichen)
    - Keine doppelten E-Mails pro Kampagne

    Args:
        df: DataFrame mit Ausgabedaten.

    Returns:
        Validierter DataFrame (ungültige Zeilen entfernt).
    """
    initial_count = len(df)
    issues: list[str] = []

    # Pflichtfelder prüfen
    required = ["email", "personalization", "subject_line"]
    for col in required:
        if col not in df.columns:
            issues.append(f"Spalte '{col}' fehlt")
            continue
        empty_count = (df[col] == "").sum()
        if empty_count > 0:
            issues.append(f"{empty_count} leere Werte in '{col}'")
            df = df[df[col] != ""]

    # Mindestlänge für E-Mail-Body
    if "personalization" in df.columns:
        too_short = df["personalization"].str.len() < 100
        short_count = too_short.sum()
        if short_count > 0:
            issues.append(f"{short_count} E-Mails unter 100 Zeichen")
            df = df[~too_short]

    # Duplikate pro Kampagne entfernen
    if "campaign_id" in df.columns and "email" in df.columns:
        before_dedup = len(df)
        df = df.drop_duplicates(subset=["campaign_id", "email"], keep="first")
        dedup_count = before_dedup - len(df)
        if dedup_count > 0:
            issues.append(f"{dedup_count} Duplikate entfernt")

    # Ergebnis loggen
    removed = initial_count - len(df)
    if issues:
        for issue in issues:
            logger.warning(f"Validierung: {issue}")
    if removed > 0:
        logger.warning(f"Validierung: {removed} Zeilen entfernt")

    return df.reset_index(drop=True)
