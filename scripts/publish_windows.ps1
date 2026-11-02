$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Tests failed" }
python scripts/check_public_artifacts.py
if ($LASTEXITCODE -ne 0) { throw "Public artifact checks failed" }
git status --short
Write-Host "Review changes for any patient information before a GitHub push."
Write-Host "Repository: https://github.com/AlimangoStudio/clinical-vision-evals"
