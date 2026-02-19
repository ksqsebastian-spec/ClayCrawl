// CSV-Verarbeitung: Import von Apollo CSV und Export für Instantly
import Papa from "papaparse";
import type { Lead, GeneratedEmail, InstantlyRow } from "./types";

// Apollo CSV Spalten-Mapping (Apollo → internes Format)
const APOLLO_FIELD_MAP: Record<string, keyof Lead> = {
  "First Name": "first_name",
  "Last Name": "last_name",
  Email: "email",
  Title: "title",
  "Company Name for Leads": "company_name",
  Company: "company_name",
  "company_name": "company_name",
  Industry: "industry",
  "# Employees": "company_size",
  "Company Size": "company_size",
  City: "city",
  State: "state",
  Country: "country",
  "Company Website": "company_website",
  Website: "company_website",
  Keywords: "keywords",
  Seniority: "seniority",
  Departments: "departments",
};

export function parseApolloCSV(csvText: string): {
  leads: Lead[];
  skipped: string[];
  headers: string[];
} {
  const result = Papa.parse<Record<string, string>>(csvText, {
    header: true,
    skipEmptyLines: true,
    transformHeader: (h: string) => h.trim(),
  });

  const headers = result.meta.fields || [];
  const leads: Lead[] = [];
  const skipped: string[] = [];

  for (const row of result.data) {
    const lead = mapRowToLead(row);

    // Validierung: E-Mail ist Pflicht
    if (!lead.email || !isValidEmail(lead.email)) {
      skipped.push(
        `Zeile übersprungen: ${lead.first_name} ${lead.last_name} — ungültige E-Mail '${lead.email || "(leer)"}'`,
      );
      continue;
    }

    // Mindestens ein Name
    if (!lead.first_name && !lead.last_name) {
      skipped.push(
        `Zeile übersprungen: ${lead.email} — kein Name vorhanden`,
      );
      continue;
    }

    leads.push(lead);
  }

  return { leads, skipped, headers };
}

function mapRowToLead(row: Record<string, string>): Lead {
  const lead: Lead = {
    first_name: "",
    last_name: "",
    email: "",
    title: "",
    company_name: "",
    industry: "",
    company_size: "",
    city: "",
    state: "",
    country: "",
    company_website: "",
    keywords: "",
    seniority: "",
    departments: "",
  };

  for (const [csvField, value] of Object.entries(row)) {
    const mappedField = APOLLO_FIELD_MAP[csvField.trim()];
    if (mappedField && value) {
      lead[mappedField] = value.trim();
    }
  }

  return lead;
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function exportToInstantlyCSV(emails: GeneratedEmail[]): string {
  const rows: InstantlyRow[] = emails.map((email) => ({
    email: email.lead.email,
    first_name: email.lead.first_name,
    last_name: email.lead.last_name,
    company_name: email.lead.company_name,
    personalization: email.body,
    icebreaker: email.icebreaker,
    subject_line: email.subject_line,
    pdf_link: email.pdf_link,
    campaign_id: email.company_id,
    segment: email.segment_id,
    custom_variable_1: email.lead.title,
    custom_variable_2: email.lead.industry,
  }));

  return Papa.unparse(rows);
}

// Export nach Firma gruppiert (eine CSV pro Firma)
export function exportByCompany(
  emails: GeneratedEmail[],
): Record<string, string> {
  const grouped: Record<string, GeneratedEmail[]> = {};

  for (const email of emails) {
    if (!grouped[email.company_id]) {
      grouped[email.company_id] = [];
    }
    grouped[email.company_id].push(email);
  }

  const result: Record<string, string> = {};
  for (const [companyId, companyEmails] of Object.entries(grouped)) {
    result[companyId] = exportToInstantlyCSV(companyEmails);
  }

  return result;
}
