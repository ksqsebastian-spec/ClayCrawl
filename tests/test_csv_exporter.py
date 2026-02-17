"""Tests für generator/csv_exporter.py."""

from pathlib import Path

import pandas as pd
import pytest

from generator.csv_exporter import (
    INSTANTLY_COLUMNS,
    build_output_row,
    export,
    split_by_campaign,
    validate_output,
)


class TestBuildOutputRow:
    """Tests für den Aufbau einer Ausgabezeile."""

    def test_builds_complete_row(self) -> None:
        """Baut eine vollständige Ausgabezeile."""
        lead = {
            "email": "max@test.de",
            "first_name": "Max",
            "last_name": "Müller",
            "company_name": "Test GmbH",
            "industry": "Real Estate",
            "city": "Hamburg",
        }

        row = build_output_row(
            lead=lead,
            rendered_body="Hallo Max, das ist der E-Mail-Body...",
            subject_line="Betreff hier",
            icebreaker="Icebreaker-Text",
            pdf_link="https://example.com",
            company_id="seehafer_elemente",
            segment_id="hausverwaltung",
        )

        assert row["email"] == "max@test.de"
        assert row["first_name"] == "Max"
        assert row["campaign_id"] == "gruppenwerk_seehafer_elemente"
        assert row["segment"] == "hausverwaltung"
        assert row["personalization"] == "Hallo Max, das ist der E-Mail-Body..."
        assert row["custom_variable_1"] == "Real Estate"
        assert row["custom_variable_2"] == "Hamburg"


class TestSplitByCampaign:
    """Tests für das Aufteilen nach Kampagne."""

    def test_splits_into_separate_campaigns(self) -> None:
        """Teilt DataFrame korrekt nach campaign_id."""
        df = pd.DataFrame([
            {"campaign_id": "gruppenwerk_seehafer", "email": "a@test.de"},
            {"campaign_id": "gruppenwerk_brink", "email": "b@test.de"},
            {"campaign_id": "gruppenwerk_seehafer", "email": "c@test.de"},
        ])

        campaigns = split_by_campaign(df)
        assert len(campaigns) == 2
        assert len(campaigns["gruppenwerk_seehafer"]) == 2
        assert len(campaigns["gruppenwerk_brink"]) == 1


class TestValidateOutput:
    """Tests für die Ausgabevalidierung."""

    def test_removes_short_personalization(self) -> None:
        """Entfernt E-Mails mit zu kurzem Body."""
        df = pd.DataFrame([
            {
                "email": "a@test.de",
                "personalization": "A" * 150,
                "subject_line": "Test",
                "campaign_id": "test",
            },
            {
                "email": "b@test.de",
                "personalization": "Kurz",
                "subject_line": "Test",
                "campaign_id": "test",
            },
        ])

        result = validate_output(df)
        assert len(result) == 1
        assert result.iloc[0]["email"] == "a@test.de"

    def test_removes_duplicates_per_campaign(self) -> None:
        """Entfernt Duplikate innerhalb einer Kampagne."""
        df = pd.DataFrame([
            {
                "email": "a@test.de",
                "personalization": "A" * 150,
                "subject_line": "Test",
                "campaign_id": "campaign_1",
            },
            {
                "email": "a@test.de",
                "personalization": "B" * 150,
                "subject_line": "Test 2",
                "campaign_id": "campaign_1",
            },
            {
                "email": "a@test.de",
                "personalization": "C" * 150,
                "subject_line": "Test 3",
                "campaign_id": "campaign_2",
            },
        ])

        result = validate_output(df)
        # Gleiche E-Mail in gleicher Kampagne = Duplikat
        # Gleiche E-Mail in anderer Kampagne = OK
        assert len(result) == 2


class TestExport:
    """Tests für den CSV-Export."""

    def test_exports_csv_files(self, tmp_path: Path) -> None:
        """Exportiert CSV-Dateien korrekt."""
        df = pd.DataFrame([
            {
                "email": "max@test.de",
                "first_name": "Max",
                "last_name": "Müller",
                "company_name": "Test GmbH",
                "personalization": "A" * 150,
                "icebreaker": "Icebreaker",
                "subject_line": "Betreff",
                "pdf_link": "https://example.com",
                "campaign_id": "gruppenwerk_seehafer",
                "segment": "hausverwaltung",
                "custom_variable_1": "Real Estate",
                "custom_variable_2": "Hamburg",
            },
        ])

        files = export(df, tmp_path)
        assert len(files) == 1
        assert files[0].exists()

        # CSV prüfen
        exported_df = pd.read_csv(files[0])
        assert len(exported_df) == 1
        assert exported_df.iloc[0]["email"] == "max@test.de"
        assert list(exported_df.columns) == INSTANTLY_COLUMNS

    def test_empty_dataframe_no_files(self, tmp_path: Path) -> None:
        """Leerer DataFrame erzeugt keine Dateien."""
        df = pd.DataFrame()
        files = export(df, tmp_path)
        assert len(files) == 0
