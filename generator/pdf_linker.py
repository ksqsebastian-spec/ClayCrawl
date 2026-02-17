"""Promo-Material-Zuordnung: PDF-Links für Firma + Segment auflösen."""

import logging

logger = logging.getLogger(__name__)


def resolve(company_id: str, segment_id: str, links: dict) -> str:
    """Löst den passenden PDF-Link für eine Firma + Segment Kombination auf.

    Priorität:
    1. Segment-spezifischer Link (z.B. seehafer_elemente.hausverwaltung)
    2. Default-Link der Firma (z.B. seehafer_elemente.default)
    3. Leerer String (kein Link verfügbar)

    Args:
        company_id: Firma-ID (z.B. "seehafer_elemente").
        segment_id: Segment-ID (z.B. "hausverwaltung").
        links: PDF-Links-Konfiguration aus links.yaml.

    Returns:
        URL-String oder leerer String.
    """
    company_links = links.get(company_id)
    if company_links is None:
        logger.warning(f"Keine PDF-Links für Firma '{company_id}' konfiguriert")
        return ""

    # Segment-spezifisch versuchen
    link = company_links.get(segment_id)
    if link:
        return link

    # Fallback auf Default
    default_link = company_links.get("default", "")
    if default_link:
        logger.debug(
            f"Kein Link für {company_id}/{segment_id} — nutze Default-Link"
        )
    else:
        logger.warning(
            f"Kein PDF-Link für {company_id}/{segment_id} und kein Default vorhanden"
        )

    return default_link
