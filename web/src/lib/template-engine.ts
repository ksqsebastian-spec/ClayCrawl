// Template-Engine: Erzeugt E-Mail-Texte aus Zuordnungen
import type { Assignment, RenderedEmail } from "./types";
import { SEGMENTATION_RULES } from "./segmentation-rules";
import { resolvePdfLink } from "./pdf-links";

// E-Mail-Templates — Firma → Segment → Template-Text
// Platzhalter: {{vorname}}, {{nachname}}, {{firma}}, {{position}}, {{kernleistung}}, {{icebreaker}}, {{pdf_link}}
const EMAIL_TEMPLATES: Record<string, Record<string, { subject: string; body: string }>> = {
  seehafer_elemente: {
    hausverwaltung: {
      subject: "Wartung & Reparatur für Ihre Objekte — Seehafer Elemente",
      body: `Guten Tag {{vorname}} {{nachname}},

als {{position}} bei {{firma}} kennen Sie die Herausforderung, Gebäude langfristig instand zu halten.

{{icebreaker}}

Seehafer Elemente ist seit 1948 Spezialist für {{kernleistung}}. Wir unterstützen Hausverwaltungen wie Ihre mit zuverlässiger Wartung und schnellen Reparaturen.

Einen Überblick über unser Leistungsspektrum finden Sie hier:
{{pdf_link}}

Hätten Sie Zeit für ein kurzes Gespräch in den nächsten Tagen?

Beste Grüße
Gruppenwerk | Seehafer Elemente`,
    },
    gewerbe: {
      subject: "Gewerbliche Bauelemente — Seehafer Elemente",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Seehafer Elemente bietet seit über 75 Jahren {{kernleistung}} für gewerbliche Immobilien.

Mehr Informationen:
{{pdf_link}}

Ich freue mich auf Ihre Rückmeldung.

Beste Grüße
Gruppenwerk | Seehafer Elemente`,
    },
    oeffentlich: {
      subject: "Bauelemente für öffentliche Einrichtungen — Seehafer",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Seehafer Elemente unterstützt öffentliche Auftraggeber mit {{kernleistung}}.

Hier finden Sie unser Leistungsangebot:
{{pdf_link}}

Beste Grüße
Gruppenwerk | Seehafer Elemente`,
    },
  },
  brink_tischlerei: {
    hausverwaltung: {
      subject: "Tischlerei-Lösungen für Ihre Objekte — Karl Brink",
      body: `Guten Tag {{vorname}} {{nachname}},

als {{position}} bei {{firma}} wissen Sie, wie wichtig hochwertige Türen und Fenster sind.

{{icebreaker}}

Karl Brink Tischlereibetrieb ist Spezialist für {{kernleistung}}.

Mehr Details:
{{pdf_link}}

Beste Grüße
Gruppenwerk | Karl Brink Tischlerei`,
    },
    bauunternehmen: {
      subject: "Maßgefertigte Bautischlerei — Karl Brink",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Für Ihr Bauvorhaben bieten wir {{kernleistung}}.

Informationen:
{{pdf_link}}

Beste Grüße
Gruppenwerk | Karl Brink Tischlerei`,
    },
    privat: {
      subject: "Einbaumöbel & Maßanfertigungen — Karl Brink",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Wir fertigen individuelle Möbel- und Einbaulösungen. {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Karl Brink Tischlerei`,
    },
  },
  maler_hantke: {
    hausverwaltung: {
      subject: "Malerarbeiten für Ihre Immobilien — Hantke",
      body: `Guten Tag {{vorname}} {{nachname}},

als {{position}} bei {{firma}} kennen Sie den Bedarf an regelmäßigen Malerarbeiten.

{{icebreaker}}

Tomas Hantke Malermeister bietet {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Tomas Hantke Malermeister`,
    },
    gewerbe: {
      subject: "Malerarbeiten für Gewerbeimmobilien — Hantke",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Wir bieten {{kernleistung}} für gewerbliche Objekte.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Tomas Hantke Malermeister`,
    },
    denkmalschutz: {
      subject: "Denkmalgerechte Malerarbeiten — Hantke",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Seit 1990 sind wir spezialisiert auf {{kernleistung}} — insbesondere im Bereich Denkmalschutz.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Tomas Hantke Malermeister`,
    },
    privat: {
      subject: "Ihr Malermeister — Tomas Hantke",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

{{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Tomas Hantke Malermeister`,
    },
  },
  werner_geruestbau: {
    bauunternehmen: {
      subject: "Gerüstbau für Ihr Projekt — J. Werner",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

J. Werner Gerüstbau bietet {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | J. Werner Gerüstbau`,
    },
    hausverwaltung: {
      subject: "Gerüstbau für Sanierungen — J. Werner",
      body: `Guten Tag {{vorname}} {{nachname}},

als {{position}} bei {{firma}} stehen Sanierungsprojekte regelmäßig an.

{{icebreaker}}

J. Werner bietet {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | J. Werner Gerüstbau`,
    },
    oeffentlich: {
      subject: "Gerüstbau für öffentliche Projekte — J. Werner",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

{{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | J. Werner Gerüstbau`,
    },
  },
  werner_bau: {
    hausverwaltung: {
      subject: "Gebäudesanierung — Werner Bauunternehmung",
      body: `Guten Tag {{vorname}} {{nachname}},

als {{position}} bei {{firma}} kennen Sie den Wert professioneller Gebäudesanierung.

{{icebreaker}}

Werner GmbH bietet {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Werner GmbH Bauunternehmung`,
    },
    oeffentlich: {
      subject: "Sanierung öffentlicher Gebäude — Werner",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Mit fast 100 Jahren Erfahrung bieten wir {{kernleistung}}.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Werner GmbH Bauunternehmung`,
    },
    denkmalschutz: {
      subject: "Denkmalgerechte Sanierung — Werner Bau",
      body: `Guten Tag {{vorname}} {{nachname}},

{{icebreaker}}

Werner GmbH ist Spezialist für {{kernleistung}}, besonders im Bereich Denkmalschutz.

{{pdf_link}}

Beste Grüße
Gruppenwerk | Werner GmbH Bauunternehmung`,
    },
  },
};

export function renderEmail(
  assignment: Assignment,
  icebreaker: string,
): RenderedEmail {
  const { lead, company_id, segment_id } = assignment;
  const companyRules = SEGMENTATION_RULES.segmentierung[company_id];
  const pdfLink = resolvePdfLink(company_id, segment_id);

  const companyTemplates = EMAIL_TEMPLATES[company_id];
  if (!companyTemplates) {
    throw new Error(`Keine Templates für Firma '${company_id}' vorhanden`);
  }

  const template = companyTemplates[segment_id];
  if (!template) {
    throw new Error(
      `Kein Template für Segment '${segment_id}' bei Firma '${company_id}'`,
    );
  }

  const replacements: Record<string, string> = {
    "{{vorname}}": lead.first_name || "",
    "{{nachname}}": lead.last_name || "",
    "{{firma}}": lead.company_name || "",
    "{{position}}": lead.title || "",
    "{{kernleistung}}": companyRules?.kernleistung || "",
    "{{icebreaker}}": icebreaker,
    "{{pdf_link}}": pdfLink,
  };

  let body = template.body;
  let subject = template.subject;

  for (const [placeholder, value] of Object.entries(replacements)) {
    body = body.replaceAll(placeholder, value);
    subject = subject.replaceAll(placeholder, value);
  }

  return {
    subject_line: subject,
    body,
    icebreaker,
    pdf_link: pdfLink,
  };
}

export function getAvailableTemplates(): { companyId: string; segmentId: string; subject: string }[] {
  const result: { companyId: string; segmentId: string; subject: string }[] = [];
  for (const [companyId, segments] of Object.entries(EMAIL_TEMPLATES)) {
    for (const [segmentId, template] of Object.entries(segments)) {
      result.push({ companyId, segmentId, subject: template.subject });
    }
  }
  return result;
}

export function getTemplateContent(
  companyId: string,
  segmentId: string,
): { subject: string; body: string } | null {
  return EMAIL_TEMPLATES[companyId]?.[segmentId] ?? null;
}
