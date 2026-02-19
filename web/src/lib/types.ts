// Gemeinsame Typen für die gesamte Anwendung

export interface Lead {
  id?: string;
  campaign_id?: string;
  first_name: string;
  last_name: string;
  email: string;
  title: string;
  company_name: string;
  industry: string;
  company_size: string;
  city: string;
  state: string;
  country: string;
  company_website: string;
  keywords: string;
  seniority: string;
  departments: string;
}

export interface Assignment {
  lead: Lead;
  company_id: string;
  segment_id: string;
  match_score: number;
}

export interface RenderedEmail {
  subject_line: string;
  body: string;
  icebreaker: string;
  pdf_link: string;
}

export interface GeneratedEmail {
  id?: string;
  campaign_id?: string;
  lead: Lead;
  company_id: string;
  segment_id: string;
  match_score: number;
  subject_line: string;
  body: string;
  icebreaker: string;
  pdf_link: string;
}

export interface Campaign {
  id: string;
  name: string;
  status: "uploading" | "segmenting" | "generating" | "completed" | "error";
  created_at: string;
  total_leads: number;
  valid_leads: number;
  total_emails: number;
  skipped_leads: number;
  companies: string[];
}

export interface CampaignStats {
  by_company: Record<string, number>;
  by_segment: Record<string, number>;
}

// Segmentierungsregeln (TypeScript-Port der YAML-Struktur)
export interface CompanyRule {
  display_name: string;
  branchen: string[];
  jobtitel_keywords: string[];
  unternehmensgroesse_min: number;
  kernleistung: string;
  templates: string[];
  default_template: string;
}

export interface TemplateConditions {
  keywords_enthalten?: string[];
  branchen_enthalten?: string[];
  titel_enthalten?: string[];
  unternehmensgroesse_min?: number;
  unternehmensgroesse_max?: number;
  kein_firmenname?: boolean;
}

export interface TemplateRule {
  beschreibung: string;
  bedingungen: TemplateConditions;
}

export interface SegmentationRules {
  segmentierung: Record<string, CompanyRule>;
  template_auswahl: Record<string, TemplateRule>;
}

// Instantly.ai CSV-Zeile
export interface InstantlyRow {
  email: string;
  first_name: string;
  last_name: string;
  company_name: string;
  personalization: string;
  icebreaker: string;
  subject_line: string;
  pdf_link: string;
  campaign_id: string;
  segment: string;
  custom_variable_1: string;
  custom_variable_2: string;
}
