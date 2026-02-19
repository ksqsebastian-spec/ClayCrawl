"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getCampaigns, deleteCampaign } from "@/lib/store";
import type { Campaign } from "@/lib/types";
import { Upload, Mail, Users, Trash2, ArrowRight } from "lucide-react";

// Status-Labels auf Deutsch
const STATUS_LABELS: Record<Campaign["status"], string> = {
  uploading: "Hochladen",
  segmenting: "Segmentierung",
  generating: "E-Mails werden generiert",
  completed: "Abgeschlossen",
  error: "Fehler",
};

const STATUS_VARIANTS: Record<Campaign["status"], "default" | "secondary" | "success" | "destructive"> = {
  uploading: "secondary",
  segmenting: "default",
  generating: "default",
  completed: "success",
  error: "destructive",
};

export default function DashboardPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  useEffect(() => {
    setCampaigns(getCampaigns().sort((a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    ));
  }, []);

  function handleDelete(id: string): void {
    if (!confirm("Kampagne wirklich löschen?")) return;
    deleteCampaign(id);
    setCampaigns(getCampaigns());
  }

  return (
    <div className="space-y-8">
      {/* Übersicht */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Übersicht aller Kampagnen
          </p>
        </div>
        <Link href="/upload">
          <Button>
            <Upload className="h-4 w-4" />
            Neue Kampagne
          </Button>
        </Link>
      </div>

      {/* Statistik-Karten */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Kampagnen gesamt</CardDescription>
            <CardTitle className="text-3xl">{campaigns.length}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Leads verarbeitet</CardDescription>
            <CardTitle className="text-3xl">
              {campaigns.reduce((sum, c) => sum + c.valid_leads, 0)}
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>E-Mails generiert</CardDescription>
            <CardTitle className="text-3xl">
              {campaigns.reduce((sum, c) => sum + c.total_emails, 0)}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Kampagnen-Liste */}
      {campaigns.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <Mail className="mb-4 h-12 w-12 text-muted-foreground" />
            <h3 className="mb-2 text-lg font-medium">Keine Kampagnen vorhanden</h3>
            <p className="mb-4 text-sm text-muted-foreground">
              Laden Sie eine Apollo CSV-Datei hoch, um Ihre erste Kampagne zu starten.
            </p>
            <Link href="/upload">
              <Button>
                <Upload className="h-4 w-4" />
                CSV hochladen
              </Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {campaigns.map((campaign) => (
            <Card key={campaign.id} className="transition-shadow hover:shadow-md">
              <CardContent className="flex items-center justify-between p-4">
                <div className="flex items-center gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium">{campaign.name}</h3>
                      <Badge variant={STATUS_VARIANTS[campaign.status]}>
                        {STATUS_LABELS[campaign.status]}
                      </Badge>
                    </div>
                    <div className="mt-1 flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        {campaign.valid_leads} Leads
                      </span>
                      <span className="flex items-center gap-1">
                        <Mail className="h-3 w-3" />
                        {campaign.total_emails} E-Mails
                      </span>
                      <span>
                        {new Date(campaign.created_at).toLocaleDateString("de-DE", {
                          day: "2-digit",
                          month: "2-digit",
                          year: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(campaign.id)}
                  >
                    <Trash2 className="h-4 w-4 text-muted-foreground" />
                  </Button>
                  <Link href={`/campaigns/${campaign.id}`}>
                    <Button variant="outline" size="sm">
                      Öffnen
                      <ArrowRight className="h-3 w-3" />
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
