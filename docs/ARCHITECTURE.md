# Architecture and scope

Version 0.1 is an independent synthetic-only demonstration. It does not import, depend upon, or expose PAPPS.

- `library.py` validates synthetic reference records and query objects.
- `matcher.py` compares explicitly described observations by exact feature overlap; order is **not** likelihood.
- `review.py` emits an unfilled clinician review worksheet; no autonomous exclusions.
- `codex.py` is a separately gated optional OpenAI Codex-family synthetic image demonstration.
- `cli.py` exposes the offline matcher and review sheet commands.
- `tests/` exercises safety and behavior without secrets or API calls.

## Private PAPPS boundary

Keep patient records, clinic workflows, treatment protocols, injection plans, doctor chart UI, private prompts, model routing, internal worker routes, pricing, permissions, tenant isolation, and patient image storage inside private PAPPS. No reverse connection is built into this repo.

## Threat boundaries

Case examples are synthetic only. In v0.1 no user-uploaded clinical cases, patient images, credentials, PHI, or clinical inference are accepted. Even a visually similar pattern cannot confirm or exclude a diagnosis.
