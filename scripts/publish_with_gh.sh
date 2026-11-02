#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/check_public_artifacts.py
git status --short
echo "This project is already hosted under AlimangoStudio/clinical-vision-evals."
echo "Review the diff for secrets/patient data before every push."
echo "Use git push origin main only after the public review."
