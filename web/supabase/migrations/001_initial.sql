-- Supabase Schema für Gruppenwerk Lead-E-Mail-Generator

-- Kampagnen
create table if not exists campaigns (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  status text not null default 'uploading'
    check (status in ('uploading', 'segmenting', 'generating', 'completed', 'error')),
  created_at timestamptz not null default now(),
  total_leads int not null default 0,
  valid_leads int not null default 0,
  total_emails int not null default 0,
  skipped_leads int not null default 0,
  companies text[] not null default '{}'
);

-- Leads (importierte Kontakte aus Apollo CSV)
create table if not exists leads (
  id uuid primary key default gen_random_uuid(),
  campaign_id uuid not null references campaigns(id) on delete cascade,
  first_name text not null,
  last_name text not null default '',
  email text not null,
  title text not null default '',
  company_name text not null default '',
  industry text not null default '',
  company_size text not null default '',
  city text not null default '',
  state text not null default '',
  country text not null default '',
  company_website text not null default '',
  keywords text not null default '',
  seniority text not null default '',
  departments text not null default '',
  created_at timestamptz not null default now()
);

-- Generierte E-Mails
create table if not exists generated_emails (
  id uuid primary key default gen_random_uuid(),
  campaign_id uuid not null references campaigns(id) on delete cascade,
  lead_id uuid not null references leads(id) on delete cascade,
  company_id text not null,
  segment_id text not null,
  match_score real not null default 0,
  subject_line text not null,
  body text not null,
  icebreaker text not null,
  pdf_link text not null default '',
  created_at timestamptz not null default now()
);

-- Indices
create index if not exists idx_leads_campaign on leads(campaign_id);
create index if not exists idx_leads_email on leads(email);
create index if not exists idx_emails_campaign on generated_emails(campaign_id);
create index if not exists idx_emails_company on generated_emails(company_id);

-- RLS (aktivieren, wenn Auth hinzugefügt wird)
-- alter table campaigns enable row level security;
-- alter table leads enable row level security;
-- alter table generated_emails enable row level security;
