-- SAHJONY Movie OS V3 durable orchestration layer
-- Deployed to Supabase project qprlbmcoksrpuvodxjtt on 2026-09-10.

create table if not exists public.agent_tasks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  shot_id uuid references public.shots(id) on delete cascade,
  parent_task_id uuid references public.agent_tasks(id) on delete set null,
  agent_role text not null,
  task_type text not null,
  priority integer not null default 50 check (priority between 0 and 100),
  status text not null default 'queued' check (status in ('queued','running','blocked','completed','failed','cancelled')),
  dependencies uuid[] not null default '{}',
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  attempt integer not null default 0,
  max_attempts integer not null default 3 check (max_attempts between 1 and 10),
  scheduled_at timestamptz,
  started_at timestamptz,
  finished_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.studio_events (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  shot_id uuid references public.shots(id) on delete cascade,
  task_id uuid references public.agent_tasks(id) on delete set null,
  event_type text not null,
  source text not null,
  payload jsonb not null default '{}'::jsonb,
  correlation_id uuid,
  causation_id uuid,
  created_at timestamptz not null default now()
);

create table if not exists public.cinematic_memory (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  scope text not null check (scope in ('project','world','character','scene','shot','asset')),
  scope_id uuid,
  memory_key text not null,
  memory_value jsonb not null,
  locked boolean not null default false,
  version integer not null default 1,
  embedding vector(1536),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(project_id, scope, scope_id, memory_key, version)
);

create table if not exists public.provenance_records (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  shot_id uuid references public.shots(id) on delete cascade,
  render_id uuid references public.renders(id) on delete cascade,
  agent_run_id uuid references public.agent_runs(id) on delete set null,
  task_id uuid references public.agent_tasks(id) on delete set null,
  artifact_type text not null,
  artifact_id text not null,
  provider text,
  model text,
  prompt_hash text,
  input_refs jsonb not null default '[]'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.project_state_versions (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  version bigint not null,
  phase text not null,
  state jsonb not null,
  created_by text not null,
  created_at timestamptz not null default now(),
  unique(project_id, version)
);

create index if not exists agent_tasks_project_status_idx on public.agent_tasks(project_id, status, priority desc);
create index if not exists studio_events_project_created_idx on public.studio_events(project_id, created_at desc);
create index if not exists cinematic_memory_project_scope_idx on public.cinematic_memory(project_id, scope, scope_id);
create index if not exists provenance_project_created_idx on public.provenance_records(project_id, created_at desc);
create index if not exists project_state_versions_project_version_idx on public.project_state_versions(project_id, version desc);

alter table public.agent_tasks enable row level security;
alter table public.studio_events enable row level security;
alter table public.cinematic_memory enable row level security;
alter table public.provenance_records enable row level security;
alter table public.project_state_versions enable row level security;

revoke all on public.agent_tasks, public.studio_events, public.cinematic_memory,
  public.provenance_records, public.project_state_versions from anon;
grant select, insert, update, delete on public.agent_tasks, public.studio_events,
  public.cinematic_memory, public.provenance_records, public.project_state_versions to authenticated;

create policy agent_tasks_project_owner on public.agent_tasks for all to authenticated
using (exists(select 1 from public.projects p where p.id = agent_tasks.project_id and p.owner_id = (select auth.uid())))
with check (exists(select 1 from public.projects p where p.id = agent_tasks.project_id and p.owner_id = (select auth.uid())));

create policy studio_events_project_owner on public.studio_events for all to authenticated
using (exists(select 1 from public.projects p where p.id = studio_events.project_id and p.owner_id = (select auth.uid())))
with check (exists(select 1 from public.projects p where p.id = studio_events.project_id and p.owner_id = (select auth.uid())));

create policy cinematic_memory_project_owner on public.cinematic_memory for all to authenticated
using (exists(select 1 from public.projects p where p.id = cinematic_memory.project_id and p.owner_id = (select auth.uid())))
with check (exists(select 1 from public.projects p where p.id = cinematic_memory.project_id and p.owner_id = (select auth.uid())));

create policy provenance_records_project_owner on public.provenance_records for all to authenticated
using (exists(select 1 from public.projects p where p.id = provenance_records.project_id and p.owner_id = (select auth.uid())))
with check (exists(select 1 from public.projects p where p.id = provenance_records.project_id and p.owner_id = (select auth.uid())));

create policy project_state_versions_project_owner on public.project_state_versions for all to authenticated
using (exists(select 1 from public.projects p where p.id = project_state_versions.project_id and p.owner_id = (select auth.uid())))
with check (exists(select 1 from public.projects p where p.id = project_state_versions.project_id and p.owner_id = (select auth.uid())));
