create table if not exists public.provider_runtime_state (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  provider text not null,
  status text not null default 'healthy'
    check (status in ('healthy','degraded','blocked')),
  failures integer not null default 0,
  block_reason text,
  blocked_until timestamptz,
  last_failure_at timestamptz,
  last_success_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  unique(project_id, provider)
);

alter table public.provider_runtime_state enable row level security;

drop policy if exists provider_runtime_state_project_owner
  on public.provider_runtime_state;
create policy provider_runtime_state_project_owner
  on public.provider_runtime_state for all to authenticated
  using (exists (
    select 1 from public.projects p
    where p.id = project_id and p.owner_id = (select auth.uid())
  ))
  with check (exists (
    select 1 from public.projects p
    where p.id = project_id and p.owner_id = (select auth.uid())
  ));

grant select, insert, update, delete
  on public.provider_runtime_state to authenticated;
