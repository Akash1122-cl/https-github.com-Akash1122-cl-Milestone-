"""
validate_project.py — Architecture Compliance Test Suite
=========================================================
Tests every completed phase (1–14) against the spec in Docs/architecture.md.
Run from the project root:  python scripts/validate_project.py
"""

import json
import os
import re
import sys
import ast
from pathlib import Path

ROOT = Path(__file__).parent.parent  # c:\Milestone 2\

PASS  = "  ✅ PASS"
FAIL  = "  ❌ FAIL"
WARN  = "  ⚠️  WARN"

results = []

def check(name, passed, detail=""):
    status = PASS if passed else FAIL
    results.append((name, passed, detail))
    print(f"{status}  {name}" + (f"\n         → {detail}" if detail else ""))

def warn(name, detail=""):
    results.append((name, None, detail))
    print(f"{WARN}  {name}" + (f"\n         → {detail}" if detail else ""))


print("=" * 65)
print("  MUTUAL FUND FAQ ASSISTANT — Architecture Compliance Tests")
print("=" * 65)

# ─────────────────────────────────────────────────────────────
# PHASE 2 — Directory Structure
# ─────────────────────────────────────────────────────────────
print("\n📂  PHASE 2 — Directory Structure")

required_dirs = [
    "data/raw",
    "data/processed",
    "scripts",
    "Docs",
    ".github/workflows",
]
for d in required_dirs:
    p = ROOT / d
    check(f"Directory exists: {d}", p.is_dir())

required_files = [
    "scripts/ingest.py",
    "scripts/index.py",
    "Docs/architecture.md",
    "Docs/raw_data.md",
    "Docs/chunking_embedding_architecture.md",
    "Docs/preview.md",
    ".github/workflows/ingest.yml",
    ".gitignore",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
]
for f in required_files:
    p = ROOT / f
    check(f"File exists: {f}", p.is_file())

# ─────────────────────────────────────────────────────────────
# PHASE 6 — GitHub Actions Workflow
# ─────────────────────────────────────────────────────────────
print("\n⚙️   PHASE 6 — GitHub Actions Workflow")

yml_path = ROOT / ".github/workflows/ingest.yml"
yml_text = yml_path.read_text(encoding="utf-8") if yml_path.exists() else ""

check("Cron schedule present (9:15 AM IST = 03:45 UTC)",
      "45 3 * * *" in yml_text,
      "Cron string not found" if "45 3 * * *" not in yml_text else "")

check("workflow_dispatch (manual trigger) present",
      "workflow_dispatch" in yml_text)

check("ingest job defined",
      re.search(r"^\s*ingest\s*:", yml_text, re.MULTILINE) is not None)

check("embed job defined",
      re.search(r"^\s*embed\s*:", yml_text, re.MULTILINE) is not None)

check("embed job depends on ingest (needs: ingest)",
      "needs: ingest" in yml_text or "needs:\n    - ingest" in yml_text or "needs: [ingest]" in yml_text)

check("actions/checkout@v4 used",
      "actions/checkout@v4" in yml_text)

check("actions/upload-artifact@v4 used",
      "actions/upload-artifact@v4" in yml_text)

check("actions/download-artifact@v4 used",
      "actions/download-artifact@v4" in yml_text)



check("playwright install chromium present",
      "playwright install chromium" in yml_text)

# ─────────────────────────────────────────────────────────────
# PHASE 12 — ingest.py structure
# ─────────────────────────────────────────────────────────────
print("\n🕷️   PHASE 12 — ingest.py (Scraper) Validation")

ingest_path = ROOT / "scripts/ingest.py"
ingest_text = ingest_path.read_text(encoding="utf-8") if ingest_path.exists() else ""

# Syntax check
try:
    ast.parse(ingest_text)
    check("ingest.py — valid Python syntax", True)
except SyntaxError as e:
    check("ingest.py — valid Python syntax", False, str(e))

check("Uses playwright or BeautifulSoup4",
      "playwright" in ingest_text.lower() or "beautifulsoup" in ingest_text.lower() or "bs4" in ingest_text.lower())

check("Targets Nippon India Target URL",
      "nippon-india" in ingest_text.lower())

check("Targets Quant Small Cap URL",
      "quant" in ingest_text.lower())

check("Targets HDFC Mid Cap URL",
      "hdfc" in ingest_text.lower())

check("Extracts NAV field",
      "nav" in ingest_text.lower())

check("Extracts min_sip field",
      "min_sip" in ingest_text.lower() or "sip" in ingest_text.lower())

check("Extracts fund_size_aum field",
      "fund_size_aum" in ingest_text.lower() or "aum" in ingest_text.lower())

check("Extracts expense_ratio field",
      "expense_ratio" in ingest_text.lower())

check("Extracts exit_load field",
      "exit_load" in ingest_text.lower())

check("Outputs to data/raw/targeted_schemes.json",
      "targeted_schemes" in ingest_text.lower())

# ─────────────────────────────────────────────────────────────
# PHASE 13 — index.py structure
# ─────────────────────────────────────────────────────────────
print("\n🔢  PHASE 13 — index.py (Embedding Pipeline) Validation")

index_path = ROOT / "scripts/index.py"
index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

# Syntax check
try:
    ast.parse(index_text)
    check("index.py — valid Python syntax", True)
except SyntaxError as e:
    check("index.py — valid Python syntax", False, str(e))

check("Uses BGE-small embedding model",
      "bge-small-en-v1.5" in index_text)

check("Uses ChromaDB",
      "chromadb" in index_text.lower())

check("Uses CloudClient/HttpClient (Cloud Vector DB)",
      "httpclient" in index_text.lower() or "cloudclient" in index_text.lower())

check("Accesses Chroma Cloud SECRETS",
      "chroma_tenant" in index_text.lower() or "chroma_database" in index_text.lower() or "chroma_api_key" in index_text.lower())

check("Reads targeted_schemes.json",
      "targeted_schemes.json" in index_text)

check("Chunks all 6 factual fields (FACTUAL_FIELDS dict or similar)",
      "nav" in index_text and "min_sip" in index_text and "expense_ratio" in index_text
      and "exit_load" in index_text and "fund_size_aum" in index_text)

check("Creates distinct ChromaDB collections per AMC",
      "get_or_create_collection" in index_text)

check("Batch upsert (BATCH_SIZE defined)",
      "BATCH_SIZE" in index_text or "batch_size" in index_text.lower())

check("Deterministic chunk ID (build_chunk_id or similar)",
      "chunk_id" in index_text.lower() or "build_chunk_id" in index_text)

check("Removed PDF chunking logic",
      "recursivecharactertextsplitter" not in index_text.lower())

check("384 embedding dimensions configured",
      "384" in index_text)

# ─────────────────────────────────────────────────────────────
# PHASE 14 — Targeted Scheme JSON Schema Validation
# ─────────────────────────────────────────────────────────────
print("\n📄  PHASE 14 — Targeted Scheme JSON Schema Validation")

REQUIRED_SCHEMA_FIELDS = {"scheme_name", "source_url", "last_updated", "nav", "min_sip",
                          "fund_size_aum", "expense_ratio", "exit_load", "rating"}

target_json = ROOT / "data/raw/targeted_schemes.json"

if not target_json.exists():
    check("targeted_schemes.json — file exists", False)
else:
    check("targeted_schemes.json — file exists", True)
    try:
        data = json.loads(target_json.read_text(encoding="utf-8"))
        check("targeted_schemes.json — valid JSON", True)

        check("targeted_schemes.json — is an array", isinstance(data, list))
        check("targeted_schemes.json — contains exactly 5 schemes", len(data) == 5, f"Found {len(data)}")

        if data:
            first = data[0]
            missing = REQUIRED_SCHEMA_FIELDS - set(first.keys())
            check("targeted_schemes.json — scheme[0] has all required fields",
                  len(missing) == 0,
                  f"Missing: {missing}" if missing else "")

    except json.JSONDecodeError as e:
        check("targeted_schemes.json — valid JSON", False, str(e))

# ─────────────────────────────────────────────────────────────
# PHASE 11 — .gitignore
# ─────────────────────────────────────────────────────────────
print("\n🔒  PHASE 11 — .gitignore Validation")

gitignore_path = ROOT / ".gitignore"
gitignore_text = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""

check(".gitignore excludes __pycache__",    "__pycache__" in gitignore_text)
check(".gitignore excludes .env files",     ".env" in gitignore_text)
check(".gitignore excludes PDFs (*.pdf or data/raw/*)", ".pdf" in gitignore_text or "data/raw/" in gitignore_text)

# ─────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
passed = sum(1 for _, r, _ in results if r is True)
failed = sum(1 for _, r, _ in results if r is False)
warned = sum(1 for _, r, _ in results if r is None)
total  = passed + failed

print(f"  RESULTS: {passed}/{total} checks passed   |   {failed} failed   |   {warned} warnings")
print("=" * 65)

if failed > 0:
    print("\n🔴 FAILED CHECKS:")
    for name, r, detail in results:
        if r is False:
            print(f"   ❌  {name}")
            if detail:
                print(f"       → {detail}")

if failed == 0:
    print("\n🎉  All checks passed! Project matches architecture specification.")
    sys.exit(0)
else:
    sys.exit(1)
