from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any

from tools.jarvis_live_runtime.project_workspace_tools import (
    PROJECT_ROOT,
    _safe_project_path,
    _tracked_project_files,
    read_file_outline,
    read_file_snippet,
    repo_git_status,
)


_MAX_SCOPE_ITEMS = 4
_MAX_OUTPUT_LINES = 80
_MAX_RELATED_FILES = 4
_PYTEST_TIMEOUT_SECONDS = 45
_GIT_TIMEOUT_SECONDS = 5
_FAIL_LINE_RE = re.compile(r"^FAILED\s+(?P<nodeid>\S+)")
_FILE_LINE_RE = re.compile(r"(?P<path>[A-Za-z0-9_./-]+\.py):(?P<line>\d+)")


def _run_bounded_process(
    command: tuple[str, ...],
    *,
    timeout_seconds: int,
    env_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    try:
        result = subprocess.run(
            list(command),
            cwd=str(PROJECT_ROOT),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            env=env,
        )
        return {
            "command": command,
            "returncode": int(result.returncode),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
        }
    except OSError as exc:
        return {
            "command": command,
            "returncode": 127,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
        }


def _dedupe(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return tuple(ordered)


def _changed_paths_from_status(status: dict[str, Any]) -> tuple[str, ...]:
    return _dedupe(
        list(status.get("staged_files", ()))
        + list(status.get("dirty_files", ()))
        + list(status.get("untracked_files", ()))
        + list(status.get("diff_name_only", ()))
    )


def _test_candidates_for_source(path: str, tracked_files: tuple[str, ...]) -> tuple[str, ...]:
    stem = Path(path).stem.casefold()
    parent = Path(path).parent.name.casefold()
    matches = [
        candidate
        for candidate in tracked_files
        if candidate.startswith("tests/")
        and candidate.endswith(".py")
        and (
            stem in Path(candidate).stem.casefold()
            or parent in candidate.casefold()
        )
    ]
    return _dedupe(matches)


def _safe_pytest_scope(user_text: str, status: dict[str, Any]) -> dict[str, Any]:
    tracked_files = _tracked_project_files()
    changed_paths = _changed_paths_from_status(status)
    direct_tests = tuple(
        path for path in changed_paths if path.startswith("tests/") and path.endswith(".py")
    )
    if direct_tests:
        selected = direct_tests[:_MAX_SCOPE_ITEMS]
        return {
            "selected_scope": selected,
            "selection_reason": "changed test files from git status",
            "changed_paths": changed_paths,
        }

    candidate_tests: list[str] = []
    for path in changed_paths:
        if not path.endswith(".py") or path.startswith("tests/"):
            continue
        candidate_tests.extend(_test_candidates_for_source(path, tracked_files))
    selected = _dedupe(candidate_tests)[:_MAX_SCOPE_ITEMS]
    if selected:
        return {
            "selected_scope": selected,
            "selection_reason": "nearest tests mapped from changed python files",
            "changed_paths": changed_paths,
        }

    lowered = user_text.casefold()
    query_tokens = tuple(
        token
        for token in re.findall(r"[a-z0-9_]+|[а-яё0-9_]+", lowered)
        if len(token) >= 4
    )
    semantic_candidates = tuple(
        path
        for path in tracked_files
        if path.startswith("tests/")
        and path.endswith(".py")
        and any(token in path.casefold() for token in query_tokens)
    )
    if semantic_candidates:
        return {
            "selected_scope": semantic_candidates[:_MAX_SCOPE_ITEMS],
            "selection_reason": "nearest tests matched from user request tokens",
            "changed_paths": changed_paths,
        }

    fallback = tuple(
        path
        for path in tracked_files
        if path
        in (
            "tests/jarvis_live_runtime/test_read_only_tool_router_boundary_smoke.py",
            "tests/jarvis_live_runtime/test_jarvis_live_project_answer_engine_boundary_smoke.py",
        )
    )
    return {
        "selected_scope": fallback[:_MAX_SCOPE_ITEMS],
        "selection_reason": "bounded fallback smoke scope for WSL diagnostics",
        "changed_paths": changed_paths,
    }


def _pytest_env() -> dict[str, str]:
    return {
        "TMPDIR": "/dev/shm",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTEST_ADDOPTS": "-p no:cacheprovider",
        "PYTHONPATH": ".",
    }


def _parse_failure_nodeids(output: str) -> tuple[str, ...]:
    nodeids: list[str] = []
    for line in output.splitlines():
        match = _FAIL_LINE_RE.match(line.strip())
        if match:
            nodeids.append(match.group("nodeid"))
    return _dedupe(nodeids)


def _related_file_refs(output: str) -> tuple[dict[str, Any], ...]:
    refs: list[dict[str, Any]] = []
    for match in _FILE_LINE_RE.finditer(output):
        path = match.group("path")
        if not _safe_project_path(path):
            continue
        refs.append({"path": path, "line": int(match.group("line"))})
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for ref in refs:
        key = (str(ref["path"]), int(ref["line"]))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ref)
    return tuple(deduped[:12])


def _error_excerpt(stdout: str, stderr: str) -> tuple[str, ...]:
    lines: list[str] = []
    for source in (stdout, stderr):
        for line in source.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("E   ") or "AssertionError" in stripped or "TypeError" in stripped or "ValueError" in stripped:
                lines.append(stripped)
    return _dedupe(lines)[:8]


def _snippets_for_related_files(
    file_refs: tuple[dict[str, Any], ...],
    changed_paths: tuple[str, ...],
    selected_scope: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    selected_paths = _dedupe(
        [str(ref["path"]) for ref in file_refs]
        + list(changed_paths)
        + [scope.split("::", 1)[0] for scope in selected_scope]
    )[:_MAX_RELATED_FILES]
    snippets: list[dict[str, Any]] = []
    for path in selected_paths:
        line_hint = next((int(ref["line"]) for ref in file_refs if str(ref["path"]) == path), 1)
        start_line = max(1, line_hint - 3)
        end_line = line_hint + 6
        snippet = read_file_snippet(path, start_line=start_line, end_line=end_line)
        outline = read_file_outline(path)
        snippets.append(
            {
                "path": path,
                "line_hint": line_hint,
                "snippet": tuple(snippet.get("snippet", ())) if isinstance(snippet, dict) else (),
                "functions": tuple(outline.get("functions", ())) if isinstance(outline, dict) else (),
                "classes": tuple(outline.get("classes", ())) if isinstance(outline, dict) else (),
                "imports": tuple(outline.get("imports", ())) if isinstance(outline, dict) else (),
            }
        )
    return tuple(snippets)


def _truncate_output(text: str) -> str:
    lines = text.splitlines()
    if len(lines) <= _MAX_OUTPUT_LINES:
        return text.strip()
    clipped = "\n".join(lines[:_MAX_OUTPUT_LINES])
    return clipped.strip() + "\n[output_truncated=true reason=bounded_wsl_operator_output]"


def build_wsl_project_diagnostics_read_model(user_text: str) -> dict[str, Any]:
    git_probe = _run_bounded_process(("git", "status", "-sb"), timeout_seconds=_GIT_TIMEOUT_SECONDS)
    status = repo_git_status()
    scope = _safe_pytest_scope(user_text, status)
    selected_scope = tuple(scope["selected_scope"])
    if selected_scope:
        pytest_command = ("python", "-m", "pytest", *selected_scope, "-q", "--tb=short", "--maxfail=8")
        pytest_probe = _run_bounded_process(
            pytest_command,
            timeout_seconds=_PYTEST_TIMEOUT_SECONDS,
            env_overrides=_pytest_env(),
        )
    else:
        pytest_probe = {
            "command": (),
            "returncode": 0,
            "stdout": "",
            "stderr": "no bounded pytest scope inferred",
            "timed_out": False,
        }
    combined_output = "\n".join(part for part in (pytest_probe["stdout"], pytest_probe["stderr"]) if part).strip()
    failing_tests = _parse_failure_nodeids(combined_output)
    file_refs = _related_file_refs(combined_output)
    error_excerpt = _error_excerpt(pytest_probe["stdout"], pytest_probe["stderr"])
    snippets = _snippets_for_related_files(file_refs, tuple(scope["changed_paths"]), selected_scope)

    diagnosis: list[str] = []
    if not selected_scope:
        diagnosis.append("no bounded pytest scope was inferred, so pytest was not executed")
    elif pytest_probe["timed_out"]:
        diagnosis.append("bounded pytest probe timed out before completion")
    elif pytest_probe["returncode"] == 0:
        diagnosis.append("bounded pytest scope passed; no failing tests detected in the selected scope")
    elif failing_tests:
        diagnosis.append("failing tests were detected in the bounded pytest scope")
    else:
        diagnosis.append("pytest returned non-zero but no FAILED nodeids were parsed; inspect stderr/stdout excerpts")
    if error_excerpt:
        diagnosis.append(f"first_error={error_excerpt[0]}")
    if file_refs:
        diagnosis.append(
            "related_file_refs=" + ", ".join(f"{ref['path']}:{ref['line']}" for ref in file_refs[:4])
        )

    fix_plan: list[str] = []
    if snippets:
        primary = snippets[0]
        fix_plan.append(f"inspect and align behavior around {primary['path']} near line {primary['line_hint']}")
    if failing_tests:
        fix_plan.append("adjust implementation or expectation to satisfy the failing assertions without widening scope")
    fix_plan.append("rerun the same bounded pytest scope after the patch proposal")
    fix_plan.append("only expand to a wider suite after the bounded scope is green")

    return {
        "intent_family": "WSL_PROJECT_DIAGNOSTICS",
        "read_only": True,
        "execution_allowed": False,
        "proposal_only": True,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "install_allowed": False,
        "download_allowed": False,
        "pc_control_allowed": False,
        "git_probe": git_probe,
        "git_status": status,
        "selected_scope": selected_scope,
        "selection_reason": str(scope["selection_reason"]),
        "pytest_probe": pytest_probe,
        "failing_tests": failing_tests,
        "related_file_refs": file_refs,
        "related_snippets": snippets,
        "error_excerpt": error_excerpt,
        "diagnosis": tuple(diagnosis),
        "fix_plan": tuple(fix_plan),
        "git_status_stdout": _truncate_output(str(git_probe["stdout"])),
        "pytest_stdout": _truncate_output(str(pytest_probe["stdout"])),
        "pytest_stderr": _truncate_output(str(pytest_probe["stderr"])),
    }
