from __future__ import annotations

import importlib
from typing import Any, Iterator


def build_jarvis_live_brain_health() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_brain_health()


def build_jarvis_live_session_status() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_session_status()


def run_jarvis_live_brain_once(user_text: str, session_id: str = "windows_voice_edge") -> dict[str, Any]:
    return _brain_loop().run_jarvis_live_brain_once(user_text, session_id=session_id)


def stream_jarvis_live_brain_response(
    user_text: str,
    session_id: str = "windows_voice_edge",
) -> Iterator[dict[str, Any]]:
    yield from _brain_loop().stream_jarvis_live_brain_response(user_text, session_id=session_id)


def write_stream_event_safely(write_callable: Any, event: dict[str, Any]) -> bool:
    return _brain_loop().write_stream_event_safely(write_callable, event)


def build_jarvis_live_project_status_read_model() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_project_status_read_model()


def build_jarvis_live_tool_catalog_read_model() -> dict[str, Any]:
    return _brain_loop().build_jarvis_live_tool_catalog_read_model()


def build_project_workspace_read_model() -> dict[str, Any]:
    return _brain_loop().build_project_workspace_read_model()


def model_runtime_status() -> dict[str, Any]:
    return _brain_loop().model_runtime_status()


def read_file_outline(path: str) -> dict[str, Any]:
    return _brain_loop().read_file_outline(path)


def read_file_snippet(
    path: str,
    start_line: int = 1,
    end_line: int | None = None,
    page: int = 1,
) -> dict[str, Any]:
    return _brain_loop().read_file_snippet(
        path,
        start_line=start_line,
        end_line=end_line,
        page=page,
    )


def repo_files(page: int = 1, page_size: int = 80) -> dict[str, Any]:
    return _brain_loop().repo_files(page=page, page_size=page_size)


def repo_git_status() -> dict[str, Any]:
    return _brain_loop().repo_git_status()


def repo_import_graph(path: str | None = None, max_edges: int = 80) -> dict[str, Any]:
    return _brain_loop().repo_import_graph(path=path, max_edges=max_edges)


def repo_search(
    query: str,
    paths: tuple[str, ...] | None = None,
    max_results: int = 40,
) -> dict[str, Any]:
    return _brain_loop().repo_search(query, paths=paths, max_results=max_results)


def repo_tree(depth: int = 2, max_entries: int = 300) -> dict[str, Any]:
    return _brain_loop().repo_tree(depth=depth, max_entries=max_entries)


def status_tools() -> dict[str, Any]:
    return _brain_loop().status_tools()


def _brain_loop() -> Any:
    return importlib.import_module("tools.jarvis_live_runtime.jarvis_live_brain_loop")
