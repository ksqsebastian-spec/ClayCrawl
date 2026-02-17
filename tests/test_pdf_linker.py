"""Tests für generator/pdf_linker.py."""

import pytest

from generator.pdf_linker import resolve


class TestResolve:
    """Tests für die PDF-Link-Auflösung."""

    def test_resolves_segment_specific_link(self, pdf_links: dict) -> None:
        """Findet segment-spezifischen Link."""
        link = resolve("seehafer_elemente", "hausverwaltung", pdf_links)
        assert link == "https://link.gruppenwerk.de/seehafer-hausverwaltung"

    def test_falls_back_to_default(self, pdf_links: dict) -> None:
        """Nutzt Default-Link wenn Segment nicht konfiguriert."""
        link = resolve("seehafer_elemente", "gibts_nicht", pdf_links)
        assert link == "https://link.gruppenwerk.de/seehafer-leistungen"

    def test_returns_empty_for_unknown_company(self, pdf_links: dict) -> None:
        """Gibt leeren String für unbekannte Firma."""
        link = resolve("gibts_nicht", "hausverwaltung", pdf_links)
        assert link == ""

    def test_resolves_all_configured_links(self, pdf_links: dict) -> None:
        """Alle konfigurierten Links sind auflösbar."""
        for company_id, segments in pdf_links.items():
            for segment_id, expected_link in segments.items():
                link = resolve(company_id, segment_id, pdf_links)
                assert link == expected_link, (
                    f"Falscher Link für {company_id}/{segment_id}: "
                    f"erwartet '{expected_link}', bekommen '{link}'"
                )
