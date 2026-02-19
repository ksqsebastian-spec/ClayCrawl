"use client";

import { useState, useCallback, type ChangeEvent } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { parseApolloCSV } from "@/lib/csv-processor";
import { assignAll } from "@/lib/segmenter";
import { renderEmail } from "@/lib/template-engine";
import { fallbackIcebreaker } from "@/lib/fallback-icebreaker";
import { saveCampaign, saveLeads, saveEmails } from "@/lib/store";
import { SEGMENTATION_RULES } from "@/lib/segmentation-rules";
import type { Lead, GeneratedEmail, Campaign } from "@/lib/types";
import { Upload, FileText, Zap, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

type Step = "upload" | "preview" | "configure" | "processing" | "done";

export default function UploadPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("upload");
  const [fileName, setFileName] = useState<string>("");
  const [leads, setLeads] = useState<Lead[]>([]);
  const [skippedMessages, setSkippedMessages] = useState<string[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<string>("");
  const [useAI, setUseAI] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);
  const [campaignId, setCampaignId] = useState<string>("");

  const handleFileUpload = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => {
      const csvText = event.target?.result as string;
      const { leads: parsedLeads, skipped } = parseApolloCSV(csvText);
      setLeads(parsedLeads);
      setSkippedMessages(skipped);
      setStep("preview");
    };
    reader.readAsText(file);
  }, []);

  const handleGenerate = useCallback(async () => {
    setStep("processing");
    setProgress(0);

    const id = crypto.randomUUID();
    setCampaignId(id);

    // Leads mit campaign_id versehen
    const campaignLeads = leads.map((l) => ({ ...l, campaign_id: id }));
    saveLeads(campaignLeads);

    // Segmentierung durchführen
    const companyFilter = selectedCompany || undefined;
    const assignments = assignAll(campaignLeads, companyFilter);

    // E-Mails generieren
    const emails: GeneratedEmail[] = [];
    const companies = new Set<string>();

    for (let i = 0; i < assignments.length; i++) {
      const assignment = assignments[i];
      companies.add(assignment.company_id);

      // Icebreaker: KI oder Fallback
      let icebreaker: string;
      if (useAI) {
        try {
          const res = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ assignment }),
          });
          const data = await res.json();
          icebreaker = data.icebreaker || fallbackIcebreaker(assignment);
        } catch {
          icebreaker = fallbackIcebreaker(assignment);
        }
      } else {
        icebreaker = fallbackIcebreaker(assignment);
      }

      const rendered = renderEmail(assignment, icebreaker);
      emails.push({
        campaign_id: id,
        lead: assignment.lead,
        company_id: assignment.company_id,
        segment_id: assignment.segment_id,
        match_score: assignment.match_score,
        ...rendered,
      });

      setProgress(Math.round(((i + 1) / assignments.length) * 100));
    }

    saveEmails(emails);

    // Kampagne speichern
    const campaign: Campaign = {
      id,
      name: fileName.replace(/\.csv$/i, ""),
      status: "completed",
      created_at: new Date().toISOString(),
      total_leads: leads.length + skippedMessages.length,
      valid_leads: leads.length,
      total_emails: emails.length,
      skipped_leads: skippedMessages.length,
      companies: [...companies],
    };
    saveCampaign(campaign);

    setStep("done");
  }, [leads, selectedCompany, useAI, fileName, skippedMessages.length]);

  const companies = Object.entries(SEGMENTATION_RULES.segmentierung);

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">CSV hochladen</h1>
        <p className="text-muted-foreground">
          Apollo.io CSV-Datei importieren und E-Mails generieren
        </p>
      </div>

      {/* Schritt-Anzeige */}
      <div className="flex items-center gap-2">
        {(
          [
            { key: "upload", label: "Hochladen" },
            { key: "preview", label: "Vorschau" },
            { key: "configure", label: "Konfigurieren" },
            { key: "processing", label: "Generierung" },
            { key: "done", label: "Fertig" },
          ] as const
        ).map((s, i) => {
          const stepOrder = ["upload", "preview", "configure", "processing", "done"] as const;
          const currentIndex = stepOrder.indexOf(step);
          const thisIndex = stepOrder.indexOf(s.key);
          return (
            <div key={s.key} className="flex items-center gap-2">
              {i > 0 && <div className="h-px w-8 bg-border" />}
              <Badge
                variant={
                  step === s.key
                    ? "default"
                    : currentIndex > thisIndex
                      ? "success"
                      : "secondary"
                }
              >
                {s.label}
              </Badge>
            </div>
          );
        })}
      </div>

      {/* Schritt 1: Datei hochladen */}
      {step === "upload" && (
        <Card>
          <CardContent className="p-8">
            <label className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-border p-12 transition-colors hover:border-primary hover:bg-accent/50">
              <Upload className="mb-4 h-10 w-10 text-muted-foreground" />
              <span className="mb-2 text-lg font-medium">
                CSV-Datei auswählen
              </span>
              <span className="text-sm text-muted-foreground">
                Apollo.io Export (.csv)
              </span>
              <input
                type="file"
                accept=".csv"
                className="hidden"
                onChange={handleFileUpload}
              />
            </label>
          </CardContent>
        </Card>
      )}

      {/* Schritt 2: Vorschau */}
      {step === "preview" && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                {fileName}
              </CardTitle>
              <CardDescription>
                {leads.length} gültige Leads gefunden
                {skippedMessages.length > 0 &&
                  ` · ${skippedMessages.length} übersprungen`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="max-h-80 overflow-auto rounded border">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-muted">
                    <tr>
                      <th className="px-3 py-2 text-left font-medium">Name</th>
                      <th className="px-3 py-2 text-left font-medium">E-Mail</th>
                      <th className="px-3 py-2 text-left font-medium">Position</th>
                      <th className="px-3 py-2 text-left font-medium">Firma</th>
                      <th className="px-3 py-2 text-left font-medium">Branche</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leads.slice(0, 50).map((lead, i) => (
                      <tr key={i} className="border-t">
                        <td className="px-3 py-2">
                          {lead.first_name} {lead.last_name}
                        </td>
                        <td className="px-3 py-2 font-mono text-xs">
                          {lead.email}
                        </td>
                        <td className="px-3 py-2">{lead.title}</td>
                        <td className="px-3 py-2">{lead.company_name}</td>
                        <td className="px-3 py-2">{lead.industry}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {leads.length > 50 && (
                  <p className="p-3 text-center text-sm text-muted-foreground">
                    … und {leads.length - 50} weitere Leads
                  </p>
                )}
              </div>

              {skippedMessages.length > 0 && (
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm text-muted-foreground">
                    {skippedMessages.length} übersprungene Einträge anzeigen
                  </summary>
                  <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                    {skippedMessages.map((msg, i) => (
                      <li key={i} className="flex items-start gap-1">
                        <AlertCircle className="mt-0.5 h-3 w-3 shrink-0 text-destructive" />
                        {msg}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-end">
            <Button onClick={() => setStep("configure")}>
              Weiter zur Konfiguration
            </Button>
          </div>
        </div>
      )}

      {/* Schritt 3: Konfiguration */}
      {step === "configure" && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Konfiguration</CardTitle>
              <CardDescription>
                Wählen Sie Firma und Optionen für die E-Mail-Generierung
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="mb-2 block text-sm font-medium">
                  Firma (optional — leer = alle Firmen)
                </label>
                <select
                  value={selectedCompany}
                  onChange={(e) => setSelectedCompany(e.target.value)}
                  className="w-full rounded-md border bg-background px-3 py-2 text-sm"
                >
                  <option value="">Alle Firmen</option>
                  {companies.map(([id, rules]) => (
                    <option key={id} value={id}>
                      {rules.display_name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="use-ai"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  className="h-4 w-4 rounded border"
                />
                <label htmlFor="use-ai" className="text-sm">
                  KI-Icebreaker aktivieren (benötigt ANTHROPIC_API_KEY auf dem
                  Server)
                </label>
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-between">
            <Button variant="outline" onClick={() => setStep("preview")}>
              Zurück
            </Button>
            <Button onClick={handleGenerate}>
              <Zap className="h-4 w-4" />
              E-Mails generieren ({leads.length} Leads)
            </Button>
          </div>
        </div>
      )}

      {/* Schritt 4: Generierung */}
      {step === "processing" && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <Loader2 className="mb-4 h-10 w-10 animate-spin text-primary" />
            <h3 className="mb-2 text-lg font-medium">E-Mails werden generiert…</h3>
            <div className="mb-2 h-2 w-64 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full bg-primary transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-sm text-muted-foreground">{progress}%</p>
          </CardContent>
        </Card>
      )}

      {/* Schritt 5: Fertig */}
      {step === "done" && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <CheckCircle className="mb-4 h-10 w-10 text-success" />
            <h3 className="mb-2 text-lg font-medium">Kampagne erstellt!</h3>
            <p className="mb-6 text-sm text-muted-foreground">
              Alle E-Mails wurden erfolgreich generiert.
            </p>
            <Button onClick={() => router.push(`/campaigns/${campaignId}`)}>
              Kampagne öffnen
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
