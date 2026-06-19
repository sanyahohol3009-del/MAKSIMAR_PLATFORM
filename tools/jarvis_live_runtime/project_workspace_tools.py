from __future__ import annotations

import ast
import shutil
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MAX_PROJECT_TREE_ENTRIES = 80
MAX_PROJECT_FILE_SNIPPETS = 6
MAX_PROJECT_FILE_BYTES = 1800
PROJECT_FILES_PAGE_SIZE = 80
PROJECT_TREE_MAX_ENTRIES = 300
PROJECT_FILE_PAGE_LINES = 120
PROJECT_FILE_MAX_BYTES = 12000
PROJECT_SEARCH_MAX_RESULTS = 40
PROJECT_IMPORT_MAX_EDGES = 80

PROJECT_VISIBILITY_EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

PROJECT_VISIBILITY_KEY_FILES = (
    "CONTROL_PLANE/api_server.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py",
    "tools/jarvis_live_runtime/jarvis_live_chat_launcher.py",
    "tools/jarvis_live_runtime/jarvis_live_terminal_chat.py",
    "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
    "tools/jarvis_live_runtime/jarvis_personality_policy.py",
    "tools/jarvis_live_runtime/jarvis_live_response_mode.py",
    "tools/project_readiness_control/jarvis_live_ci_status.py",
    "tools/roadmap_post_step_drift_check.py",
)


def _run_read_only_command(command: tuple[str, ...]) -> str:
    try:
        result = subprocess.run(
            list(command),
            cwd=str(PROJECT_ROOT),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _parse_int(value: Any, default: int) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def _query_tokens(text: str) -> tuple[str, ...]:
    return tuple(part for part in text.casefold().replace("?", " ").replace(",", " ").split() if len(part) >= 4)


def repo_git_status() -> dict[str, Any]:
    status_short = _run_read_only_command(("git", "status", "--short"))
    parsed = _parse_git_status_short(status_short)
    return {
        "branch": _run_read_only_command(("git", "branch", "--show-current")),
        "head": _run_read_only_command(("git", "rev-parse", "HEAD")),
        "status_short": status_short,
        "dirty_files": parsed["dirty_files"],
        "untracked_files": parsed["untracked_files"],
        "staged_files": parsed["staged_files"],
        "diff_name_only": tuple(_run_read_only_command(("git", "diff", "--name-only")).splitlines()),
        "diff_stat": _run_read_only_command(("git", "diff", "--stat")),
        "read_only": True,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "pc_control_allowed": False,
    }


def repo_tree(depth: int = 2, max_entries: int = PROJECT_TREE_MAX_ENTRIES) -> dict[str, Any]:
    depth = max(1, min(int(depth), 5))
    max_entries = max(1, min(int(max_entries), PROJECT_TREE_MAX_ENTRIES))
    entries: list[str] = []
    for path in _tracked_project_files():
        if _is_excluded_project_path(path):
            continue
        parts = Path(path).parts[:depth]
        if not parts:
            continue
        value = "/".join(parts) + ("/" if len(Path(path).parts) > len(parts) else "")
        if value not in entries:
            entries.append(value)
        if len(entries) >= max_entries:
            break
    return {"depth": depth, "entries": tuple(entries), "entry_count": len(entries), "read_only": True}


def repo_files(page: int = 1, page_size: int = PROJECT_FILES_PAGE_SIZE) -> dict[str, Any]:
    files = _tracked_project_files()
    page = max(1, int(page))
    page_size = max(1, min(int(page_size), PROJECT_FILES_PAGE_SIZE))
    start = (page - 1) * page_size
    end = start + page_size
    total_pages = (len(files) + page_size - 1) // page_size if files else 1
    return {
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_files": len(files),
        "files": files[start:end],
        "read_only": True,
    }


def repo_search(query: str, paths: tuple[str, ...] | None = None, max_results: int = PROJECT_SEARCH_MAX_RESULTS) -> dict[str, Any]:
    query = query.strip()
    if not query:
        return {"query": query, "results": (), "result_count": 0, "read_only": True}
    max_results = max(1, min(int(max_results), PROJECT_SEARCH_MAX_RESULTS))
    search_paths = tuple(path for path in (paths or ()) if _safe_project_path(path))
    results = _repo_search_with_rg(query, search_paths, max_results)
    if not results:
        results = _repo_search_with_python(query, search_paths, max_results)
    return {"query": query, "results": tuple(results[:max_results]), "result_count": len(results[:max_results]), "read_only": True}


def read_file_snippet(path: str, start_line: int = 1, end_line: int | None = None, page: int = 1) -> dict[str, Any]:
    if not _safe_project_path(path) or not _is_safe_project_text_path(path):
        return {"path": path, "allowed": False, "error": "path_denied", "read_only": True}
    full_path = PROJECT_ROOT / path
    if not full_path.exists() or not full_path.is_file():
        return {"path": path, "allowed": False, "error": "file_not_found", "read_only": True}
    page = max(1, int(page))
    if end_line is None:
        start_line = ((page - 1) * PROJECT_FILE_PAGE_LINES) + 1
        end_line = start_line + PROJECT_FILE_PAGE_LINES - 1
    start_line = max(1, int(start_line))
    end_line = max(start_line, min(int(end_line), start_line + PROJECT_FILE_PAGE_LINES - 1))
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")[:PROJECT_FILE_MAX_BYTES * max(1, page)]
    except OSError:
        return {"path": path, "allowed": False, "error": "read_failed", "read_only": True}
    lines = text.splitlines()
    selected = lines[start_line - 1:end_line]
    numbered = tuple(f"{idx}: {line}" for idx, line in enumerate(selected, start=start_line))
    return {
        "path": path,
        "allowed": True,
        "page": page,
        "start_line": start_line,
        "end_line": min(end_line, len(lines)),
        "line_count": len(lines),
        "snippet": numbered,
        "read_only": True,
    }


def read_file_outline(path: str) -> dict[str, Any]:
    snippet = read_file_snippet(path, start_line=1, end_line=PROJECT_FILE_PAGE_LINES, page=1)
    if not snippet.get("allowed"):
        return snippet
    full_path = PROJECT_ROOT / path
    try:
        text = full_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {"path": path, "allowed": False, "error": "read_failed", "read_only": True}
    imports: list[str] = []
    classes: list[str] = []
    functions: list[str] = []
    constants: list[str] = []
    if full_path.suffix == ".py":
        try:
            tree = ast.parse(text)
        except SyntaxError:
            tree = None
        if tree is not None:
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(("." * node.level) + str(node.module or ""))
                elif isinstance(node, ast.ClassDef):
                    classes.append(f"{node.name}:{node.lineno}")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append(f"{node.name}:{node.lineno}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constants.append(f"{target.id}:{node.lineno}")
    return {
        "path": path,
        "allowed": True,
        "line_count": len(text.splitlines()),
        "imports": tuple(imports[:40]),
        "classes": tuple(classes[:40]),
        "functions": tuple(functions[:80]),
        "constants": tuple(constants[:40]),
        "read_only": True,
    }


def repo_import_graph(path: str | None = None, max_edges: int = PROJECT_IMPORT_MAX_EDGES) -> dict[str, Any]:
    max_edges = max(1, min(int(max_edges), PROJECT_IMPORT_MAX_EDGES))
    files = (path,) if path else tuple(file for file in _tracked_project_files() if file.endswith(".py"))
    edges: list[dict[str, str]] = []
    for file_path in files:
        outline = read_file_outline(file_path)
        if not outline.get("allowed"):
            continue
        for imported in outline.get("imports", ())[:20]:
            edges.append({"from": file_path, "to": str(imported)})
            if len(edges) >= max_edges:
                return {"edges": tuple(edges), "edge_count": len(edges), "read_only": True}
    return {"edges": tuple(edges), "edge_count": len(edges), "read_only": True}


def _parse_git_status_short(status_short: str) -> dict[str, tuple[str, ...]]:
    dirty: list[str] = []
    untracked: list[str] = []
    staged: list[str] = []
    for line in status_short.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:].strip() if len(line) > 3 else line.strip()
        if code == "??":
            untracked.append(path)
            continue
        if code[0].strip():
            staged.append(path)
        if code[1].strip():
            dirty.append(path)
    return {"dirty_files": tuple(dirty), "untracked_files": tuple(untracked), "staged_files": tuple(staged)}


def _important_paths_detected(paths: tuple[str, ...]) -> tuple[str, ...]:
    markers = (
        "CONTROL_PLANE/api_server.py",
        "jarvis_live_brain_loop.py",
        "jarvis_live_terminal_chat.py",
        "jarvis_live_chat_launcher.py",
        "jarvis_live_response_mode.py",
        "jarvis_personality_policy.py",
        "jarvis_live_ci_status.py",
        "roadmap_post_step_drift_check.py",
    )
    return tuple(path for path in paths if any(marker in path for marker in markers))[:80]


def _domain_groups_for_paths(paths: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    groups: dict[str, list[str]] = {
        "CONTROL_PLANE": [],
        "MAKSIMAR_CORE_LIB": [],
        "MAKSIMAR_SERVER": [],
        "AI_SERVICES": [],
        "tools": [],
        "tests": [],
        "runtime_history_store": [],
        "memory/history": [],
        "regulatory memory": [],
        "proposal/audit/approval": [],
        "security/safety/execution control": [],
        "core guard / watchdog / OOB / runtime truth": [],
        "JARVIS terminal runtime": [],
        "Ollama/model/Qwen/runtime model layer": [],
        "mobile/app/chat/sync": [],
        "dashboards/read-only views": [],
        "roadmap/check/CI tools": [],
        "external/vendor": [],
        "unknown/other": [],
    }
    for path in paths:
        lowered = path.casefold()
        matched = False
        for prefix in ("CONTROL_PLANE", "MAKSIMAR_CORE_LIB", "MAKSIMAR_SERVER", "AI_SERVICES", "tools", "tests", "runtime_history_store"):
            if path.startswith(prefix + "/") or path == prefix:
                groups[prefix].append(path)
                matched = True
        keyword_groups = (
            ("memory/history", ("memory", "history", "runtime_history")),
            ("regulatory memory", ("regulatory", "jurisdiction", "compliance")),
            ("proposal/audit/approval", ("proposal", "audit", "approval")),
            ("security/safety/execution control", ("security", "safety", "execution_control", "admission", "allowlist")),
            ("core guard / watchdog / OOB / runtime truth", ("core_guard", "watchdog", "oob", "runtime_truth", "truth")),
            ("JARVIS terminal runtime", ("jarvis_live_runtime", "terminal_chat", "brain_loop", "chat_launcher")),
            ("Ollama/model/Qwen/runtime model layer", ("ollama", "qwen", "model", "ai_orchestration")),
            ("mobile/app/chat/sync", ("mobile", "android", "ios", "chat", "sync")),
            ("dashboards/read-only views", ("dashboard", "read_only", "panel")),
            ("roadmap/check/CI tools", ("roadmap", "ci_status", "drift_check", "readiness")),
            ("external/vendor", ("external", "vendor", "mempalace")),
        )
        for group, markers in keyword_groups:
            if any(marker in lowered for marker in markers):
                groups[group].append(path)
                matched = True
        if not matched:
            groups["unknown/other"].append(path)
    return {key: tuple(value[:80]) for key, value in groups.items()}


def _repo_search_with_rg(query: str, paths: tuple[str, ...], max_results: int) -> list[dict[str, Any]]:
    if shutil.which("rg") is None:
        return []
    command = ["rg", "-n", "--no-heading", "--fixed-strings", "--max-count", "3", query]
    command.extend(paths or ["."])
    output = _run_read_only_command(tuple(command))
    results: list[dict[str, Any]] = []
    for line in output.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        path, line_number, matched = parts
        if not _safe_project_path(path):
            continue
        results.append({"path": path, "line_number": _parse_int(line_number, 0), "line": matched.strip()[:300]})
        if len(results) >= max_results:
            break
    return results


def _repo_search_with_python(query: str, paths: tuple[str, ...], max_results: int) -> list[dict[str, Any]]:
    lowered = query.casefold()
    candidates = paths or _tracked_project_files()
    results: list[dict[str, Any]] = []
    for path in candidates:
        if not _safe_project_path(path) or not _is_safe_project_text_path(path):
            continue
        full_path = PROJECT_ROOT / path
        try:
            lines = full_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            if lowered in line.casefold():
                results.append({"path": path, "line_number": line_number, "line": line.strip()[:300]})
                break
        if len(results) >= max_results:
            break
    return results


def _safe_project_path(path: str) -> bool:
    candidate = (PROJECT_ROOT / path).resolve()
    try:
        candidate.relative_to(PROJECT_ROOT)
    except ValueError:
        return False
    return not _is_excluded_project_path(str(candidate.relative_to(PROJECT_ROOT)))


def _project_tree_summary() -> str:
    tracked = _tracked_project_files()
    if tracked:
        top_entries = _top_level_entries_from_tracked_files(tracked)
        selected = tracked[:MAX_PROJECT_TREE_ENTRIES]
        return (
            "project_workspace_read_model: "
            f"project_root={PROJECT_ROOT}; "
            f"tracked_file_count={len(tracked)}; "
            f"top_level={', '.join(top_entries[:40])}; "
            f"sample_tracked_files={', '.join(selected[:30])}; "
            "read_only=true; direct_execution_allowed=false; canonical_write_allowed=false"
        )
    top_entries = [
        path.name + ("/" if path.is_dir() else "")
        for path in sorted(PROJECT_ROOT.iterdir(), key=lambda item: item.name.casefold())
        if path.name not in PROJECT_VISIBILITY_EXCLUDED_DIRS
    ][:40]
    return (
        "project_workspace_read_model: "
        f"project_root={PROJECT_ROOT}; tracked_file_count=unknown; "
        f"top_level={', '.join(top_entries)}; "
        "read_only=true; direct_execution_allowed=false; canonical_write_allowed=false"
    )


def _tracked_project_files() -> tuple[str, ...]:
    output = _run_read_only_command(("git", "ls-files"))
    if output:
        return tuple(
            line.strip()
            for line in output.splitlines()
            if line.strip() and not _is_excluded_project_path(line.strip())
        )
    paths: list[str] = []
    for path in PROJECT_ROOT.rglob("*"):
        if len(paths) >= 2000:
            break
        if path.is_dir() or _is_excluded_project_path(str(path.relative_to(PROJECT_ROOT))):
            continue
        paths.append(str(path.relative_to(PROJECT_ROOT)))
    return tuple(sorted(paths))


def _top_level_entries_from_tracked_files(paths: tuple[str, ...]) -> tuple[str, ...]:
    entries: list[str] = []
    seen: set[str] = set()
    for path in paths:
        first = path.split("/", 1)[0]
        if first in seen:
            continue
        seen.add(first)
        entries.append(first + ("/" if "/" in path else ""))
    return tuple(entries)


def _select_project_files_for_context(user_text: str, deep: bool) -> tuple[Path, ...]:
    tokens = _query_tokens(user_text)
    selected: list[str] = []
    tracked = _tracked_project_files()
    for key_file in PROJECT_VISIBILITY_KEY_FILES:
        if key_file in tracked or (PROJECT_ROOT / key_file).exists():
            selected.append(key_file)
    for path in tracked:
        if len(selected) >= (MAX_PROJECT_FILE_SNIPPETS * 3 if deep else MAX_PROJECT_FILE_SNIPPETS):
            break
        lowered = path.casefold()
        if tokens and not any(token in lowered for token in tokens):
            continue
        if path not in selected:
            selected.append(path)
    return tuple(PROJECT_ROOT / path for path in selected if _is_safe_project_text_path(path))


def _read_project_file_snippet(path: Path) -> str:
    try:
        relative = path.relative_to(PROJECT_ROOT)
    except ValueError:
        return ""
    relative_text = str(relative)
    if _is_excluded_project_path(relative_text) or not _is_safe_project_text_path(relative_text):
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    compact = " ".join(text.split())
    return (
        "project_file_snippet: "
        f"path={relative_text}; bytes_read_limit={MAX_PROJECT_FILE_BYTES}; "
        f"content={compact[:MAX_PROJECT_FILE_BYTES]}"
    )


def _is_excluded_project_path(path: str) -> bool:
    parts = Path(path).parts
    return any(part in PROJECT_VISIBILITY_EXCLUDED_DIRS for part in parts)


def _is_safe_project_text_path(path: str) -> bool:
    suffix = Path(path).suffix.casefold()
    if suffix in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".tar", ".gz", ".sqlite", ".db"}:
        return False
    return True
