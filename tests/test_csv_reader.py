"""Tests für generator/csv_reader.py."""

from pathlib import Path

import pandas as pd
import pytest

from generator.csv_reader import (
    clean_data,
    deduplicate,
    read_and_validate,
    validate_emails,
)


class TestReadAndValidate:
    """Tests für das Einlesen und Validieren von Apollo CSVs."""

    def test_reads_valid_csv(self, sample_csv_path: Path) -> None:
        """Liest eine gültige CSV erfolgreich ein."""
        df = read_and_validate(sample_csv_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_raises_on_missing_file(self) -> None:
        """Wirft FileNotFoundError bei fehlender Datei."""
        with pytest.raises(FileNotFoundError):
            read_and_validate("/nicht/existent.csv")

    def test_raises_on_missing_columns(self, tmp_path: Path) -> None:
        """Wirft ValueError wenn Pflichtspalten fehlen."""
        csv_path = tmp_path / "incomplete.csv"
        csv_path.write_text("first_name,email\nMax,max@test.de\n")

        with pytest.raises(ValueError, match="Pflichtspalten fehlen"):
            read_and_validate(csv_path)

    def test_adds_optional_columns(self, tmp_path: Path) -> None:
        """Ergänzt fehlende optionale Spalten mit leerem String."""
        csv_path = tmp_path / "minimal.csv"
        csv_path.write_text(
            "first_name,last_name,email,title,company_name,industry\n"
            "Max,Müller,max@test.de,Manager,Test GmbH,Real Estate\n"
        )

        df = read_and_validate(csv_path)
        assert "company_size" in df.columns
        assert "city" in df.columns

    def test_filters_invalid_emails(self, sample_csv_path: Path) -> None:
        """Entfernt Leads mit ungültiger E-Mail."""
        df = read_and_validate(sample_csv_path)
        emails = df["email"].tolist()
        assert "invalid-email" not in emails

    def test_filters_leads_without_email(self, sample_csv_path: Path) -> None:
        """Entfernt Leads ohne E-Mail-Adresse."""
        df = read_and_validate(sample_csv_path)
        assert (df["email"] == "").sum() == 0


class TestCleanData:
    """Tests für die Datenbereinigung."""

    def test_strips_whitespace(self) -> None:
        """Entfernt Whitespace aus allen Feldern."""
        df = pd.DataFrame({
            "first_name": ["  Max  "],
            "email": [" max@test.de "],
            "company_name": ["Test GmbH  "],
        })
        cleaned = clean_data(df)
        assert cleaned.iloc[0]["first_name"] == "Max"
        assert cleaned.iloc[0]["email"] == "max@test.de"

    def test_removes_leads_without_required_fields(self) -> None:
        """Entfernt Leads mit leeren Pflichtfeldern."""
        df = pd.DataFrame({
            "first_name": ["Max", ""],
            "email": ["max@test.de", "anna@test.de"],
            "company_name": ["Test GmbH", "Test2 GmbH"],
        })
        cleaned = clean_data(df)
        assert len(cleaned) == 1


class TestValidateEmails:
    """Tests für die E-Mail-Validierung."""

    def test_keeps_valid_emails(self) -> None:
        """Behält gültige E-Mail-Adressen."""
        df = pd.DataFrame({"email": ["max@test.de", "anna@example.com"]})
        result = validate_emails(df)
        assert len(result) == 2

    def test_removes_invalid_emails(self) -> None:
        """Entfernt ungültige E-Mail-Adressen."""
        df = pd.DataFrame({"email": ["max@test.de", "not-an-email", ""]})
        result = validate_emails(df)
        assert len(result) == 1
        assert result.iloc[0]["email"] == "max@test.de"


class TestDeduplicate:
    """Tests für die Duplikat-Entfernung."""

    def test_removes_duplicate_emails(self) -> None:
        """Entfernt Duplikate basierend auf E-Mail."""
        df = pd.DataFrame({
            "email": ["max@test.de", "anna@test.de", "max@test.de"],
            "first_name": ["Max", "Anna", "Maximilian"],
        })
        result = deduplicate(df)
        assert len(result) == 2
        # Erster Eintrag wird behalten
        assert result.iloc[0]["first_name"] == "Max"

    def test_no_duplicates_unchanged(self) -> None:
        """DataFrame ohne Duplikate bleibt unverändert."""
        df = pd.DataFrame({
            "email": ["max@test.de", "anna@test.de"],
        })
        result = deduplicate(df)
        assert len(result) == 2
