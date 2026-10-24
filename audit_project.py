#!/usr/bin/env python3
"""
MAKSIMAR_PLATFORM Project Audit Tool
======================================
Scans a Python codebase for:
  1. Duplicate definitions (classes/functions/config keys defined in multiple places)
     -> your "parallel realities" / duplicate voice-contract problem
  2. Dead / unreachable code (via vulture, if installed)
  3. A module-level dependency graph (via pydeps, if installed) rendered to SVG

Usage:
    python3 audit_project.py /path/to/your/repo

Output:
    ./audit_report/duplicates.md
    ./audit_report/dead_code.txt
    ./audit_report/dependency_graph.svg
    ./audit_report/SUMMARY.md
"""

import ast
import sys
import os
import subprocess
import collections
from pathlib import Path

def find_python_files(root: Path):
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "node_modules", "build", "dist"}
    # substrings anywhere in the path that mark it as archive/backup/vendored
    # code rather than live first-party source. These inflate duplicate counts
    # with frozen snapshots and third-party libraries.
    skip_path_substrings = (
        "deleted_live_track_archive",
        "manual_patch_backups",
        "_backup",
        "vendor_quarantine",
    )
    for p in root.rglob("*.py"):
        if any(part in skip_dirs for part in p.parts):
            continue
        path_str = str(p)
        if any(s in path_str for s in skip_path_substrings):
            continue
        yield p

def collect_definitions(files):
    """
    Walk every file's AST and record every top-level and class-level
    function/class definition, plus any module-level constant assignment
    (useful for catching duplicate config keys / flags like
    'owner_command_detected' defined differently in multiple files).
    """
    defs = collections.defaultdict(list)  # name -> list of (file, lineno, kind)

    for f in files:
        try:
            src = f.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(src, filename=str(f))
        except SyntaxError as e:
            defs["__SYNTAX_ERROR__"].append((str(f), e.lineno or 0, "syntax_error"))
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defs[node.name].append((str(f), node.lineno, "function"))
            elif isinstance(node, ast.ClassDef):
                defs[node.name].append((str(f), node.lineno, "class"))
            elif isinstance(node, ast.Assign):
                # only care about simple top-level constants, e.g. FLAG = True
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        defs[target.id].append((str(f), node.lineno, "constant"))

    return defs

def report_duplicates(defs, out_path: Path):
    lines = ["# Duplicate Definitions Report\n",
             "Names defined in more than one file. Review each — some duplicates",
             "are fine (e.g. common helper names), but repeated contracts, config",
             "flags, or class names across files are exactly the 'parallel reality'",
             "pattern to hunt down.\n"]

    syntax_errors = defs.pop("__SYNTAX_ERROR__", [])
    real_dupes = {name: locs for name, locs in defs.items() if len(locs) > 1}

    if not real_dupes:
        lines.append("No duplicate top-level names found.\n")
    else:
        # sort by number of duplicates descending — worst offenders first
        for name, locs in sorted(real_dupes.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"## `{name}`  ({len(locs)} definitions)")
            for file, lineno, kind in locs:
                lines.append(f"- {kind}: `{file}:{lineno}`")
            lines.append("")

    if syntax_errors:
        lines.append("## Files with syntax errors (skipped)\n")
        for file, lineno, _ in syntax_errors:
            lines.append(f"- `{file}:{lineno}`")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return len(real_dupes), len(syntax_errors)

def run_vulture(root: Path, out_path: Path):
    try:
        result = subprocess.run(
            ["vulture", str(root), "--min-confidence", "70"],
            capture_output=True, text=True, timeout=300
        )
        output = result.stdout or "(no dead code found, or vulture produced no output)"
        out_path.write_text(output, encoding="utf-8")
        return True
    except FileNotFoundError:
        out_path.write_text(
            "vulture not installed. Install with:\n  pip install vulture --break-system-packages",
            encoding="utf-8"
        )
        return False
    except subprocess.TimeoutExpired:
        out_path.write_text("vulture timed out after 300s on this codebase.", encoding="utf-8")
        return False

def run_pydeps(root: Path, out_svg: Path):
    """
    pydeps needs the project to be importable, so this may fail on
    partially-broken codebases. That's expected — it's informative on its own.
    """
    try:
        result = subprocess.run(
            ["pydeps", str(root), "--max-bacon", "2", "--noshow",
             "-o", str(out_svg)],
            capture_output=True, text=True, timeout=300
        )
        if out_svg.exists():
            return True, ""
        return False, result.stderr[-2000:] if result.stderr else "unknown pydeps failure"
    except FileNotFoundError:
        return False, "pydeps not installed. Install with:\n  pip install pydeps --break-system-packages"
    except subprocess.TimeoutExpired:
        return False, "pydeps timed out after 300s."

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 audit_project.py /path/to/repo")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        print(f"Path does not exist: {root}")
        sys.exit(1)

    out_dir = Path.cwd() / "audit_report"
    out_dir.mkdir(exist_ok=True)

    print(f"Scanning {root} ...")
    files = list(find_python_files(root))
    print(f"Found {len(files)} Python files.")

    print("Checking for duplicate definitions...")
    defs = collect_definitions(files)
    dupe_count, syntax_err_count = report_duplicates(defs, out_dir / "duplicates.md")

    print("Running vulture (dead code detection)...")
    vulture_ok = run_vulture(root, out_dir / "dead_code.txt")

    print("Running pydeps (dependency graph)...")
    pydeps_ok, pydeps_err = run_pydeps(root, out_dir / "dependency_graph.svg")

    summary = [
        "# Audit Summary\n",
        f"Files scanned: {len(files)}",
        f"Files with syntax errors: {syntax_err_count}",
        f"Duplicate names found: {dupe_count} (see duplicates.md)",
        f"Dead code scan: {'completed' if vulture_ok else 'FAILED - see dead_code.txt'}",
        f"Dependency graph: {'generated at dependency_graph.svg' if pydeps_ok else 'FAILED'}",
    ]
    if not pydeps_ok:
        summary.append(f"\npydeps error detail:\n{pydeps_err}")

    (out_dir / "SUMMARY.md").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))
    print(f"\nFull reports written to: {out_dir}")

if __name__ == "__main__":
    main()
