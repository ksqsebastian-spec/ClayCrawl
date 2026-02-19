// Lokaler Zustandsspeicher — für den Fall, dass Supabase noch nicht konfiguriert ist
// Speichert Kampagnen und E-Mails im localStorage des Browsers

import type { Campaign, GeneratedEmail, Lead } from "./types";

const CAMPAIGNS_KEY = "claycrawl_campaigns";
const EMAILS_KEY = "claycrawl_emails";
const LEADS_KEY = "claycrawl_leads";

// Kampagnen
export function getCampaigns(): Campaign[] {
  if (typeof window === "undefined") return [];
  const data = localStorage.getItem(CAMPAIGNS_KEY);
  return data ? JSON.parse(data) : [];
}

export function getCampaign(id: string): Campaign | null {
  return getCampaigns().find((c) => c.id === id) ?? null;
}

export function saveCampaign(campaign: Campaign): void {
  const campaigns = getCampaigns();
  const index = campaigns.findIndex((c) => c.id === campaign.id);
  if (index >= 0) {
    campaigns[index] = campaign;
  } else {
    campaigns.push(campaign);
  }
  localStorage.setItem(CAMPAIGNS_KEY, JSON.stringify(campaigns));
}

export function deleteCampaign(id: string): void {
  const campaigns = getCampaigns().filter((c) => c.id !== id);
  localStorage.setItem(CAMPAIGNS_KEY, JSON.stringify(campaigns));

  // Zugehörige Leads und E-Mails löschen
  const emails = getAllEmails().filter((e) => e.campaign_id !== id);
  localStorage.setItem(EMAILS_KEY, JSON.stringify(emails));
  const leads = getAllLeads().filter((l) => l.campaign_id !== id);
  localStorage.setItem(LEADS_KEY, JSON.stringify(leads));
}

// Leads
export function getAllLeads(): Lead[] {
  if (typeof window === "undefined") return [];
  const data = localStorage.getItem(LEADS_KEY);
  return data ? JSON.parse(data) : [];
}

export function getLeadsByCampaign(campaignId: string): Lead[] {
  return getAllLeads().filter((l) => l.campaign_id === campaignId);
}

export function saveLeads(leads: Lead[]): void {
  const existing = getAllLeads();
  localStorage.setItem(LEADS_KEY, JSON.stringify([...existing, ...leads]));
}

// E-Mails
export function getAllEmails(): GeneratedEmail[] {
  if (typeof window === "undefined") return [];
  const data = localStorage.getItem(EMAILS_KEY);
  return data ? JSON.parse(data) : [];
}

export function getEmailsByCampaign(campaignId: string): GeneratedEmail[] {
  return getAllEmails().filter((e) => e.campaign_id === campaignId);
}

export function saveEmails(emails: GeneratedEmail[]): void {
  const existing = getAllEmails();
  localStorage.setItem(EMAILS_KEY, JSON.stringify([...existing, ...emails]));
}
