# SAHJONY AI Movie Studio V2

V2 turns the V1 shot runtime into a production-ready **queued movie execution plan** with explicit cost governance and provider routing.

## New in V2

- 45-second / 9-shot autonomous proof-of-concept: **The Compass in the Rain**
- persistent character/style bibles
- provider registry and ordered fallback chain
- project/shot budget guardrails
- deterministic dry-run cost planner
- hero-shot premium routing
- draft-shot economical routing
- production manifest ready for live generation

## Planned generation economics

Using the currently observed 5-second 720p preflight values:

- Seedance 2.0 Mini: 12.5 credits / 5 sec
- Cinema Studio Video 3.0: 25 credits / 5 sec

The 9-shot manifest routes 4 hero shots to Cinema Studio and 5 normal shots to Seedance Mini, for an estimated first-pass total of **162.5 credits** before retries.

## Environment

Server-side only:

- `HF_API_KEY`
- `HF_API_SECRET`
- `HF_SEEDANCE_APPLICATION=seedance_2_5`

Never commit secrets or expose them client-side.

## Run locally

```bash
python examples/plan_sequence.py
pytest -q
```
