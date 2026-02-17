"""KI-basierte Icebreaker-Generierung mit Claude API."""

import asyncio
import logging
import os

import anthropic

from generator.segmenter import Assignment

logger = logging.getLogger(__name__)

# Prompt-Template für die Icebreaker-Generierung
ICEBREAKER_PROMPT = """Du bist ein deutscher Vertriebstexter für ein Handwerksunternehmen aus Hamburg.

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
- Kein "Sehr geehrte/r" — starte direkt mit dem Inhalt nach "Hallo {{first_name}},"

Beispiele für gute Icebreaker:
- "als Facility Manager bei einer der größeren Hamburger Hausverwaltungen wissen Sie, wie wichtig kurze Reaktionszeiten bei Reparaturen sind."
- "wir arbeiten bereits mit mehreren Hausverwaltungen im Raum Hamburg zusammen und haben gesehen, dass bei der Fassadensanierung häufig Gerüstbau-Kapazitäten der Engpass sind."
- "mit über 200 Mitarbeitern und einem wachsenden Immobilienbestand stehen bei {{company_name}} vermutlich regelmäßig Instandhaltungsthemen auf der Agenda."

Schreibe NUR den Icebreaker, nichts anderes."""

# Regelbasierte Fallback-Icebreaker
FALLBACK_ICEBREAKERS: dict[str, str] = {
    "hausverwaltung": (
        "als {title} bei {company_name} haben Sie sicher regelmäßig mit "
        "Instandhaltungsthemen zu tun — von Türen über Fenster bis zur Fassade."
    ),
    "bauunternehmen": (
        "bei Bauprojekten in Hamburg kommt es auf zuverlässige Partner an, "
        "die pünktlich liefern und Qualität garantieren."
    ),
    "oeffentlich": (
        "öffentliche Gebäude stellen besondere Anforderungen an Qualität, "
        "Sicherheit und Vergabekonformität — genau darauf haben wir uns spezialisiert."
    ),
    "denkmalschutz": (
        "die Arbeit an denkmalgeschützten Gebäuden erfordert besonderes "
        "Fingerspitzengefühl und Erfahrung — beides bringen wir seit Jahrzehnten mit."
    ),
    "gewerbe": (
        "für gewerbliche Immobilien mit hoher Nutzungsfrequenz sind schnelle "
        "und professionelle Handwerksleistungen unverzichtbar."
    ),
    "privat": (
        "für Ihr Bau- oder Sanierungsprojekt möchten wir Ihnen eine "
        "unkomplizierte und professionelle Zusammenarbeit anbieten."
    ),
}


def build_prompt(assignment: Assignment, rules: dict) -> str:
    """Baut den Prompt für die Claude API.

    Args:
        assignment: Lead-Zuordnung.
        rules: Segmentierungsregeln (für Firmeninfos).

    Returns:
        Fertiger Prompt-String.
    """
    lead = assignment.lead
    company_rules = rules.get("segmentierung", {}).get(assignment.company_id, {})

    return ICEBREAKER_PROMPT.format(
        first_name=lead.get("first_name", ""),
        last_name=lead.get("last_name", ""),
        title=lead.get("title", ""),
        company_name=lead.get("company_name", ""),
        industry=lead.get("industry", ""),
        company_size=lead.get("company_size", ""),
        city=lead.get("city", "Hamburg"),
        gruppenwerk_firma=company_rules.get("display_name", assignment.company_id),
        kernleistung=company_rules.get("kernleistung", ""),
    )


def fallback_single(assignment: Assignment) -> str:
    """Generiert einen regelbasierten Fallback-Icebreaker.

    Args:
        assignment: Lead-Zuordnung.

    Returns:
        Icebreaker-Text.
    """
    lead = assignment.lead
    template = FALLBACK_ICEBREAKERS.get(
        assignment.segment_id,
        FALLBACK_ICEBREAKERS["hausverwaltung"],
    )

    return template.format(
        title=lead.get("title", ""),
        company_name=lead.get("company_name", ""),
    )


def fallback_batch(assignments: list[Assignment]) -> list[str]:
    """Generiert Fallback-Icebreaker für eine Liste von Assignments.

    Args:
        assignments: Liste von Lead-Zuordnungen.

    Returns:
        Liste von Icebreaker-Texten.
    """
    return [fallback_single(a) for a in assignments]


async def generate_batch(
    assignments: list[Assignment],
    rules: dict,
    config: dict,
) -> list[str]:
    """Generiert Icebreaker per Claude API für einen Batch von Assignments.

    Nutzt asyncio für parallele API-Calls mit Concurrency-Limit.
    Bei Fehler für einzelne Leads wird auf Fallback zurückgegriffen.

    Args:
        assignments: Liste von Lead-Zuordnungen.
        rules: Segmentierungsregeln.
        config: App-Konfiguration.

    Returns:
        Liste von Icebreaker-Texten (gleiche Reihenfolge wie Eingabe).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY nicht gesetzt — nutze Fallback-Icebreaker")
        return fallback_batch(assignments)

    model = config.get("ai_model", "claude-sonnet-4-5-20250929")
    max_tokens = config.get("ai_max_tokens", 150)
    temperature = config.get("ai_temperature", 0.7)
    max_retries = config.get("ai_max_retries", 3)
    concurrency = config.get("ai_concurrency", 10)
    delay = config.get("ai_rate_limit_delay_seconds", 1)

    client = anthropic.AsyncAnthropic(api_key=api_key)
    semaphore = asyncio.Semaphore(concurrency)

    async def generate_one(assignment: Assignment) -> str:
        async with semaphore:
            prompt = build_prompt(assignment, rules)

            for attempt in range(max_retries):
                try:
                    response = await client.messages.create(
                        model=model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    text = response.content[0].text.strip()

                    # Validierung: maximal 200 Zeichen
                    if len(text) > 200:
                        text = text[:197] + "..."

                    logger.debug(
                        f"Icebreaker für {assignment.lead.get('email', '?')}: {text[:50]}..."
                    )
                    return text

                except anthropic.RateLimitError:
                    wait_time = delay * (2 ** attempt)
                    logger.warning(
                        f"Rate Limit erreicht — warte {wait_time}s "
                        f"(Versuch {attempt + 1}/{max_retries})"
                    )
                    await asyncio.sleep(wait_time)

                except anthropic.APIError as e:
                    logger.error(
                        f"API-Fehler für {assignment.lead.get('email', '?')}: {e} "
                        f"(Versuch {attempt + 1}/{max_retries})"
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)

            # Nach allen Retries: Fallback
            logger.warning(
                f"Fallback-Icebreaker für {assignment.lead.get('email', '?')} "
                f"nach {max_retries} fehlgeschlagenen Versuchen"
            )
            return fallback_single(assignment)

    tasks = [generate_one(a) for a in assignments]
    return await asyncio.gather(*tasks)
