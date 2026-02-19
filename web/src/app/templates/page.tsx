"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getAvailableTemplates, getTemplateContent } from "@/lib/template-engine";
import { SEGMENTATION_RULES } from "@/lib/segmentation-rules";
import { FileText, Eye } from "lucide-react";

export default function TemplatesPage() {
  const templates = getAvailableTemplates();
  const [selected, setSelected] = useState<{
    companyId: string;
    segmentId: string;
  } | null>(null);

  const selectedContent = selected
    ? getTemplateContent(selected.companyId, selected.segmentId)
    : null;

  const companyDisplayName = (id: string): string =>
    SEGMENTATION_RULES.segmentierung[id]?.display_name || id;

  // Gruppierung nach Firma
  const grouped: Record<string, typeof templates> = {};
  for (const t of templates) {
    if (!grouped[t.companyId]) grouped[t.companyId] = [];
    grouped[t.companyId].push(t);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">E-Mail-Templates</h1>
        <p className="text-muted-foreground">
          Übersicht aller verfügbaren E-Mail-Vorlagen nach Firma und Segment
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Template-Liste */}
        <div className="space-y-4">
          {Object.entries(grouped).map(([companyId, companyTemplates]) => (
            <Card key={companyId}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <FileText className="h-4 w-4" />
                  {companyDisplayName(companyId)}
                </CardTitle>
                <CardDescription>
                  {companyTemplates.length} Templates
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {companyTemplates.map((t) => (
                    <div
                      key={`${t.companyId}-${t.segmentId}`}
                      className={`cursor-pointer rounded-md border p-3 transition-colors hover:bg-accent ${
                        selected?.companyId === t.companyId &&
                        selected?.segmentId === t.segmentId
                          ? "border-primary bg-accent"
                          : ""
                      }`}
                      onClick={() =>
                        setSelected({
                          companyId: t.companyId,
                          segmentId: t.segmentId,
                        })
                      }
                    >
                      <div className="flex items-center justify-between">
                        <Badge variant="outline">{t.segmentId}</Badge>
                        <Eye className="h-3 w-3 text-muted-foreground" />
                      </div>
                      <p className="mt-1 truncate text-sm text-muted-foreground">
                        {t.subject}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Template-Vorschau */}
        <div className="lg:sticky lg:top-20">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5" />
                Template-Vorschau
              </CardTitle>
            </CardHeader>
            <CardContent>
              {selectedContent ? (
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-medium text-muted-foreground">
                      Firma
                    </p>
                    <p className="text-sm">
                      {companyDisplayName(selected!.companyId)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs font-medium text-muted-foreground">
                      Segment
                    </p>
                    <Badge variant="secondary">{selected!.segmentId}</Badge>
                  </div>
                  <div>
                    <p className="text-xs font-medium text-muted-foreground">
                      Betreff
                    </p>
                    <p className="text-sm font-medium">
                      {selectedContent.subject}
                    </p>
                  </div>
                  <hr />
                  <div>
                    <p className="mb-2 text-xs font-medium text-muted-foreground">
                      Body (mit Platzhaltern)
                    </p>
                    <pre className="whitespace-pre-wrap rounded-md bg-muted p-4 text-sm leading-relaxed">
                      {selectedContent.body}
                    </pre>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    <p className="w-full text-xs text-muted-foreground">
                      Verfügbare Platzhalter:
                    </p>
                    {[
                      "{{vorname}}",
                      "{{nachname}}",
                      "{{firma}}",
                      "{{position}}",
                      "{{kernleistung}}",
                      "{{icebreaker}}",
                      "{{pdf_link}}",
                    ].map((p) => (
                      <Badge key={p} variant="outline" className="font-mono text-xs">
                        {p}
                      </Badge>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="py-8 text-center text-sm text-muted-foreground">
                  Wählen Sie ein Template aus der Liste
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
