# Source extraction and intellectual-property boundary

**Review scope:** existing private PAPPS Doctor's Corner capture-first Vision pipeline and its related controller/worker design were inspected for reusable concepts. This is an explicit, limited extraction of generic engineering behavior, **not a bulk copy or publication of the PAPPS source tree**.

## Reused architectural invariants, independently implemented in Python

| Existing PAPPS behavior reviewed | Public implementation | What changed |
| --- | --- | --- |
| Complete standardized capture set, exactly one saved capture for each expected view, in prescribed order | capture_contract.py | Generic synthetic case tokens and arbitrary view metadata; no procedures, patient IDs, EMR queries, model access, storage paths or clinic rules |
| Capture/clinical observations are separate from optional model analysis | evidence.py | Evidence assembly is offline and synthetic; no model calls or private job/session state |
| Physician-authored findings remain separate from provisional AI observations | evidence.py | Synthetic physician-first baseline is sealed and required before revealing research reference overlaps; AI-unverified observations excluded from reference matching |
| User-facing output requires clinical review and provenance | evidence.py | Preserve modality, origin, source title and time; list source disagreements and absent modalities without prescribing tests |

The *new* physician-first baseline gate and cross-modal research inventory reflect the open-source project charter; they are not claims that the private PAPPS system currently implements this exact behavior.

## Deliberately excluded

- Any private PHP/Laravel controller, ORM model, route, database schema, tenant authorization, service container or job worker implementation.
- Patient-identifying fields, image bytes, medical records, real laboratory values, credential stores or live URLs.
- Aesthetic protocols, injectable planning, proprietary prompts, provider selection, pricing, private model-routing/fallback strategies and business workflows.
- The private Rust worker; its operational code is not needed for the public research toolkit.
- Any clinical image interpretation model or clinical output generator.

## Review safeguards

- The open-source functions are standalone, written for the public Python package; they do not import or require PAPPS.
- Every new workflow is synthetic-only, disconnected from production systems, and tested for misuse.
- A synthetic label or hash cannot reliably de-identify real patient information. The public repository must never be given actual patient input.
- No inference that passing tests validates medical performance.
