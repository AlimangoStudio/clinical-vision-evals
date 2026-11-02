# Clinical Vision Evals — Project Charter

**Mission:** Build an open-source, reproducible research foundation for integrating structured clinical evidence and studying physician-reviewed, evidence-linked possible explanations. This is a product direction and engineering specification, **not a grant-only demonstration** and not a claim of clinical effectiveness.

**Current state:** synthetic-only, non-diagnostic prototype. It does not interpret real CT/MRI/X-ray pixels, diagnose disease, recommend testing, or predict prognosis. It uses fictional reference patterns. Patient data must never enter the public repository or its hosted CI.

## 1. Aggregate the clinical picture

Study a single evidence ledger integrating patient-reported symptoms, timing and history; independent physician examination and initial clinical impression; laboratory measurements and reference intervals; X-ray, CT, MRI and ultrasound reports; clinical photographs; pathology and biopsy reports; medicines, previous results and longitudinal changes. This list is the *future objective*, not present clinical functionality. All source records must retain dates, originating parties, original wording, method, modality, measured units, uncertain extraction status and usage rights. A model-extracted observation must not be silently promoted to a clinician-confirmed fact.

## 2. Physician-first, before AI suggestions

1. Ingest only authorized records and make the originals reviewable by a qualified clinician.
2. Physician **independently documents** history, examination, concerns, hypotheses, and missing information without seeing generated hypotheses. This is mandatory.
3. Persist a versioned, immutable, timestamped, clinician-attributed baseline with an independent audit mechanism. A SHA-256 of a client-supplied record is useful only as a prototype checksum, not a secure production signature.
4. Perform AI research independently, without treating the doctor's preliminary diagnostic label as a model hint. After analysis compare candidate explanations to the baseline and label disagreements.
5. Display possible explanations only **after** the baseline gate; show supporting and conflicting findings, source provenance, unresolved questions, and known model limitations.
6. Clinician must independently decide whether to consider, investigate, reject or defer any possibility. Record the *after-AI* clinician assessment separately.

## 3. Cross-reference, do not blindly eliminate

Normalize duplicates and identify weak or irrelevant evidence for a focused interface while preserving all original records. Retain contradictions and information missingness. Missing, not observed, explicitly negative, low-confidence and contradictory are different states. Do not hide serious conditions simply because a reference-library match is low or absent. A descriptive overlap is **never** a disease probability or proof of cause. More than one underlying cause may explain one patient's observations.

### What further information might help?

The research framework may highlight diagnostic *questions* or missing source information that the physician might investigate independently. It must not auto-order or recommend patient-specific tests, imaging views, lumbar puncture, biopsy, or other invasive procedures. Such decisions depend on patient-specific contraindications, validated guidance and clinician judgment. Hypotheses about an underlying cause are different from prognosis, which requires separate validated outcome modeling.

## 4. Open-source components

- Schema validation, source-level provenance, quality and missing-data annotations
- Synthetic data ingestion, reference matching, contradiction detection, cross-modal evidence linkage
- Reproducible evaluation, blinded synthetic tests, physician-baseline gate, audit-contract reference designs
- Public licensing and publication checks, safe synthetic image preparation and Codex engineering instructions

## 5. What stays with PAPPS

Private Doctor's Corner UI, records/EMR, tenant data, real patient media, commercial protocols, clinical treatment planning, dosing, private prompts, model-routing policies, access controls, production queues and costs, billing, credentials and private deployment remain in PAPPS. Open-source code is **standalone** and must not import or depend on PAPPS internals. Shared engineering patterns must be separated from proprietary code and independently reimplemented or consciously released with proper provenance.

## 6. AI / API boundary

Use OpenAI Codex for code assistance, code review and tests; no non-OpenAI provider adapters. Any optional runtime model experiment uses only deliberately synthetic, allowlisted assets behind explicit opt-in. Codex is optimized for software engineering, **not a medically validated clinical imaging model**. Other OpenAI vision and image-generation models have separate capabilities and usage terms; grant credit eligibility must be confirmed. Do not test real medical images using the synthetic demo adapter.

## 7. Research milestones and acceptance gates

- **M0:** Synthetic case schemas, provenance links, 100% test coverage of fail-closed data boundary invariants; no real clinical data.
- **M1:** Generic capture contract and physician-first evidence ledger; prove no possibility list before baseline, reject AI-unverified observations as facts, preserve conflicting evidence, attach source IDs. Automated tests.
- **M2:** Standardized synthetic lab, imaging-report, pathology-report and patient complaint adapters; units, timestamps and source fidelity; reviewer-approved reference catalog design.
- **M3:** Versioned, rights-verified medical knowledge catalog, separate from synthetic fixtures; independent clinical editorial review, copyright checks and rollback mechanism.
- **M4:** Research-grade blinded validation for independent modalities and combined evidence; assess false negatives, hallucinations, missingness, bias, anchoring, drift and clinician decision impact.
- **M5:** External clinical, privacy, security, ethics and regulatory review before any patient-facing or diagnostic use.

No milestone may be described as clinically validated merely because unit tests or a grant application passed.

## Success criterion

A researcher can trace: **what was reported, by whom, when; what the physician thought before AI; what sources an analysis considered; which competing explanations overlap; which observations conflict; what is not known; and how the physician independently reviewed the output afterward.** This is the long-term contribution—not an autonomous diagnosis engine.
