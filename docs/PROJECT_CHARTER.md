# Clinical Vision Evals — Project Charter and Engineering Contract

Status: **long-term project requirements, 2026-11-03**. Not a claim of implemented or clinically validated capabilities.

## Mission

Build a genuine, useful, **open-source multimodal clinical evidence research toolkit** that can aggregate authorized information, preserve original observations and provenance, compare findings against curated reference evidence, and evaluate possible underlying-cause hypotheses for independent physician assessment.

This project exists whether or not any grant is approved. It is not a temporary grant showcase and it must not quietly become a skin-only image classifier. Research quality, independent reproducibility and human safety come before claims of clinical performance.

## Physician-first principle (mandatory)

1. Assemble the source inventory, but **do not show AI hypotheses, differential lists, candidate diagnoses or prognostic narratives**.
2. The physician records independently: chief concern, symptoms, history, examination/visual observations, relevant positives and negatives, *their own initial clinical impression*, uncertainty and open questions.
3. Seal a dated, authored, versioned baseline *before AI hypothesis disclosure*. Retain the immutable initial version and append revisions instead of rewriting it. The synthetic demonstration uses a digest; a clinical product requires genuine authenticated, tamper-evident audit infrastructure.
4. Independently normalize evidence and compare literature sources. When developing automated hypotheses, do **not** feed the physician's initial diagnostic guess to the hypothesis generator merely to make the model agree. Physician observations can be evidence; the initial diagnostic impression is preserved for later comparison.
5. After the baseline is sealed, reveal an evidence-linked research report side-by-side with the physician's baseline, highlighting agreement, contradictions, uncertainties, missing evidence and model limitations.
6. The physician owns review, verification, testing and any final clinical conclusions. Model disagreement is a prompt to examine sources, not an automatic correction of the physician.

The default system must **fail closed** if this sequence cannot be demonstrated.

## Sources to evaluate together

- Patient-reported complaints: symptom wording, onset, duration, progression, severity and relevant history.
- Clinician-authored notes: examination, independent initial impression, prior assessments, medications and longitudinal progress.
- Laboratories: measured values, units, collection time, reference intervals, assay context and source reports. Never silently turn a value into a diagnosis.
- Biopsy, pathology and specialist reports: distinguish original authored report findings from any AI summary.
- Radiology: X-ray, CT, MRI and other reports. Record study type, body site, technique, acquisition timing and whether raw diagnostic images are actually available.
- Clinical photographs and visual observations: distinguish confirmed clinician observations from **unverified AI-generated descriptions**.
- Prior records and serial results: change over time matters; apparent contradictions can reflect different time points.
- Medical references: reputable guidelines, papers and validated datasets with license, publication date, source URL, evidence quality, version and independent verification state.

**Input acquisition is separate from extraction and interpretation.** The public repository never automatically fetches real patient records. All current examples are synthetic. A future real-data deployment requires separate approvals, permissions, privacy engineering and clinical/regulatory review.

## Target architecture (not implemented in v0.1)

1. **Ingestion adapters** for explicitly authorized, governed research datasets: structured data, clinical documents and image metadata. Define format-specific parsers independently. No hidden bulk scraping.
2. **Provenance and normalization**: retain raw-source references, collection date, clinician/source attribution, standardized concepts and terminology, units, negation and uncertainty. Never overwrite source evidence with generated guesses.
3. **Physician baseline barrier**: independent authored assessment sealed and auditable before AI hypotheses become visible.
4. **Multimodal extraction**: separately test text/document parsing and vision observations on permitted data; treat generated findings as provisional. Track extraction accuracy and failures.
5. **Reference catalog**: medically reviewed, rights-cleared sources, citations, versions, evidence levels, conflicts and outdated information. Synthetic fixtures are not medical ground truth.
6. **Evidence reconciliation**: deduplicate, identify possible source disagreements, track missing material and distinguish irrelevant background from potentially important red flags. Do not permanently delete or conceal raw evidence.
7. **Hypothesis research**: when separately validated, form a limited, explainable set of competing potential underlying-cause hypotheses, showing evidence for/against and uncertainty. Avoid forced single-cause explanations, made-up probabilities, unsupported exclusion and premature diagnostic closure.
8. **Evidence gaps**: identify missing *information* that might distinguish hypotheses: unanswered history questions, missing records, prior test reports, technical coverage of an already-acquired imaging study. If discussing possible further investigations, present them as literature-grounded questions requiring clinician judgment, not test orders.
9. **Independent review and feedback**: physician reconciliation, errors and blinded comparisons; update research evaluation without training on data unless expressly authorized.
10. **Safety evaluation and release gates**: formal intended use, independent clinical validation, human-factors testing, privacy/security review and local regulatory clearance wherever applicable.

## Prohibited autonomous behavior

- No diagnosis, cancer detection/screening claims, prognostic predictions, medication advice, dose, treatment, emergency triage or unreviewed clinical actions.
- No automatic ruling out serious illness because a pattern does not match the catalog. No assumption that absent data equals a negative test.
- No autonomous orders or procedural recommendations. **Lumbar puncture, biopsy, CT, MRI, or other invasive/high-stakes tests are not inferred as instructions from generic symptom matches**. The system can expose evidence gaps and cited contextual literature for professional assessment only after appropriate validation.
- No interpretation of specialized medical imaging as if a general-purpose vision model were a validated radiologist or pathologist.
- No publishing actual clinical photographs, health records, identifiable samples, proprietary clinic treatment protocols, credentials or private PAPPS systems.
- No fabricated clinical reference citations, invented accuracy rates or synthetic generated images presented as verified cases.

## Public versus proprietary boundaries

**Public toolkit:** portable schemas, synthetic fixtures, evidence inventory and provenance, physician-first research gating, capture metadata validation, reproducible comparisons, literature catalog tooling, safety benchmarks, tests and documentation.

**Private PAPPS:** Doctor's Corner UI/EMR, real patient media/storage, tenancy and permissions, session execution, provider keys, commercial model routing, proprietary prompts, active clinic protocols, treatment planning, billing and production deployment. Do not copy private routes, identifiers, secrets or patient data. Generic invariants inspired by PAPPS can be independently implemented in Python and tested.

The open-source project should remain usable without installing PAPPS.

## OpenAI policy

Codex is the project's **exclusive coding assistant**; no third-party AI-provider adapters. The optional runtime API demonstration remains fixed to the permitted OpenAI Codex-family synthetic fixture experiment defined by the existing repository. Codex is not represented as a clinically validated diagnostic model. Future multimodal or image-generation research needs a separately scoped, suitable OpenAI model, provider terms, data governance review, and written clarification of any grant credit restrictions. **No patient data through the public API demo.**

## Deliverable sequence and acceptance gates

| Milestone | Deliverable | Required verification |
| --- | --- | --- |
| M0 | Synthetic-only reference matcher and transparent limitations | Offline tests, zero API calls by default (existing v0.1) |
| M1 | Port generic PAPPS-tested *invariants*: capture completeness, ownership, explicit review boundary | Public-safe independent source, tests, no PAPPS dependencies |
| M2 | Provenance-tagged synthetic multimodal evidence bundle and physician baseline gate | Synthetic tests covering missing/edited baselines, conflicts and AI-origin exclusion |
| M3 | Document/lab/report extraction evaluation harness | Gold-standard synthetic data, extraction accuracy, provenance/errors; no live patients |
| M4 | Licensed and versioned reference catalog with expert-review workflow | Audit of rights and medical source quality, versioned citations |
| M5 | Research-only differential hypothesis and evidence-gap benchmark | Blinded comparison against expert-adjudicated references; measure false negatives and harmful omissions |
| M6 | Prospective clinical research feasibility | Ethics, security, clinician validation, regulatory intended-use assessment BEFORE patient workflows |

**Current implementation is an unvalidated research prototype; it must not be deployed as clinical decision support.** Each milestone needs tests, documented limitations and measurable acceptance evidence, not a claim of safety inferred from passing unit tests.

## Contributor checklist

Before merging changes: confirm public-safe provenance and rights, physician-first reveal gate, explicit synthetic-only boundary, no silent diagnostic inference, no unjustified medical claims, no secrets or patient metadata, robust error states, all unit/public-artifact checks passing, and release documentation reflecting what actually exists.
