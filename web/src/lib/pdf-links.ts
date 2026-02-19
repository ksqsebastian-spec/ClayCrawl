// PDF-Link-Konfiguration — TypeScript-Port der YAML-Datei

// Zuordnung: Firma → Segment → PDF-Link
export const PDF_LINKS: Record<string, Record<string, string>> = {
  seehafer_elemente: {
    hausverwaltung:
      "https://gruppenwerk.de/seehafer/hausverwaltung-broschuere.pdf",
    gewerbe: "https://gruppenwerk.de/seehafer/gewerbe-broschuere.pdf",
    oeffentlich:
      "https://gruppenwerk.de/seehafer/oeffentlich-broschuere.pdf",
  },
  brink_tischlerei: {
    hausverwaltung:
      "https://gruppenwerk.de/brink/hausverwaltung-broschuere.pdf",
    bauunternehmen:
      "https://gruppenwerk.de/brink/bauunternehmen-broschuere.pdf",
    privat: "https://gruppenwerk.de/brink/privat-broschuere.pdf",
  },
  maler_hantke: {
    hausverwaltung:
      "https://gruppenwerk.de/hantke/hausverwaltung-broschuere.pdf",
    gewerbe: "https://gruppenwerk.de/hantke/gewerbe-broschuere.pdf",
    denkmalschutz:
      "https://gruppenwerk.de/hantke/denkmalschutz-broschuere.pdf",
    privat: "https://gruppenwerk.de/hantke/privat-broschuere.pdf",
  },
  werner_geruestbau: {
    bauunternehmen:
      "https://gruppenwerk.de/werner-geruest/bauunternehmen-broschuere.pdf",
    hausverwaltung:
      "https://gruppenwerk.de/werner-geruest/hausverwaltung-broschuere.pdf",
    oeffentlich:
      "https://gruppenwerk.de/werner-geruest/oeffentlich-broschuere.pdf",
  },
  werner_bau: {
    hausverwaltung:
      "https://gruppenwerk.de/werner-bau/hausverwaltung-broschuere.pdf",
    oeffentlich:
      "https://gruppenwerk.de/werner-bau/oeffentlich-broschuere.pdf",
    denkmalschutz:
      "https://gruppenwerk.de/werner-bau/denkmalschutz-broschuere.pdf",
  },
};

export function resolvePdfLink(
  companyId: string,
  segmentId: string,
): string {
  const companyLinks = PDF_LINKS[companyId];
  if (!companyLinks) {
    console.warn(`Keine PDF-Links für Firma '${companyId}' konfiguriert`);
    return "";
  }

  const link = companyLinks[segmentId];
  if (!link) {
    console.warn(
      `Kein PDF-Link für Segment '${segmentId}' bei Firma '${companyId}'`,
    );
    return "";
  }

  return link;
}
