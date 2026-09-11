# SAHJONY Movie OS V3 — Durable Runtime

The Movie OS now persists autonomous production state in Supabase rather than relying on process memory.

## Durable primitives

- `agent_tasks`: department work queue, dependencies, attempts, priority and results.
- `studio_events`: append-only production event stream.
- `cinematic_memory`: versioned canonical project/world/character/scene/shot memory with lock state.
- `provenance_records`: lineage for generated media and agent artifacts.
- `project_state_versions`: immutable snapshots of Movie OS state.

All five tables use owner-scoped Row Level Security. Server workers use Supabase secret/service credentials only on trusted backends; browser code must never receive them.

## Higgsfield execution

`HiggsfieldWorker` uses the official `higgsfield_client` SDK contract already proven in the SAHJONY import/export platform:

- `submit_async`
- `status_async`
- `result_async`
- `cancel_async`

The worker persists `render.submitted` events and generated-video provenance. Credentials remain environment-only via `HF_API_KEY`, `HF_API_SECRET`, and `HF_SEEDANCE_APPLICATION`.

## Runtime flow

`DurableMovieStudioOS` bootstraps canonical state, stores a project snapshot, persists the bootstrap event, schedules department tasks locally, and mirrors them into `agent_tasks` plus `studio_events`.
