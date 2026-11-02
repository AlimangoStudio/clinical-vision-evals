# Maintainer instructions for Codex

- This project is an OpenAI Codex-only coding project. Never add adapters to other AI providers.
- The only optional runtime external model is the fixed `gpt-5.3-codex` and it may be used solely with hash-allowlisted synthetic diagrams. Codex is not clinically validated.
- Never add patient data, medical records, API keys, clinic policies, medical photographs, proprietary PAPPS code, production prompts, or live tenant endpoints.
- Features are **reference overlap**, not disease probabilities, medical diagnoses, risk scores, exclusions, or automated triage.
- For changes: update tests, maintain `clinician_review_required`, document provenance and limitations.
- Run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python scripts/check_public_artifacts.py` before committing.
- Do not permit PR content to trigger secret-bearing workflows. Never run untrusted code with API keys.
- A grant from Codex for Open Source is not authorization to use its API credits for clinical inference; obtain written confirmation of approved uses.

## Binding project mission

Read [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) before any substantive feature. Treat this as the long-term implementation objective, not a grant pitch. Enforce physician-first baseline recording before any AI-generated possibilities are displayed. Preserve original evidence and distinguish unverified AI claims from reported facts. No automatic diagnosis, exclusion, patient-specific test orders or prognosis. Every candidate requires evidence provenance and uncertainty. Do not commit PAPPS proprietary runtime source or patient data to this public repository. See docs/PORTING_PROVENANCE.md.
