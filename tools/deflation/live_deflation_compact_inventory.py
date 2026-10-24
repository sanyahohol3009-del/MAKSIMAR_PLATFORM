from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import json

ROOT = Path(".")
OUT_DIR = Path("RUNTIME/audits/live_deflation")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SKIP_DIRS = {
    ".git", ".venv", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "__pycache__", ".runtime",
}

LIVE_PATTERNS = re.compile(
    r"voice|jarvis_live|live|control_plane|runtime|tts|stt|ollama|screen|pc_control|approval|sandbox|smoke|probe|read_model",
    re.I,
)

HARD_BLOCK_PATTERNS = re.compile(
    r"pc_control_allowed\s*[:=]\s*False|pc_control_allowed=false|"
    r"approval_required\s*[:=]\s*True|operator_approval_required|"
    r"must remain false|requires approval|approval-only|proposal-only|"
    r"direct_execution_allowed\s*[:=]\s*False|direct_ollama_allowed\s*[:=]\s*False",
    re.I,
)

def iter_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in {".py", ".md", ".json", ".txt", ".yaml", ".yml"}:
            continue
        yield p

files = list(iter_files())
live_files = [p for p in files if LIVE_PATTERNS.search(str(p))]

hard_hits = []
for p in live_files:
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    matches = []
    for i, line in enumerate(text.splitlines(), 1):
        if HARD_BLOCK_PATTERNS.search(line):
            matches.append({"line": i, "text": line.strip()[:220]})
    if matches:
        hard_hits.append({
            "path": str(p),
            "hit_count": len(matches),
            "sample": matches[:8],
        })

by_dir = Counter(str(p.parts[0]) for p in live_files if p.parts)
by_suffix = Counter(p.suffix for p in live_files)

delete_candidate_keywords = re.compile(r"smoke|probe|debug|preview|terminal_preview|web_preview|status|read_model", re.I)
delete_candidates = [
    str(p) for p in live_files
    if delete_candidate_keywords.search(str(p))
]

keep_core_keywords = re.compile(
    r"CONTROL_PLANE/api_server.py|"
    r"tools/jarvis_live_runtime/jarvis_live_brain_loop.py|"
    r"tools/jarvis_live_runtime/ollama_|"
    r"MAKSIMAR_SERVER/AI_ORCHESTRATION/project_workspace_tools.py|"
    r"MAKSIMAR_SERVER/AI_ORCHESTRATION/session_memory_store.py|"
    r"MAKSIMAR_CORE_LIB/ai_orchestration/model_profile_registry_contract.py",
    re.I,
)
keep_core = [str(p) for p in live_files if keep_core_keywords.search(str(p))]

report = {
    "summary": {
        "all_text_files_scanned": len(files),
        "live_related_files": len(live_files),
        "hard_block_files": len(hard_hits),
        "delete_or_quarantine_candidate_count": len(delete_candidates),
        "keep_core_candidate_count": len(keep_core),
    },
    "by_top_dir": dict(by_dir.most_common()),
    "by_suffix": dict(by_suffix.most_common()),
    "keep_core_candidates": keep_core[:120],
    "delete_or_quarantine_candidates": delete_candidates[:300],
    "hard_block_files_top": sorted(hard_hits, key=lambda x: x["hit_count"], reverse=True)[:120],
}

json_path = OUT_DIR / "live_deflation_compact_inventory_001.json"
md_path = OUT_DIR / "live_deflation_compact_inventory_001.md"

json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

lines = []
lines.append("# LIVE DEFLATION COMPACT INVENTORY 001")
lines.append("")
for k, v in report["summary"].items():
    lines.append(f"- {k}: {v}")

lines.append("\n## Top directories")
for k, v in report["by_top_dir"].items():
    lines.append(f"- {k}: {v}")

lines.append("\n## KEEP CORE candidates")
for p in report["keep_core_candidates"]:
    lines.append(f"- {p}")

lines.append("\n## QUARANTINE/DELETE candidates")
for p in report["delete_or_quarantine_candidates"][:180]:
    lines.append(f"- {p}")

lines.append("\n## Hard-block files")
for item in report["hard_block_files_top"]:
    lines.append(f"\n### {item['path']} ({item['hit_count']} hits)")
    for hit in item["sample"]:
        lines.append(f"- L{hit['line']}: `{hit['text']}`")

md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(md_path)
print(json_path)
print("summary=", report["summary"])
