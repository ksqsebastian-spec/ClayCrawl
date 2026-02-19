// KI-Personalisierung: Icebreaker-Generierung mit Claude API (nur serverseitig)
import Anthropic from "@anthropic-ai/sdk";
import type { Assignment } from "./types";
import { SEGMENTATION_RULES } from "./segmentation-rules";
import { fallbackIcebreaker } from "./fallback-icebreaker";

const ICEBREAKER_PROMPT = `Du bist ein deutschsprachiger B2B-Sales-Texter. Erstelle einen kurzen, personalisierten Icebreaker (1-2 Sätze) für eine Cold-E-Mail.

REGELN:
- Deutsch, professionell, nicht aufdringlich
- Bezug auf Branche, Position oder Unternehmen des Empfängers
- Keine Floskeln wie "Ich hoffe, es geht Ihnen gut"
- Kein "Ich habe gesehen, dass..."
- Maximal 2 Sätze
- Nahtloser Übergang zum Rest der E-Mail

LEAD-INFORMATIONEN:
- Name: {{vorname}} {{nachname}}
- Position: {{position}}
- Firma: {{firma}}
- Branche: {{branche}}
- Unternehmensgröße: {{groesse}}
- Stadt: {{stadt}}

ABSENDER-FIRMA: {{absender_firma}}
KERNLEISTUNG: {{kernleistung}}

Antworte NUR mit dem Icebreaker-Text, ohne Anführungszeichen.`;

export async function generateIcebreaker(
  assignment: Assignment,
  apiKey: string,
): Promise<string> {
  const { lead, company_id } = assignment;
  const companyRules = SEGMENTATION_RULES.segmentierung[company_id];

  if (!companyRules) {
    return fallbackIcebreaker(assignment);
  }

  const prompt = ICEBREAKER_PROMPT
    .replace("{{vorname}}", lead.first_name || "")
    .replace("{{nachname}}", lead.last_name || "")
    .replace("{{position}}", lead.title || "")
    .replace("{{firma}}", lead.company_name || "")
    .replace("{{branche}}", lead.industry || "")
    .replace("{{groesse}}", lead.company_size || "")
    .replace("{{stadt}}", lead.city || "")
    .replace("{{absender_firma}}", companyRules.display_name)
    .replace("{{kernleistung}}", companyRules.kernleistung);

  const client = new Anthropic({ apiKey });

  // 3 Versuche mit Backoff
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const response = await client.messages.create({
        model: "claude-sonnet-4-5-20250929",
        max_tokens: 200,
        messages: [{ role: "user", content: prompt }],
      });

      const block = response.content[0];
      if (block.type === "text") {
        return block.text.trim();
      }
      return fallbackIcebreaker(assignment);
    } catch (error) {
      if (attempt < 2) {
        const delay = Math.pow(2, attempt + 1) * 1000;
        await new Promise((resolve) => setTimeout(resolve, delay));
        continue;
      }
      console.error(`Claude API Fehler nach 3 Versuchen: ${error}`);
      return fallbackIcebreaker(assignment);
    }
  }

  return fallbackIcebreaker(assignment);
}
