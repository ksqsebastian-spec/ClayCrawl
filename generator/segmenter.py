"""Lead-Segmentierung: Zuordnung zu Gruppenwerk-Firmen und Template-Typen."""

import logging
import re
from dataclasses import dataclass, field

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class Assignment:
    """Ein Lead zugeordnet zu einer Firma und einem Template-Segment."""

    lead: pd.Series
    company_id: str
    segment_id: str
    match_score: float = 0.0


def assign_all(
    df: pd.DataFrame,
    rules: dict,
    company_filter: str | None = None,
) -> list[Assignment]:
    """Weist alle Leads den passenden Firmen und Segmenten zu.

    Args:
        df: DataFrame mit Lead-Daten.
        rules: Geladene Segmentierungsregeln aus rules.yaml.
        company_filter: Optional — nur für diese Firma zuordnen.

    Returns:
        Liste von Assignments (ein Lead kann mehrfach vorkommen).
    """
    segmentation_rules = rules.get("segmentierung", {})
    template_rules = rules.get("template_auswahl", {})
    assignments: list[Assignment] = []

    companies = segmentation_rules.keys()
    if company_filter:
        if company_filter not in companies:
            raise ValueError(
                f"Unbekannte Firma: '{company_filter}'. "
                f"Verfügbar: {', '.join(companies)}"
            )
        companies = [company_filter]

    for _, lead in df.iterrows():
        for company_id in companies:
            company_rules = segmentation_rules[company_id]
            matched, score = match_company(lead, company_rules)

            if matched:
                segment_id = determine_segment(
                    lead, company_id, company_rules, template_rules
                )
                assignments.append(
                    Assignment(
                        lead=lead,
                        company_id=company_id,
                        segment_id=segment_id,
                        match_score=score,
                    )
                )

    # Statistiken loggen
    _log_statistics(assignments, len(df))

    return assignments


def match_company(
    lead: pd.Series, company_rules: dict
) -> tuple[bool, float]:
    """Prüft ob ein Lead zu einer Firma passt.

    Kriterien (gewichtet):
    - Branche des Leads in Firmenliste (0.5)
    - Jobtitel enthält relevante Keywords (0.3)
    - Unternehmensgröße über Minimum (0.2)

    Args:
        lead: Einzelne Lead-Zeile.
        company_rules: Regeln für eine Firma.

    Returns:
        Tuple (matched: bool, score: float).
    """
    score = 0.0

    # Branche prüfen
    lead_industry = lead.get("industry", "").strip()
    target_industries = company_rules.get("branchen", [])
    if _matches_any(lead_industry, target_industries):
        score += 0.5

    # Jobtitel prüfen
    lead_title = lead.get("title", "").strip()
    title_keywords = company_rules.get("jobtitel_keywords", [])
    if _title_matches_keywords(lead_title, title_keywords):
        score += 0.3

    # Unternehmensgröße prüfen
    min_size = company_rules.get("unternehmensgroesse_min", 0)
    lead_size = _parse_company_size(lead.get("company_size", ""))
    if lead_size >= min_size:
        score += 0.2

    # Mindestens ein Kriterium muss matchen (Branche oder Jobtitel)
    matched = score >= 0.5
    return matched, score


def determine_segment(
    lead: pd.Series,
    company_id: str,
    company_rules: dict,
    template_rules: dict,
) -> str:
    """Bestimmt das Template-Segment für einen Lead innerhalb einer Firma.

    Prüft Sekundärsegmente in Prioritätsreihenfolge.
    Fällt auf das Default-Template der Firma zurück.

    Args:
        lead: Einzelne Lead-Zeile.
        company_id: ID der zugeordneten Firma.
        company_rules: Regeln der zugeordneten Firma.
        template_rules: Sekundäre Segmentierungsregeln.

    Returns:
        Segment-ID (z.B. "hausverwaltung", "denkmalschutz").
    """
    available_templates = company_rules.get("templates", [])
    default_template = company_rules.get("default_template", "hausverwaltung")

    lead_industry = lead.get("industry", "").strip()
    lead_title = lead.get("title", "").strip()
    lead_keywords = lead.get("keywords", "").strip()
    lead_size = _parse_company_size(lead.get("company_size", ""))
    lead_company = lead.get("company_name", "").strip()

    # Prüfe jedes Sekundärsegment in Reihenfolge
    for segment_id, segment_rules in template_rules.items():
        if segment_id not in available_templates:
            continue

        conditions = segment_rules.get("bedingungen", {})

        # Denkmalschutz: Keywords oder Branche
        keywords_check = conditions.get("keywords_enthalten", [])
        if keywords_check:
            combined_text = f"{lead_industry} {lead_title} {lead_keywords}"
            if _text_contains_any(combined_text, keywords_check):
                return segment_id

        # Branche prüfen
        branchen_check = conditions.get("branchen_enthalten", [])
        if branchen_check and _matches_any(lead_industry, branchen_check):
            # Zusätzliche Titel-Bedingung für "bauunternehmen"
            titel_check = conditions.get("titel_enthalten", [])
            if titel_check:
                if _title_matches_keywords(lead_title, titel_check):
                    return segment_id
                continue
            return segment_id

        # Unternehmensgröße-Bedingungen
        size_min = conditions.get("unternehmensgroesse_min")
        if size_min is not None and lead_size >= size_min:
            return segment_id

        size_max = conditions.get("unternehmensgroesse_max")
        if size_max is not None and lead_size > 0 and lead_size <= size_max:
            return segment_id

        # Kein Firmenname
        if conditions.get("kein_firmenname") and not lead_company:
            return segment_id

    return default_template


def _matches_any(value: str, targets: list[str]) -> bool:
    """Prüft ob ein Wert (case-insensitive) in einer Liste enthalten ist."""
    value_lower = value.lower()
    return any(target.lower() in value_lower for target in targets)


def _title_matches_keywords(title: str, keywords: list[str]) -> bool:
    """Prüft ob ein Jobtitel eines der Keywords enthält (case-insensitive)."""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def _text_contains_any(text: str, keywords: list[str]) -> bool:
    """Prüft ob ein Text eines der Keywords enthält (case-insensitive)."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _parse_company_size(size_str: str) -> int:
    """Extrahiert eine Zahl aus dem company_size Feld.

    Versteht Formate wie: "51-200", "200+", "200", "51 - 200".

    Args:
        size_str: Rohwert aus der CSV.

    Returns:
        Untere Grenze als Integer, oder 0 wenn nicht parsbar.
    """
    if not size_str:
        return 0

    # Erste Zahl aus dem String extrahieren
    match = re.search(r"\d+", size_str.replace(",", "").replace(".", ""))
    if match:
        return int(match.group())
    return 0


def _log_statistics(assignments: list[Assignment], total_leads: int) -> None:
    """Loggt Segmentierungsstatistiken."""
    if not assignments:
        logger.warning("Keine Leads konnten zugeordnet werden")
        return

    # Leads mit mindestens einer Zuordnung
    unique_emails = {a.lead["email"] for a in assignments}
    unmatched = total_leads - len(unique_emails)

    logger.info(f"Segmentierung: {len(assignments)} Zuordnungen für {len(unique_emails)} Leads")

    if unmatched > 0:
        logger.warning(f"{unmatched} Leads ohne Zuordnung (keiner Firma zugewiesen)")

    # Pro Firma
    company_counts: dict[str, int] = {}
    for a in assignments:
        company_counts[a.company_id] = company_counts.get(a.company_id, 0) + 1

    for company_id, count in sorted(company_counts.items()):
        logger.info(f"  → {company_id}: {count} Leads")
