"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getCampaigns } from "@/lib/store";
import type { Campaign } from "@/lib/types";
import { ArrowRight, Mail, Users, Upload } from "lucide-react";

const STATUS_LABELS: Record<Campaign["status"], string> = {
  uploading: "Hochladen",
  segmenting: "Segmentierung",
  generating: "Generierung",
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

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  useEffect(() => {
    setCampaigns(
      getCampaigns().sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
      ),
    );
  }, []);

  if (campaigns.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Kampagnen</h1>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-16">
            <Mail className="mb-4 h-12 w-12 text-muted-foreground" />
            <h3 className="mb-2 text-lg font-medium">
              Keine Kampagnen vorhanden
            </h3>
            <p className="mb-4 text-sm text-muted-foreground">
              Erstellen Sie eine Kampagne, indem Sie eine CSV-Datei hochladen.
            </p>
            <Link href="/upload">
              <Button>
                <Upload className="h-4 w-4" />
                CSV hochladen
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Kampagnen</h1>
        <Link href="/upload">
          <Button>
            <Upload className="h-4 w-4" />
            Neue Kampagne
          </Button>
        </Link>
      </div>

      <div className="space-y-3">
        {campaigns.map((campaign) => (
          <Link key={campaign.id} href={`/campaigns/${campaign.id}`}>
            <Card className="cursor-pointer transition-shadow hover:shadow-md">
              <CardContent className="flex items-center justify-between p-4">
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
                    {campaign.companies.length > 0 && (
                      <span>
                        {campaign.companies
                          .map((c) =>
                            c.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
                          )
                          .join(", ")}
                      </span>
                    )}
                    <span>
                      {new Date(campaign.created_at).toLocaleDateString("de-DE")}
                    </span>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
