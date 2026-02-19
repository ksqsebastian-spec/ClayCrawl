// API-Route: KI-Icebreaker generieren
import { NextRequest, NextResponse } from "next/server";
import { generateIcebreaker } from "@/lib/ai-personalizer";
import { fallbackIcebreaker } from "@/lib/fallback-icebreaker";
import type { Assignment } from "@/lib/types";

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json();
    const assignment = body.assignment as Assignment;

    if (!assignment?.lead?.email) {
      return NextResponse.json(
        { error: "Ungültige Anfrage: 'assignment' fehlt" },
        { status: 400 },
      );
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) {
      // Fallback wenn kein API-Key konfiguriert
      const icebreaker = fallbackIcebreaker(assignment);
      return NextResponse.json({ icebreaker, source: "fallback" });
    }

    const icebreaker = await generateIcebreaker(assignment, apiKey);
    return NextResponse.json({ icebreaker, source: "ai" });
  } catch (error) {
    console.error("Fehler bei Icebreaker-Generierung:", error);
    return NextResponse.json(
      { error: "Interner Serverfehler" },
      { status: 500 },
    );
  }
}
