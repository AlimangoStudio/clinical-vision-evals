# Maintainer instructions for Codex

**Authoritative engineering specification:** [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md). This is a real, long-term open-source multimodal clinical research project—not a grant demonstration. Do not silently narrow the project to aesthetic photographs or a skin-only classifier.

## Non-negotiable boundaries

- OpenAI Codex is the only coding assistant for this repository. Never add adapters to other AI providers.
- The optional runtime external model remains the fixed gpt-5.3-codex, used **only with hash-allowlisted synthetic diagrams**. Codex is not clinically validated and may not be appropriate for medical-image interpretation; no clinical inference in this project.
- Never commit patient data, medical records, raw medical images, API keys, clinic policies, private PAPPS code, production prompts or live tenant endpoints.
- Synthetic research fixtures only. An input flag saying "synthetic" is **not** sufficient evidence to accept arbitrary uploaded patient information. Review all proposed fixtures before release.
- The project's long-term aim is multimodal clinical *research*: patient-reported symptoms, labs, pathology/biopsies, physician notes, X-ray/CT/MRI reports, visual observations, historical context, and medically reviewed/rights-cleared reference catalogs.
- The **physician-first gate** is mandatory: record the clinician's independent initial observations and impression before revealing AI-generated hypothesis lists. Retain the baseline for comparison. Failure of the gate must fail closed.
- Generated observations must retain provenance and verification status; do not treat exploratory AI descriptions as clinical ground truth. Preserve original evidence and disagreements; do not auto-remove serious conditions.
- Current synthetic reference matches are descriptive overlaps, **not diagnoses, probabilities, prognoses, medical orders, or triage**. Invasive procedures such as lumbar puncture must never be automatically recommended.
- Generic PAPPS workflow invariants may be **independently reimplemented** in this repo with tests, while all proprietary PAPPS systems remain separate. Do not copy application-specific classes, private prompts or clinical protocols.
- For every change, update tests, maintain clinician_review_required, document provenance and limitations. Do not claim clinical validation based on unit tests.
- Run "PYTHONPATH=src python -m unittest discover -s tests -v" and "python scripts/check_public_artifacts.py" before committing.
- Never permit PR content to trigger secret-bearing workflows or run untrusted code with API keys.
- A Codex Open Source Fund grant does not necessarily authorize clinical inference or image generation; obtain written confirmation of approved spending.

## Milestones

See the charter's M0-M6 research roadmap. Prioritize reproducible synthetic test harnesses, source provenance, physician-first review, and licensed medical reference catalogs before making any claims of clinical utility.
