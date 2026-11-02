# OpenAI Codex-only development and research demonstration

This repository uses **OpenAI Codex exclusively** for agent-assisted code development, refactoring, maintenance, tests and documentation. Do not add alternative model-provider adapters.

The optional demonstration adapter sends only the SHA-256-allowlisted synthetic color-shape image to the OpenAI Responses API using a pinned Codex-family model; it is disabled by default and requires both `--allow-api` and a locally configured `OPENAI_API_KEY`.

```bash
python -m pip install -e .
clinical-vision-evals codex-observe --image examples/fixtures/synthetic_shape.png --manifest examples/fixtures/manifest.json --allow-api
```

Codex is a coding-focused model, **not a validated medical image analysis or diagnostic system**. Do not substitute actual patients, clinical photographs, radiology images or lab reports in remote tests. Provider access or model support for images can vary and a test may be rejected; no fallback provider is allowed. API use may incur charges and a grant may impose additional restrictions.
