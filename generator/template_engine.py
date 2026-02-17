"""Template-Auswahl und Rendering mit Jinja2."""

import logging
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)


@dataclass
class RenderedEmail:
    """Ergebnis eines gerenderten E-Mail-Templates."""

    subject_line: str
    body: str
    icebreaker: str
    pdf_link: str


def create_environment(templates_dir: str | Path) -> Environment:
    """Erstellt eine Jinja2-Umgebung für die Templates.

    Args:
        templates_dir: Pfad zum Templates-Verzeichnis.

    Returns:
        Konfigurierte Jinja2 Environment.
    """
    templates_dir = Path(templates_dir)
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates-Verzeichnis nicht gefunden: {templates_dir}")

    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
    )


def render(
    company_id: str,
    segment_id: str,
    lead: dict,
    icebreaker: str,
    pdf_link: str,
    sender_name: str,
    env: Environment,
) -> RenderedEmail:
    """Rendert ein E-Mail-Template mit den Lead-Daten.

    Args:
        company_id: Firma-ID (z.B. "seehafer_elemente").
        segment_id: Segment-ID (z.B. "hausverwaltung").
        lead: Lead-Daten als Dict.
        icebreaker: Generierter Icebreaker-Text.
        pdf_link: URL zum Promo-Material.
        sender_name: Name des Absenders.
        env: Jinja2 Environment.

    Returns:
        RenderedEmail mit Betreffzeile und Body.

    Raises:
        TemplateNotFound: Wenn das Template nicht existiert.
    """
    template_path = f"{company_id}/{segment_id}.txt"

    try:
        template = env.get_template(template_path)
    except TemplateNotFound:
        logger.error(f"Template nicht gefunden: {template_path}")
        raise

    # Template-Variablen zusammenbauen
    context = {
        **lead,
        "icebreaker": icebreaker,
        "pdf_link": pdf_link,
        "sender_name": sender_name,
    }

    rendered = template.render(**context)

    # Betreffzeile und Body trennen
    subject_line, body = _split_subject_and_body(rendered)

    return RenderedEmail(
        subject_line=subject_line,
        body=body,
        icebreaker=icebreaker,
        pdf_link=pdf_link,
    )


def _split_subject_and_body(rendered: str) -> tuple[str, str]:
    """Trennt Betreffzeile und Body aus dem gerenderten Template.

    Erwartet Format:
        Betreff: <betreffzeile>

        <body>

    Args:
        rendered: Komplett gerenderter Template-Text.

    Returns:
        Tuple (subject_line, body).
    """
    lines = rendered.strip().split("\n")

    subject_line = ""
    body_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower().startswith("betreff:"):
            subject_line = stripped[len("Betreff:"):].strip()
            # Body beginnt nach der nächsten Leerzeile
            body_start = i + 1
            while body_start < len(lines) and not lines[body_start].strip():
                body_start += 1
            break

    body = "\n".join(lines[body_start:]).strip()

    if not subject_line:
        logger.warning("Keine Betreffzeile im Template gefunden")

    return subject_line, body
