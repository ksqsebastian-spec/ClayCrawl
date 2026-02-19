// Fallback-Icebreaker — kann sowohl client- als auch serverseitig verwendet werden
import type { Assignment } from "./types";

export function fallbackIcebreaker(assignment: Assignment): string {
  const { lead } = assignment;
  const industry = lead.industry || "Ihrer Branche";
  const city = lead.city ? ` in ${lead.city}` : "";

  return `Unternehmen${city} im Bereich ${industry} stehen vor der Herausforderung, zuverlässige Handwerkspartner zu finden — besonders wenn Qualität und Termintreue entscheidend sind.`;
}
