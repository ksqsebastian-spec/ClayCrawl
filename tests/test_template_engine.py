"""Tests für generator/template_engine.py."""

from pathlib import Path

import pytest

from generator.template_engine import (
    RenderedEmail,
    create_environment,
    render,
    _split_subject_and_body,
)


PROJECT_ROOT = Path(__file__).parent.parent


class TestCreateEnvironment:
    """Tests für die Jinja2-Umgebung."""

    def test_creates_environment(self) -> None:
        """Erstellt erfolgreich eine Jinja2-Umgebung."""
        env = create_environment(PROJECT_ROOT / "templates")
        assert env is not None

    def test_raises_on_missing_directory(self) -> None:
        """Wirft FileNotFoundError bei fehlendem Verzeichnis."""
        with pytest.raises(FileNotFoundError):
            create_environment("/nicht/existent")


class TestRender:
    """Tests für das Template-Rendering."""

    def test_renders_seehafer_hausverwaltung(self) -> None:
        """Rendert Seehafer Hausverwaltung Template korrekt."""
        env = create_environment(PROJECT_ROOT / "templates")
        lead = {
            "first_name": "Max",
            "last_name": "Müller",
            "company_name": "ABC Hausverwaltung GmbH",
        }

        result = render(
            company_id="seehafer_elemente",
            segment_id="hausverwaltung",
            lead=lead,
            icebreaker="als erfahrener Facility Manager wissen Sie, wie wichtig schnelle Reaktionszeiten sind.",
            pdf_link="https://link.gruppenwerk.de/seehafer-hausverwaltung",
            sender_name="Axel Seehafer",
            env=env,
        )

        assert isinstance(result, RenderedEmail)
        assert "ABC Hausverwaltung GmbH" in result.subject_line
        assert "Max" in result.body
        assert "Seehafer Elemente" in result.body
        assert "https://link.gruppenwerk.de/seehafer-hausverwaltung" in result.body
        assert result.icebreaker != ""

    def test_renders_all_templates(self) -> None:
        """Alle 15 Templates können gerendert werden."""
        env = create_environment(PROJECT_ROOT / "templates")
        lead = {
            "first_name": "Test",
            "last_name": "Person",
            "company_name": "Test GmbH",
        }

        templates = [
            ("seehafer_elemente", "hausverwaltung"),
            ("seehafer_elemente", "gewerbe"),
            ("seehafer_elemente", "oeffentlich"),
            ("brink_tischlerei", "hausverwaltung"),
            ("brink_tischlerei", "bauunternehmen"),
            ("brink_tischlerei", "privat"),
            ("maler_hantke", "hausverwaltung"),
            ("maler_hantke", "gewerbe"),
            ("maler_hantke", "denkmalschutz"),
            ("maler_hantke", "privat"),
            ("werner_geruestbau", "bauunternehmen"),
            ("werner_geruestbau", "hausverwaltung"),
            ("werner_geruestbau", "oeffentlich"),
            ("werner_bau", "hausverwaltung"),
            ("werner_bau", "oeffentlich"),
            ("werner_bau", "denkmalschutz"),
        ]

        for company_id, segment_id in templates:
            result = render(
                company_id=company_id,
                segment_id=segment_id,
                lead=lead,
                icebreaker="Test-Icebreaker.",
                pdf_link="https://example.com",
                sender_name="Test Sender",
                env=env,
            )
            assert result.subject_line, f"Keine Betreffzeile: {company_id}/{segment_id}"
            assert len(result.body) > 100, f"Body zu kurz: {company_id}/{segment_id}"

    def test_raises_on_missing_template(self) -> None:
        """Wirft Fehler bei fehlendem Template."""
        env = create_environment(PROJECT_ROOT / "templates")
        from jinja2 import TemplateNotFound

        with pytest.raises(TemplateNotFound):
            render(
                company_id="gibts_nicht",
                segment_id="auch_nicht",
                lead={"first_name": "Test"},
                icebreaker="Test",
                pdf_link="",
                sender_name="Test",
                env=env,
            )


class TestSplitSubjectAndBody:
    """Tests für die Betreff/Body-Trennung."""

    def test_splits_correctly(self) -> None:
        """Trennt Betreff und Body korrekt."""
        text = "Betreff: Test-Betreff\n\nHallo Max,\n\nDas ist der Body."
        subject, body = _split_subject_and_body(text)
        assert subject == "Test-Betreff"
        assert body == "Hallo Max,\n\nDas ist der Body."

    def test_handles_missing_subject(self) -> None:
        """Handhabt fehlende Betreffzeile."""
        text = "Hallo Max,\n\nDas ist der Body."
        subject, body = _split_subject_and_body(text)
        assert subject == ""
