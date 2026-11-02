# Clinical Vision Evals

[![Python CI](https://github.com/AlimangoStudio/clinical-vision-evals/actions/workflows/ci.yml/badge.svg)](https://github.com/AlimangoStudio/clinical-vision-evals/actions/workflows/ci.yml)

**Open source, synthetic-data-first reference-library and evaluation toolkit** for studying AI-assisted clinical image observations and clinician-facing case comparisons. Maintained by **Alimango Studio**. Apache-2.0 software license; all example data and synthetic diagrams are CC0-1.0.

> **RESEARCH PROTOTYPE — NOT CLINICALLY VALIDATED.** Does not diagnose, screen for cancer, detect emergencies, eliminate diseases, determine testing, prescribe, or replace a clinician. No actual medical images or patient records are included. In v0.1 the library is an **illustrative prototype** with fabricated pattern metadata, NOT a validated clinical reference database.

## Why this is useful

A clinician can record **observed** features and clinician-interpreted lab-status flags, then view which *illustrative reference patterns* share those features, with original educational source links and limitations. An unmatched pattern **is never ruled out**. This makes structured clinical-differential research easier to evaluate without claiming medical performance.

Long-term objective (requires separate validation and regulatory work): clinician-facing support for comparing vetted clinical evidence from licensed images, lab context, and verified diagnoses; display multiple hypotheses for professional consideration and independent verification. Not enabled in v0.1.

## Quick start (offline, no API key)

```bash
python -m pip install -e .
clinical-vision-evals match --library examples/library --query examples/queries/synthetic-itchy-rash.json
clinical-vision-evals match --library examples/library --query examples/queries/synthetic-changing-spot.json
clinical-vision-evals review-sheet --library examples/library --query examples/queries/synthetic-changing-spot.json
python -m unittest discover -s tests -v
python scripts/check_public_artifacts.py
```

The matching engine returns overlapping tags, provenance, and the limitations for each case. `review-sheet` creates a blank, synthetic-only worksheet where a physician could later document their own comparison and questions; it never fills in diagnostic decisions. It deliberately does **not** emit diagnosis labels, confidence percentages, clinical exclusion claims, risk scores or priorities. The reference library is sparse, synthetic and illustrative.

## Codex-only API policy

- **Development:** OpenAI Codex for coding, tests, code review and OSS maintenance (`AGENTS.md`).
- **Optional API demonstration:** only OpenAI Responses API with a fixed `gpt-5.3-codex` model. No fallback or third-party provider adapters.
- **Model limitation:** Codex is optimized for code, NOT validated for medical image interpretation. Synthetic diagrams only. Nothing in this project claims Codex is a clinical model or that a Codex OSS grant authorizes medical inference.
- **Default:** zero network activity. A remote call requires `--allow-api`, `OPENAI_API_KEY`, and a SHA-256-allowlisted synthetic fixture.

```bash
# OPTIONAL and billable; never run on patient images. See docs/CODEX.md.
export OPENAI_API_KEY=... # set locally, never commit
clinical-vision-evals codex-observe \
  --image examples/fixtures/synthetic_shape.png \
  --manifest examples/fixtures/manifest.json \
  --allow-api
```

**No real patient data or medical image should ever be supplied to the public CLI or the OpenAI adapter.** The hash allowlist is a guardrail, not a full PHI inspection system.

## Scope boundary

| Open-source project | Remains proprietary to PAPPS |
|---|---|
| Synthetic reference-case schema and example library | Doctor's Corner application, chart UI, EMR and actual clinical records |
| Descriptive overlap matcher, evidence provenance | Active clinic protocols, procedures, treatment limits, injection plans |
| Portable evaluation harness and synthetic tests | Private prompts, model selection/orchestration, billing, job queues |
| Codex-only synthetic demonstration adapter | Real clinic image processing, patient-facing predictions and any clinical deployment |
| Privacy/publication gate examples | User identity and access control, tenant isolation, audit infrastructure |

We do **not** copy PAPPS private code or prompts into this repository. The open-source project is independently implemented.

## Medical/regulatory boundary

Merely calling software an 'assistant' or 'not a source of truth' does not exempt it from medical-device regulations. In particular, tools intended to interpret medical images, raise cancer alerts, or recommend testing may qualify as regulated software. See [regulatory considerations](docs/REGULATORY.md), [validation](docs/VALIDATION.md) and [data governance](docs/DATA_GOVERNANCE.md). No prospective clinical use without independent validation, security/privacy review and local regulatory assessment.

## Links

- [Architecture and PAPPS private boundary](docs/ARCHITECTURE.md)
- [Codex-only integration policy](docs/CODEX.md)
- [Data and licensing policy](docs/DATA_GOVERNANCE.md)
- [Safety and clinical validation gates](docs/VALIDATION.md)
- [Threat model](docs/SECURITY_MODEL.md)
- [Contribution guide](CONTRIBUTING.md)

## License

Software is Apache-2.0. Example records and synthetic diagram are created specifically for this repository and dedicated to CC0-1.0. External webpages are *linked*, not copied; each publisher retains its rights. Trademarks remain with their owners.