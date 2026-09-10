# SAHJONY Movie OS V3

An autonomous, state-centric AI movie studio designed to coordinate specialized creative agents, persistent cinematic memory, spatial cinematography, generation providers, QA, budgets, provenance, and final assembly.

## Architecture

```text
Creative Brief
    ↓
Master Director
    ↓
Production Graph + Event Bus
    ├─ Writer / Continuity
    ├─ Art Director / Asset Factory
    ├─ Cinematographer / Lighting / Performance
    ├─ Render Workers / Provider Governor
    ├─ Multimodal QA / Remediation
    └─ Editor / Sound / Final Master
         ↓
Persistent Project State + Canon + Provenance
```

## V3 core

- typed agent task/decision contracts
- narrow tool permissions by department
- versioned canonical project state
- persistent structured cinematic memory
- event-driven orchestration
- dependency-aware production graph
- priority scheduler for parallel departments
- model capability registry
- provider circuit-breaker/fallback governor
- deterministic provenance ledger
- QA ensemble with repair-specific remediation
- automatic approval gates for script, hero assets, shots, and masters
- typed camera-command DSL with handoff/interruption rules
- screen-direction and eyeline continuity guards
- spatial adapter interface for Unreal, Blender, Cesium, or custom stages

## Cinematography DSL

Every canonical shot can carry an executable command instead of a vague motion prompt:

```python
CameraCommand(
    verb="orbit",
    subject="ARIA",
    lens_mm=50,
    radius_m=4.5,
    degrees=110,
    duration_s=5,
    maintain_screen_direction=True,
    maintain_eyeline=True,
)
```

The Cinematographer Agent owns camera/lens/blocking. Other agents cannot mutate those fields without going through the supervisor.

## Autonomous shot loop

```text
SHOT SPEC → ASSETS → GENERATE → QA
                         ↑        ↓
                         └─ REMEDIATE
```
Failed renders produce targeted repair actions, then re-enter generation under retry and budget ceilings. Approved shots can be locked against accidental drift.

## First production manifest

`examples/first_autonomous_sequence.json` defines a reproducible 45-second / 9-shot proof of concept. The dry-run currently estimates 162.5 Higgsfield credits before retries using the configured draft/final routing policy.

## Environment

Server-side only:

- `HF_API_KEY`
- `HF_API_SECRET`
- `HF_SEEDANCE_APPLICATION=seedance_2_5`

Never commit production credentials or expose them through browser-prefixed environment variables.

## Validation

```bash
python -m compileall -q orchestrator tests examples
python examples/plan_sequence.py
pytest -q
```

The orchestration layer intentionally stays provider-agnostic. Generation, voice, music, 3D, and spatial engines are adapters around canonical studio state, not owners of that state.
