"""Tests für generator/segmenter.py."""

import pandas as pd
import pytest

from generator.segmenter import (
    Assignment,
    assign_all,
    determine_segment,
    match_company,
    _parse_company_size,
)


class TestMatchCompany:
    """Tests für die Firmenzuordnung."""

    def test_matches_by_industry(self, segmentation_rules: dict) -> None:
        """Lead mit passender Branche wird zugeordnet."""
        lead = pd.Series({
            "industry": "Real Estate",
            "title": "Manager",
            "company_size": "51-200",
        })
        rules = segmentation_rules["segmentierung"]["seehafer_elemente"]
        matched, score = match_company(lead, rules)
        assert matched is True
        assert score >= 0.5

    def test_matches_by_title_keyword(self, segmentation_rules: dict) -> None:
        """Lead mit passendem Jobtitel-Keyword wird zugeordnet."""
        lead = pd.Series({
            "industry": "Real Estate",
            "title": "Facility Manager",
            "company_size": "100",
        })
        rules = segmentation_rules["segmentierung"]["seehafer_elemente"]
        matched, score = match_company(lead, rules)
        assert matched is True
        assert score >= 0.8  # Branche + Titel + Größe

    def test_no_match_wrong_industry(self, segmentation_rules: dict) -> None:
        """Lead mit falscher Branche wird nicht zugeordnet."""
        lead = pd.Series({
            "industry": "Food & Beverage",
            "title": "Koch",
            "company_size": "5",
        })
        rules = segmentation_rules["segmentierung"]["seehafer_elemente"]
        matched, score = match_company(lead, rules)
        assert matched is False


class TestDetermineSegment:
    """Tests für die Sekundärsegmentierung."""

    def test_hausverwaltung_for_real_estate(self, segmentation_rules: dict) -> None:
        """Real Estate Lead bekommt hausverwaltung Template."""
        lead = pd.Series({
            "industry": "Real Estate",
            "title": "Facility Manager",
            "company_size": "51-200",
            "keywords": "",
            "company_name": "Test GmbH",
        })
        company_rules = segmentation_rules["segmentierung"]["seehafer_elemente"]
        template_rules = segmentation_rules["template_auswahl"]

        segment = determine_segment(lead, "seehafer_elemente", company_rules, template_rules)
        assert segment == "hausverwaltung"

    def test_denkmalschutz_for_heritage_keywords(self, segmentation_rules: dict) -> None:
        """Lead mit Denkmalschutz-Keywords bekommt denkmalschutz Template."""
        lead = pd.Series({
            "industry": "Government",
            "title": "Leiterin Gebäudemanagement",
            "company_size": "201-500",
            "keywords": "Denkmalschutz Schulen",
            "company_name": "Schulamt Hamburg",
        })
        company_rules = segmentation_rules["segmentierung"]["maler_hantke"]
        template_rules = segmentation_rules["template_auswahl"]

        segment = determine_segment(lead, "maler_hantke", company_rules, template_rules)
        assert segment == "denkmalschutz"

    def test_bauunternehmen_for_construction_with_bau_title(self, segmentation_rules: dict) -> None:
        """Construction Lead mit Bau-Titel bekommt bauunternehmen Template."""
        lead = pd.Series({
            "industry": "Construction",
            "title": "Bauleiter",
            "company_size": "51-200",
            "keywords": "",
            "company_name": "Bau GmbH",
        })
        company_rules = segmentation_rules["segmentierung"]["werner_geruestbau"]
        template_rules = segmentation_rules["template_auswahl"]

        segment = determine_segment(lead, "werner_geruestbau", company_rules, template_rules)
        assert segment == "bauunternehmen"

    def test_falls_back_to_default(self, segmentation_rules: dict) -> None:
        """Unklarer Lead bekommt Default-Template."""
        lead = pd.Series({
            "industry": "Other",
            "title": "CEO",
            "company_size": "51-200",
            "keywords": "",
            "company_name": "Irgendwas GmbH",
        })
        company_rules = segmentation_rules["segmentierung"]["seehafer_elemente"]
        template_rules = segmentation_rules["template_auswahl"]

        segment = determine_segment(lead, "seehafer_elemente", company_rules, template_rules)
        assert segment == company_rules["default_template"]


class TestAssignAll:
    """Tests für die Gesamtzuordnung."""

    def test_assigns_leads_to_multiple_companies(self, segmentation_rules: dict) -> None:
        """Ein Lead kann mehreren Firmen zugeordnet werden."""
        df = pd.DataFrame([{
            "first_name": "Max",
            "last_name": "Müller",
            "email": "max@test.de",
            "title": "Facility Manager",
            "company_name": "ABC Hausverwaltung",
            "industry": "Real Estate",
            "company_size": "51-200",
            "keywords": "",
        }])

        assignments = assign_all(df, segmentation_rules)
        companies = {a.company_id for a in assignments}
        # Real Estate + Facility Manager sollte mehrere Firmen matchen
        assert len(companies) >= 2

    def test_company_filter_limits_results(self, segmentation_rules: dict) -> None:
        """Company-Filter begrenzt Zuordnungen auf eine Firma."""
        df = pd.DataFrame([{
            "first_name": "Max",
            "last_name": "Müller",
            "email": "max@test.de",
            "title": "Facility Manager",
            "company_name": "ABC Hausverwaltung",
            "industry": "Real Estate",
            "company_size": "51-200",
            "keywords": "",
        }])

        assignments = assign_all(df, segmentation_rules, company_filter="seehafer_elemente")
        companies = {a.company_id for a in assignments}
        assert companies == {"seehafer_elemente"}

    def test_invalid_company_filter_raises(self, segmentation_rules: dict) -> None:
        """Unbekannter Company-Filter wirft ValueError."""
        df = pd.DataFrame([{
            "first_name": "Max",
            "last_name": "Müller",
            "email": "max@test.de",
            "title": "Manager",
            "company_name": "Test",
            "industry": "Real Estate",
            "company_size": "10",
            "keywords": "",
        }])

        with pytest.raises(ValueError, match="Unbekannte Firma"):
            assign_all(df, segmentation_rules, company_filter="gibts_nicht")


class TestParseCompanySize:
    """Tests für das Parsen der Unternehmensgröße."""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("51-200", 51),
            ("200+", 200),
            ("200", 200),
            ("51 - 200", 51),
            ("1,000-5,000", 1000),
            ("", 0),
            ("n/a", 0),
        ],
    )
    def test_parses_various_formats(self, input_str: str, expected: int) -> None:
        """Parst verschiedene company_size Formate korrekt."""
        assert _parse_company_size(input_str) == expected
