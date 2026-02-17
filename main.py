"""Gruppenwerk Lead-E-Mail-Generator — CLI-Einstiegspunkt.

Verwandelt Apollo.io CSV-Exporte in personalisierte, segmentierte
Kaltakquise-E-Mails und exportiert sie als Instantly.ai-kompatible CSVs.
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

import click
import pandas as pd
import yaml

from generator import csv_reader, segmenter, template_engine, ai_personalizer, pdf_linker
from generator.csv_exporter import build_output_row, export


def load_yaml(path: str | Path) -> dict:
    """Lädt eine YAML-Konfigurationsdatei.

    Args:
        path: Pfad zur YAML-Datei.

    Returns:
        Geladenes Dict.

    Raises:
        FileNotFoundError: Wenn die Datei nicht existiert.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {path}")

    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def setup_logging(log_level: str, output_dir: str | Path) -> None:
    """Konfiguriert das Logging für einen Durchlauf.

    Args:
        log_level: Log-Level (DEBUG, INFO, WARNING, ERROR).
        output_dir: Verzeichnis für Log-Dateien.
    """
    log_dir = Path(output_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file = log_dir / f"{timestamp}_generation.log"

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def chunked(lst: list, size: int) -> list[list]:
    """Teilt eine Liste in Chunks gleicher Größe.

    Args:
        lst: Eingabeliste.
        size: Chunk-Größe.

    Returns:
        Liste von Chunk-Listen.
    """
    return [lst[i : i + size] for i in range(0, len(lst), size)]


@click.group()
@click.version_option(version="1.0.0")
def cli() -> None:
    """Gruppenwerk Lead-E-Mail-Generator

    Generiert personalisierte Kaltakquise-E-Mails aus Apollo.io-Daten
    für alle Gruppenwerk-Unternehmen.
    """
    pass


@cli.command()
@click.option(
    "--input", "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Pfad zur Apollo.io CSV-Datei.",
)
@click.option(
    "--no-ai",
    is_flag=True,
    default=False,
    help="Nur regelbasierte Icebreaker (keine Claude API).",
)
@click.option(
    "--company",
    default=None,
    help="Nur für diese Firma generieren (z.B. seehafer_elemente).",
)
@click.option(
    "--config-path",
    default="config.yaml",
    type=click.Path(exists=True),
    help="Pfad zur Konfigurationsdatei.",
)
def generate(input_path: str, no_ai: bool, company: str | None, config_path: str) -> None:
    """Vollständiger Durchlauf: Apollo CSV → E-Mails → Instantly CSV."""
    config = load_yaml(config_path)
    setup_logging(config.get("log_level", "INFO"), config.get("output_directory", "./data/output"))

    logger = logging.getLogger(__name__)
    logger.info("=== Gruppenwerk E-Mail-Generator gestartet ===")

    # Schritt 1: CSV einlesen & validieren
    click.echo("→ Lese Apollo CSV...")
    leads_df = csv_reader.read_and_validate(input_path)

    # Schritt 2: Duplikate entfernen
    if config.get("duplicate_check", True):
        leads_df = csv_reader.deduplicate(leads_df)

    click.echo(f"  {len(leads_df)} gültige Leads geladen")

    # Schritt 3: Segmentierung
    click.echo("→ Segmentiere Leads...")
    rules = load_yaml(config.get("segments_config", "./segments/rules.yaml"))
    assignments = segmenter.assign_all(leads_df, rules, company)
    click.echo(f"  {len(assignments)} Zuordnungen erstellt")

    if not assignments:
        click.echo("⚠ Keine Leads konnten zugeordnet werden. Abbruch.")
        return

    # Schritt 4: E-Mails generieren
    click.echo("→ Generiere E-Mails...")
    pdf_links = load_yaml(config.get("promo_materials_config", "./promo_materials/links.yaml"))
    env = template_engine.create_environment(
        config.get("templates_directory", "./templates")
    )
    sender_name = config.get("default_sender_name", "Axel Seehafer")
    batch_size = config.get("batch_size", 50)
    campaign_prefix = config.get("campaign_prefix", "gruppenwerk")

    results: list[dict] = []
    batches = chunked(assignments, batch_size)

    for batch_idx, batch in enumerate(batches, 1):
        click.echo(f"  Batch {batch_idx}/{len(batches)} ({len(batch)} Leads)...")

        # Icebreaker generieren
        if no_ai or not config.get("ai_enabled", True):
            icebreakers = ai_personalizer.fallback_batch(batch)
        else:
            icebreakers = asyncio.run(
                ai_personalizer.generate_batch(batch, rules, config)
            )

        # Templates rendern und Ausgabezeilen bauen
        for assignment, icebreaker in zip(batch, icebreakers):
            lead_dict = assignment.lead.to_dict()
            link = pdf_linker.resolve(
                assignment.company_id, assignment.segment_id, pdf_links
            )

            try:
                rendered = template_engine.render(
                    company_id=assignment.company_id,
                    segment_id=assignment.segment_id,
                    lead=lead_dict,
                    icebreaker=icebreaker,
                    pdf_link=link,
                    sender_name=sender_name,
                    env=env,
                )
            except Exception as e:
                logger.error(
                    f"Template-Fehler für {lead_dict.get('email', '?')} "
                    f"({assignment.company_id}/{assignment.segment_id}): {e}"
                )
                continue

            row = build_output_row(
                lead=lead_dict,
                rendered_body=rendered.body,
                subject_line=rendered.subject_line,
                icebreaker=icebreaker,
                pdf_link=link,
                company_id=assignment.company_id,
                segment_id=assignment.segment_id,
                campaign_prefix=campaign_prefix,
            )
            results.append(row)

    if not results:
        click.echo("⚠ Keine E-Mails generiert. Prüfe die Logs.")
        return

    # Schritt 5: Export
    click.echo("→ Exportiere Instantly CSVs...")
    output_df = pd.DataFrame(results)
    output_dir = config.get("output_directory", "./data/output")
    separator = config.get("instantly_csv_separator", ",")
    encoding = config.get("instantly_csv_encoding", "utf-8")

    written_files = export(output_df, output_dir, separator, encoding)

    # Zusammenfassung
    click.echo("")
    click.echo("=== Zusammenfassung ===")
    click.echo(f"✓ {len(results)} E-Mails generiert")
    click.echo(f"✓ {len(written_files)} CSV-Dateien exportiert:")
    for f in written_files:
        click.echo(f"  → {f}")
    click.echo("")

    logger.info(f"Durchlauf abgeschlossen: {len(results)} E-Mails, {len(written_files)} Dateien")


@cli.command()
@click.option(
    "--input", "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Pfad zur Apollo.io CSV-Datei.",
)
@click.option(
    "--config-path",
    default="config.yaml",
    type=click.Path(exists=True),
    help="Pfad zur Konfigurationsdatei.",
)
def segment(input_path: str, config_path: str) -> None:
    """Nur Segmentierung anzeigen (ohne E-Mails zu generieren)."""
    config = load_yaml(config_path)
    setup_logging(config.get("log_level", "INFO"), config.get("output_directory", "./data/output"))

    leads_df = csv_reader.read_and_validate(input_path)
    if config.get("duplicate_check", True):
        leads_df = csv_reader.deduplicate(leads_df)

    rules = load_yaml(config.get("segments_config", "./segments/rules.yaml"))
    assignments = segmenter.assign_all(leads_df, rules)

    click.echo(f"\n=== Segmentierungsergebnis ===")
    click.echo(f"Leads geladen: {len(leads_df)}")
    click.echo(f"Zuordnungen: {len(assignments)}")
    click.echo("")

    # Pro Firma und Segment aufschlüsseln
    stats: dict[str, dict[str, int]] = {}
    for a in assignments:
        if a.company_id not in stats:
            stats[a.company_id] = {}
        stats[a.company_id][a.segment_id] = (
            stats[a.company_id].get(a.segment_id, 0) + 1
        )

    for company_id, segments in sorted(stats.items()):
        total = sum(segments.values())
        click.echo(f"{company_id} ({total} Leads):")
        for segment_id, count in sorted(segments.items()):
            click.echo(f"  → {segment_id}: {count}")
        click.echo("")


@cli.command()
@click.option(
    "--input", "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Pfad zur Apollo.io CSV-Datei.",
)
@click.option(
    "--count",
    default=5,
    type=int,
    help="Anzahl der Vorschau-Leads.",
)
@click.option(
    "--config-path",
    default="config.yaml",
    type=click.Path(exists=True),
    help="Pfad zur Konfigurationsdatei.",
)
def preview(input_path: str, count: int, config_path: str) -> None:
    """Vorschau: Zeigt generierte E-Mails für die ersten N Leads."""
    config = load_yaml(config_path)
    setup_logging("WARNING", config.get("output_directory", "./data/output"))

    leads_df = csv_reader.read_and_validate(input_path)
    rules = load_yaml(config.get("segments_config", "./segments/rules.yaml"))
    assignments = segmenter.assign_all(leads_df, rules)

    pdf_links = load_yaml(config.get("promo_materials_config", "./promo_materials/links.yaml"))
    env = template_engine.create_environment(
        config.get("templates_directory", "./templates")
    )
    sender_name = config.get("default_sender_name", "Axel Seehafer")

    # Nur die ersten N anzeigen
    preview_assignments = assignments[:count]
    icebreakers = ai_personalizer.fallback_batch(preview_assignments)

    for i, (assignment, icebreaker) in enumerate(zip(preview_assignments, icebreakers), 1):
        lead_dict = assignment.lead.to_dict()
        link = pdf_linker.resolve(
            assignment.company_id, assignment.segment_id, pdf_links
        )

        rendered = template_engine.render(
            company_id=assignment.company_id,
            segment_id=assignment.segment_id,
            lead=lead_dict,
            icebreaker=icebreaker,
            pdf_link=link,
            sender_name=sender_name,
            env=env,
        )

        click.echo(f"\n{'='*60}")
        click.echo(f"Vorschau {i}/{len(preview_assignments)}")
        click.echo(f"Lead: {lead_dict.get('first_name', '')} {lead_dict.get('last_name', '')} "
                    f"({lead_dict.get('email', '')})")
        click.echo(f"Firma: {assignment.company_id} → {assignment.segment_id}")
        click.echo(f"Score: {assignment.match_score:.1f}")
        click.echo(f"{'='*60}")
        click.echo(f"Betreff: {rendered.subject_line}")
        click.echo(f"---")
        click.echo(rendered.body)
        click.echo("")


@cli.command()
@click.option(
    "--output",
    default="./data/output",
    type=click.Path(),
    help="Ausgabeverzeichnis.",
)
def stats(output: str) -> None:
    """Zeigt Statistiken zu exportierten CSV-Dateien."""
    output_dir = Path(output)

    if not output_dir.exists():
        click.echo(f"Verzeichnis nicht gefunden: {output_dir}")
        return

    csv_files = sorted(output_dir.glob("*.csv"))
    if not csv_files:
        click.echo("Keine CSV-Dateien im Ausgabeverzeichnis gefunden.")
        return

    click.echo(f"\n=== Export-Statistiken ===")
    click.echo(f"Verzeichnis: {output_dir}")
    click.echo("")

    total_leads = 0
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        count = len(df)
        total_leads += count
        click.echo(f"  {csv_file.name}: {count} Leads")

    click.echo(f"\nGesamt: {total_leads} Leads in {len(csv_files)} Dateien")


if __name__ == "__main__":
    cli()
