# Future clinical evidence library — proposal only

## Research goal
Support clinicians in reviewing and comparing possible reference patterns, with explicit evidence sources and uncertainty, so they can investigate possibilities rather than relying on the model's unsupported assertions.

## Proposed reference schema
Case type; condition or reference concept; clinician-confirmed diagnosis and basis; observational attributes; modality and image acquisition context; source provenance and image-use license; laboratory observations with unit/range provenance; expert adjudication; population and skin-tone coverage; uncertainty; known confounders; reference date; follow-up verification and review status.

## Validation gates
Use licensed cases and adjudicated ground truth. Separate training, retrieval and blinded test sets by patient, site, and source. Assess sensitivity/specificity and calibration where clinically appropriate, fairness across skin tones, false negatives, false positives, workflow failure modes, generalizability, clinician usability, regulatory status and clinical governance.

**Not included in v0.1:** actual diagnostic image matching, cancer risk flags, medical triage, clinical lab ingestion, clinical scoring or patient care. No software result may automatically rule out a disease.
