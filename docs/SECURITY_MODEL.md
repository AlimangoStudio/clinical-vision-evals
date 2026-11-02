# Security and threat model

Potential failures include secret leakage, patient/PHI uploads, accidental API requests, malicious reference data, misleading diagnostic interpretations, contaminated evaluation labels and misuse as a medical device.

Current safeguards:
- Public fixture checks reject a number of private paths and sensitive extensions; **not** a comprehensive PHI/DLP scanner.
- The API adapter rejects arbitrary images and manifest substitutions; only a hash-pinned synthetic diagram is accepted.
- API calls are explicit opt-in with no fallback provider.
- API request includes `store: false` but platform/account-specific policies must still be reviewed.
- No cloud-based model is required for the offline reference demonstration.
- Tests verify refusal on modified fixtures, personal identifiers and nonsynthetic cases.

No guarantees are provided. For patient-bearing future work, independent security and privacy audits are prerequisites.
