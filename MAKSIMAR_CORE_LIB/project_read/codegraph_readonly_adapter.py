from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CODEGRAPH_OUT_ROOT = PROJECT_ROOT / "codegraph-out"
CODEGRAPH_GRAPH_JSON = CODEGRAPH_OUT_ROOT / "graph.json"
CODEGRAPH_GRAPH_REPORT = CODEGRAPH_OUT_ROOT / "GRAPH_REPORT.md"
CODEGRAPH_WIKI_INDEX = CODEGRAPH_OUT_ROOT / "wiki" / "index.md"
CODEGRAPH_EXECUTABLE = PROJECT_ROOT / ".venv" / "bin" / "codegraph"

def inspect_codegraph_readonly_capability() -> dict[str, Any]:
    graph_available = CODEGRAPH_GRAPH_JSON.exists()
    report_available = CODEGRAPH_GRAPH_REPORT.exists()
    wiki_available = CODEGRAPH_WIKI_INDEX.exists()
    executable_available = CODEGRAPH_EXECUTABLE.exists()
    package_installed = importlib.util.find_spec("codegraph") is not None
    if graph_available or report_available:
        status = "available"
        reason = "existing_codegraph_artifacts_detected"
    elif executable_available or package_installed:
        status = "degraded"
        reason = "codegraph_installed_but_graph_not_built"
    else:
        status = "degraded"
        reason = "codegraph_runtime_not_detected"
    return {
        "capability_id": "project_codegraph_readonly",
        "graph_available": graph_available,
        "report_available": report_available,
        "wiki_available": wiki_available,
        "package_installed": package_installed,
        "executable_available": executable_available,
        "status": status,
        "reason": reason,
        "graph_json_path": str(CODEGRAPH_GRAPH_JSON),
        "graph_report_path": str(CODEGRAPH_GRAPH_REPORT),
        "wiki_index_path": str(CODEGRAPH_WIKI_INDEX),
        "codegraph_executable": str(CODEGRAPH_EXECUTABLE),
        "direct_allowed": True,
        "approval_required": False,
        "write_allowed": False,
        "rebuild_allowed": False,
    }


def build_codegraph_readonly_response(
    query: str,
    *,
    timeout_seconds: float = 5.0,
    output_budget: int = 3000,
) -> dict[str, Any]:
    status = inspect_codegraph_readonly_capability()
    source_files: list[str] = []
    if status["report_available"]:
        source_files.append(str(CODEGRAPH_GRAPH_REPORT))
    if status["wiki_available"]:
        source_files.append(str(CODEGRAPH_WIKI_INDEX))
    if status["graph_available"]:
        source_files.append(str(CODEGRAPH_GRAPH_JSON))

    if not status["graph_available"]:
        response_text = "Codegraph is installed but graph.json is not built yet."
        if status["report_available"]:
            response_text += " GRAPH_REPORT.md is available for read-only summary."
        return {
            **status,
            "query": query,
            "response_text": response_text,
            "source_files": tuple(source_files),
            "selected_nodes": (),
            "error_kind": "",
            "cli_used": False,
        }

    cli_payload = _run_codegraph_cli_query(query, timeout_seconds=timeout_seconds, output_budget=output_budget)
    if cli_payload["response_text"]:
        return {
            **status,
            "query": query,
            "response_text": cli_payload["response_text"],
            "source_files": tuple(dict.fromkeys(source_files + list(cli_payload["source_files"]))),
            "selected_nodes": tuple(cli_payload["selected_nodes"]),
            "error_kind": cli_payload["error_kind"],
            "cli_used": cli_payload["cli_used"],
        }

    report_text = _read_best_report(output_budget=output_budget)
    if report_text:
        excerpt, selected_nodes = _extract_report_excerpt(report_text, query, output_budget=output_budget)
        return {
            **status,
            "query": query,
            "response_text": excerpt,
            "source_files": tuple(source_files),
            "selected_nodes": tuple(selected_nodes),
            "error_kind": "",
            "cli_used": False,
        }

    return {
        **status,
        "query": query,
        "response_text": "Codegraph graph.json exists, but no readable report/query result was produced in read-only mode.",
        "source_files": tuple(source_files),
        "selected_nodes": (),
        "error_kind": "empty_codegraph_readonly_result",
        "cli_used": False,
    }


def _run_codegraph_cli_query(
    query: str,
    *,
    timeout_seconds: float,
    output_budget: int,
) -> dict[str, Any]:
    executable = _resolve_codegraph_executable()
    if executable is None:
        return {
            "response_text": "",
            "source_files": (),
            "selected_nodes": (),
            "error_kind": "",
            "cli_used": False,
        }
    command = (
        str(executable),
        "query",
        query,
    )
    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except (OSError, subprocess.TimeoutExpired):
        return {
            "response_text": "",
            "source_files": (),
            "selected_nodes": (),
            "error_kind": "codegraph_query_unavailable",
            "cli_used": True,
        }
    stdout = str(completed.stdout or "").strip()
    if completed.returncode != 0 or not stdout:
        return {
            "response_text": "",
            "source_files": (),
            "selected_nodes": (),
            "error_kind": "codegraph_query_unavailable",
            "cli_used": True,
        }
    trimmed = stdout[:output_budget].strip()
    return {
        "response_text": trimmed,
        "source_files": (str(CODEGRAPH_GRAPH_JSON),),
        "selected_nodes": _extract_selected_nodes(trimmed),
        "error_kind": "",
        "cli_used": True,
    }


def _resolve_codegraph_executable() -> Path | None:
    if CODEGRAPH_EXECUTABLE.exists():
        return CODEGRAPH_EXECUTABLE
    return None


def _read_best_report(*, output_budget: int) -> str:
    for path in (CODEGRAPH_WIKI_INDEX, CODEGRAPH_GRAPH_REPORT):
        if not path.exists():
            continue
        try:
            return path.read_text(encoding="utf-8", errors="replace")[:output_budget * 2]
        except OSError:
            continue
    return ""


def _extract_report_excerpt(report_text: str, query: str, *, output_budget: int) -> tuple[str, tuple[str, ...]]:
    lowered_query = str(query or "").casefold()
    lines = [line.strip() for line in report_text.splitlines() if line.strip()]
    matched = [
        line
        for line in lines
        if any(token and token in line.casefold() for token in _query_tokens(lowered_query))
    ]
    excerpt_lines = matched[:8] if matched else lines[:8]
    excerpt = "\n".join(excerpt_lines)[:output_budget].strip()
    if not excerpt:
        excerpt = "Codegraph report is available, but no non-empty excerpt was produced."
    return excerpt, _extract_selected_nodes(excerpt)


def _extract_selected_nodes(text: str) -> tuple[str, ...]:
    nodes: list[str] = []
    for line in str(text or "").splitlines():
        cleaned = line.strip(" -:*")
        if not cleaned:
            continue
        if "/" in cleaned or "." in cleaned:
            nodes.append(cleaned[:180])
        if len(nodes) >= 8:
            break
    return tuple(dict.fromkeys(nodes))


def _query_tokens(text: str) -> tuple[str, ...]:
    tokens = []
    for part in str(text or "").replace("?", " ").replace(",", " ").split():
        normalized = part.strip().casefold()
        if len(normalized) >= 4:
            tokens.append(normalized)
    return tuple(tokens)
