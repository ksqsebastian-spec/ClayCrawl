// Segmentierung: Zuordnung von Leads zu Firmen und Template-Segmenten
import type {
  Lead,
  Assignment,
  CompanyRule,
  TemplateRule,
  SegmentationRules,
} from "./types";
import { SEGMENTATION_RULES } from "./segmentation-rules";

export function assignAll(
  leads: Lead[],
  companyFilter?: string,
  rules: SegmentationRules = SEGMENTATION_RULES,
): Assignment[] {
  const { segmentierung, template_auswahl } = rules;
  const assignments: Assignment[] = [];

  let companies = Object.keys(segmentierung);
  if (companyFilter) {
    if (!(companyFilter in segmentierung)) {
      throw new Error(
        `Unbekannte Firma: '${companyFilter}'. Verfügbar: ${companies.join(", ")}`,
      );
    }
    companies = [companyFilter];
  }

  for (const lead of leads) {
    for (const companyId of companies) {
      const companyRules = segmentierung[companyId];
      const { matched, score } = matchCompany(lead, companyRules);

      if (matched) {
        const segmentId = determineSegment(
          lead,
          companyId,
          companyRules,
          template_auswahl,
        );
        assignments.push({
          lead,
          company_id: companyId,
          segment_id: segmentId,
          match_score: score,
        });
      }
    }
  }

  return assignments;
}

export function matchCompany(
  lead: Lead,
  companyRules: CompanyRule,
): { matched: boolean; score: number } {
  let score = 0;

  // Branche prüfen
  const leadIndustry = (lead.industry || "").trim();
  if (matchesAny(leadIndustry, companyRules.branchen)) {
    score += 0.5;
  }

  // Jobtitel prüfen
  const leadTitle = (lead.title || "").trim();
  if (titleMatchesKeywords(leadTitle, companyRules.jobtitel_keywords)) {
    score += 0.3;
  }

  // Unternehmensgröße prüfen
  const leadSize = parseCompanySize(lead.company_size || "");
  if (leadSize >= companyRules.unternehmensgroesse_min) {
    score += 0.2;
  }

  return { matched: score >= 0.5, score };
}

export function determineSegment(
  lead: Lead,
  companyId: string,
  companyRules: CompanyRule,
  templateRules: Record<string, TemplateRule>,
): string {
  const availableTemplates = companyRules.templates;
  const defaultTemplate = companyRules.default_template;

  const leadIndustry = (lead.industry || "").trim();
  const leadTitle = (lead.title || "").trim();
  const leadKeywords = (lead.keywords || "").trim();
  const leadCompany = (lead.company_name || "").trim();

  for (const [segmentId, segmentRule] of Object.entries(templateRules)) {
    if (!availableTemplates.includes(segmentId)) continue;

    const conditions = segmentRule.bedingungen;

    // Denkmalschutz: Keywords
    if (conditions.keywords_enthalten?.length) {
      const combinedText = `${leadIndustry} ${leadTitle} ${leadKeywords}`;
      if (textContainsAny(combinedText, conditions.keywords_enthalten)) {
        return segmentId;
      }
    }

    // Branche prüfen
    if (conditions.branchen_enthalten?.length) {
      if (matchesAny(leadIndustry, conditions.branchen_enthalten)) {
        // Zusätzliche Titel-Bedingung für "bauunternehmen"
        if (conditions.titel_enthalten?.length) {
          if (titleMatchesKeywords(leadTitle, conditions.titel_enthalten)) {
            return segmentId;
          }
          continue;
        }
        return segmentId;
      }
    }

    // Unternehmensgröße
    const leadSize = parseCompanySize(lead.company_size || "");
    if (
      conditions.unternehmensgroesse_min !== undefined &&
      leadSize >= conditions.unternehmensgroesse_min
    ) {
      return segmentId;
    }
    if (
      conditions.unternehmensgroesse_max !== undefined &&
      leadSize > 0 &&
      leadSize <= conditions.unternehmensgroesse_max
    ) {
      return segmentId;
    }

    // Kein Firmenname
    if (conditions.kein_firmenname && !leadCompany) {
      return segmentId;
    }
  }

  return defaultTemplate;
}

function matchesAny(value: string, targets: string[]): boolean {
  const lower = value.toLowerCase();
  return targets.some((t) => lower.includes(t.toLowerCase()));
}

function titleMatchesKeywords(title: string, keywords: string[]): boolean {
  const lower = title.toLowerCase();
  return keywords.some((kw) => lower.includes(kw.toLowerCase()));
}

function textContainsAny(text: string, keywords: string[]): boolean {
  const lower = text.toLowerCase();
  return keywords.some((kw) => lower.includes(kw.toLowerCase()));
}

export function parseCompanySize(sizeStr: string): number {
  if (!sizeStr) return 0;
  const match = sizeStr.replace(/,/g, "").match(/\d+/);
  return match ? parseInt(match[0], 10) : 0;
}
