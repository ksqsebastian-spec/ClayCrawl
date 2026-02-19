"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getCampaign, getEmailsByCampaign } from "@/lib/store";
import { exportToInstantlyCSV, exportByCompany } from "@/lib/csv-processor";
import { SEGMENTATION_RULES } from "@/lib/segmentation-rules";
import type { Campaign, GeneratedEmail } from "@/lib/types";
import { Download, Mail, ArrowLeft, Eye, FileDown } from "lucide-react";

export default function CampaignDetailPage() {
  const params = useParams();
  const campaignId = params.id as string;

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [emails, setEmails] = useState<GeneratedEmail[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<GeneratedEmail | null>(null);
  const [filterCompany, setFilterCompany] = useState<string>("");

  useEffect(() => {
    const c = getCampaign(campaignId);
    setCampaign(c);
    const e = getEmailsByCampaign(campaignId);
    setEmails(e);
    if (e.length > 0) setSelectedEmail(e[0]);
  }, [campaignId]);

  if (!campaign) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <h2 className="mb-2 text-lg font-medium">Kampagne nicht gefunden</h2>
        <Link href="/campaigns">
          <Button variant="outline">
            <ArrowLeft className="h-4 w-4" />
            Zurück
          </Button>
        </Link>
      </div>
    );
  }

  const filteredEmails = filterCompany
    ? emails.filter((e) => e.company_id === filterCompany)
    : emails;

  // Statistiken nach Firma
  const companyStats: Record<string, number> = {};
  for (const email of emails) {
    companyStats[email.company_id] = (companyStats[email.company_id] || 0) + 1;
  }

  function downloadCSV(content: string, filename: string): void {
    const blob = new Blob([content], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function handleDownloadAll(): void {
    const csv = exportToInstantlyCSV(emails);
    downloadCSV(csv, `${campaign!.name}_alle.csv`);
  }

  function handleDownloadByCompany(): void {
    const csvMap = exportByCompany(emails);
    for (const [companyId, csv] of Object.entries(csvMap)) {
      downloadCSV(csv, `${campaign!.name}_${companyId}.csv`);
    }
  }

  const companyDisplayName = (id: string): string =>
    SEGMENTATION_RULES.segmentierung[id]?.display_name || id;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link
            href="/campaigns"
            className="mb-2 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="h-3 w-3" />
            Alle Kampagnen
          </Link>
          <h1 className="text-2xl font-bold">{campaign.name}</h1>
          <p className="text-muted-foreground">
            {campaign.valid_leads} Leads · {campaign.total_emails} E-Mails ·{" "}
            {new Date(campaign.created_at).toLocaleDateString("de-DE")}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleDownloadByCompany}>
            <FileDown className="h-4 w-4" />
            Pro Firma
          </Button>
          <Button onClick={handleDownloadAll}>
            <Download className="h-4 w-4" />
            Alle herunterladen
          </Button>
        </div>
      </div>

      {/* Statistik pro Firma */}
      <div className="grid gap-3 md:grid-cols-3 lg:grid-cols-5">
        {Object.entries(companyStats).map(([companyId, count]) => (
          <Card
            key={companyId}
            className={`cursor-pointer transition-shadow hover:shadow-md ${
              filterCompany === companyId ? "ring-2 ring-primary" : ""
            }`}
            onClick={() =>
              setFilterCompany(filterCompany === companyId ? "" : companyId)
            }
          >
            <CardContent className="p-4">
              <p className="text-sm font-medium">{companyDisplayName(companyId)}</p>
              <p className="text-2xl font-bold">{count}</p>
              <p className="text-xs text-muted-foreground">E-Mails</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* E-Mail-Liste und Vorschau */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Liste */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="h-5 w-5" />
              E-Mails
              {filterCompany && (
                <Badge variant="secondary">
                  {companyDisplayName(filterCompany)}
                  <button
                    className="ml-1"
                    onClick={() => setFilterCompany("")}
                  >
                    ×
                  </button>
                </Badge>
              )}
            </CardTitle>
            <CardDescription>
              {filteredEmails.length} E-Mails
              {filterCompany && ` (gefiltert)`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="max-h-[500px] space-y-2 overflow-auto">
              {filteredEmails.map((email, i) => (
                <div
                  key={i}
                  className={`cursor-pointer rounded-md border p-3 transition-colors hover:bg-accent ${
                    selectedEmail === email
                      ? "border-primary bg-accent"
                      : ""
                  }`}
                  onClick={() => setSelectedEmail(email)}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      {email.lead.first_name} {email.lead.last_name}
                    </span>
                    <Badge variant="outline" className="text-xs">
                      {email.segment_id}
                    </Badge>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {email.lead.email}
                  </p>
                  <p className="mt-1 truncate text-xs text-muted-foreground">
                    {email.subject_line}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Vorschau */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              E-Mail-Vorschau
            </CardTitle>
          </CardHeader>
          <CardContent>
            {selectedEmail ? (
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-medium text-muted-foreground">
                    An
                  </p>
                  <p className="text-sm">
                    {selectedEmail.lead.first_name}{" "}
                    {selectedEmail.lead.last_name} &lt;
                    {selectedEmail.lead.email}&gt;
                  </p>
                </div>
                <div>
                  <p className="text-xs font-medium text-muted-foreground">
                    Betreff
                  </p>
                  <p className="text-sm font-medium">
                    {selectedEmail.subject_line}
                  </p>
                </div>
                <div>
                  <p className="text-xs font-medium text-muted-foreground">
                    Firma / Segment
                  </p>
                  <p className="text-sm">
                    {companyDisplayName(selectedEmail.company_id)} /{" "}
                    {selectedEmail.segment_id}
                    <span className="ml-2 text-xs text-muted-foreground">
                      (Score: {(selectedEmail.match_score * 100).toFixed(0)}%)
                    </span>
                  </p>
                </div>
                <hr />
                <div className="whitespace-pre-wrap rounded-md bg-muted p-4 text-sm leading-relaxed">
                  {selectedEmail.body}
                </div>
              </div>
            ) : (
              <p className="py-8 text-center text-sm text-muted-foreground">
                Wählen Sie eine E-Mail aus der Liste
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
