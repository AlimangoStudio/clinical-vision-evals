# Reuse audit — PAPPS to Clinical Vision Evals

**Owner-authorized engineering adaptation.** The original PAPPS repository remains private. This public project has no dependency on it.

| Private PAPPS source reviewed | Public adaptation | What is deliberately excluded |
|---|---|---|
| `frontend/cms-vue/src/lib/photoCapture.js` | `adapters/browser/syntheticPhotoCapture.mjs`: dimensions and browser-canvas re-encoding concepts | Chart photo history, clinic UI, patient metadata, original-file passthrough |
| `backend/app/Services/Clinical/VisionSessionService.php` | `src/clinical_vision_evals/capture_contract.py`: synthetic view order, uniqueness and saved-record validation | Eloquent models, patient/tenant IDs, procedure mapping, queue orchestration and credentials |
| `backend/app/Services/Clinical/VisionSessionService.php`, `backend/app/Services/Clinical/AestheticVisionService.php` | `src/clinical_vision_evals/evidence.py`: independently implemented physician-first evidence ledger and structured-overlap research | Private model routing, procedural prompts, HA/Botox/injection protocols and clinical decision logic |
| `backend/app/Support/Media/AiImagePayload.php` | Metadata-stripping and image-sanitization *design principles* adopted in synthetic browser re-encoding | PHP server implementation; PDFs never forwarded from this adapter |

**No production secrets, real images, patient records, personal identifiers, tokens, private routes or proprietary clinical procedures were copied.** This is not a comprehensive code-similarity audit; review future contributions before public merge. Some utility ideas are adapted from owner-controlled private source; public implementation must be reviewed for licensing and copyright clearance. The project README and LICENSE remain Apache-2.0.
