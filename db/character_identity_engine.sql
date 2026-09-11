-- SAHJONY Character Identity Engine persistence

create table if not exists public.character_identity_packs (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  character_id uuid not null references public.characters(id) on delete cascade,
  version integer not null default 1,
  status text not null default 'draft' check (status in ('draft','locked','retired')),
  immutable_traits jsonb not null default '{}'::jsonb,
  appearance_profile jsonb not null default '{}'::jsonb,
  wardrobe_profile jsonb not null default '{}'::jsonb,
  voice_profile jsonb not null default '{}'::jsonb,
  performance_profile jsonb not null default '{}'::jsonb,
  negative_constraints jsonb not null default '[]'::jsonb,
  reference_asset_ids uuid[] not null default '{}',
  identity_threshold numeric(5,4) not null default 0.9500 check (identity_threshold between 0 and 1),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(character_id, version)
);

create index if not exists character_identity_packs_project_character_idx
on public.character_identity_packs(project_id, character_id, version desc);

alter table public.character_identity_packs enable row level security;
revoke all on public.character_identity_packs from anon;
grant select, insert, update, delete on public.character_identity_packs to authenticated;

create policy character_identity_packs_project_owner
on public.character_identity_packs for all to authenticated
using (
  exists(
    select 1 from public.projects p
    where p.id = character_identity_packs.project_id
      and p.owner_id = (select auth.uid())
  )
)
with check (
  exists(
    select 1 from public.projects p
    where p.id = character_identity_packs.project_id
      and p.owner_id = (select auth.uid())
  )
);
