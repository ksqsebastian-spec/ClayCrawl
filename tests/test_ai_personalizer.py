"""Tests für generator/ai_personalizer.py."""

import pandas as pd
import pytest

from generator.ai_personalizer import (
    build_prompt,
    fallback_batch,
    fallback_single,
    FALLBACK_ICEBREAKERS,
)
from generator.segmenter import Assignment


@pytest.fixture
def sample_assignment() -> Assignment:
    """Ein Beispiel-Assignment für Tests."""
    lead = pd.Series({
        "first_name": "Max",
        "last_name": "Müller",
        "email": "max@test.de",
        "title": "Facility Manager",
        "company_name": "ABC Hausverwaltung GmbH",
        "industry": "Real Estate",
        "company_size": "51-200",
        "city": "Hamburg",
    })
    return Assignment(
        lead=lead,
        company_id="seehafer_elemente",
        segment_id="hausverwaltung",
        match_score=0.8,
    )


class TestBuildPrompt:
    """Tests für die Prompt-Erstellung."""

    def test_builds_prompt_with_lead_data(
        self, sample_assignment: Assignment, segmentation_rules: dict
    ) -> None:
        """Prompt enthält Lead-Daten."""
        prompt = build_prompt(sample_assignment, segmentation_rules)
        assert "Max" in prompt
        assert "Müller" in prompt
        assert "Facility Manager" in prompt
        assert "ABC Hausverwaltung GmbH" in prompt
        assert "Real Estate" in prompt

    def test_builds_prompt_with_company_info(
        self, sample_assignment: Assignment, segmentation_rules: dict
    ) -> None:
        """Prompt enthält Firmeninformationen."""
        prompt = build_prompt(sample_assignment, segmentation_rules)
        assert "Seehafer Elemente" in prompt
        assert "Bauelemente" in prompt  # Aus kernleistung

    def test_prompt_contains_rules(
        self, sample_assignment: Assignment, segmentation_rules: dict
    ) -> None:
        """Prompt enthält Generierungsregeln."""
        prompt = build_prompt(sample_assignment, segmentation_rules)
        assert "Deutsch" in prompt
        assert "maximal 2 Sätze" in prompt


class TestFallbackIcebreaker:
    """Tests für die Fallback-Icebreaker."""

    def test_fallback_single_returns_german_text(self, sample_assignment: Assignment) -> None:
        """Fallback-Icebreaker ist auf Deutsch."""
        result = fallback_single(sample_assignment)
        assert isinstance(result, str)
        assert len(result) > 20
        # Enthält Lead-Daten
        assert "Facility Manager" in result or "ABC Hausverwaltung" in result

    def test_fallback_all_segments_exist(self) -> None:
        """Alle erwarteten Segmente haben einen Fallback-Icebreaker."""
        expected_segments = [
            "hausverwaltung",
            "bauunternehmen",
            "oeffentlich",
            "denkmalschutz",
            "gewerbe",
            "privat",
        ]
        for segment in expected_segments:
            assert segment in FALLBACK_ICEBREAKERS, f"Kein Fallback für '{segment}'"

    def test_fallback_batch_returns_correct_count(self) -> None:
        """Fallback-Batch gibt korrekte Anzahl zurück."""
        assignments = []
        for segment in ["hausverwaltung", "bauunternehmen", "oeffentlich"]:
            lead = pd.Series({
                "title": "Manager",
                "company_name": "Test GmbH",
            })
            assignments.append(
                Assignment(lead=lead, company_id="test", segment_id=segment, match_score=0.5)
            )

        results = fallback_batch(assignments)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    def test_unknown_segment_falls_back_to_hausverwaltung(self) -> None:
        """Unbekanntes Segment nutzt hausverwaltung als Fallback."""
        lead = pd.Series({
            "title": "Manager",
            "company_name": "Test GmbH",
        })
        assignment = Assignment(
            lead=lead,
            company_id="test",
            segment_id="gibts_nicht",
            match_score=0.5,
        )

        result = fallback_single(assignment)
        expected_template = FALLBACK_ICEBREAKERS["hausverwaltung"]
        expected = expected_template.format(title="Manager", company_name="Test GmbH")
        assert result == expected
