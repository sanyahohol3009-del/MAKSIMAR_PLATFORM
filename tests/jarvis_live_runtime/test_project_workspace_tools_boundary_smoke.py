from __future__ import annotations

import inspect
from pathlib import Path

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import project_workspace_tools


def test_brain_loop_uses_extracted_project_workspace_module() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop.repo_git_status).__name__ == (
        "tools.jarvis_live_runtime.project_workspace_tools"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.repo_search).__name__ == (
        "tools.jarvis_live_runtime.project_workspace_tools"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._project_tree_summary).__name__ == (
        "tools.jarvis_live_runtime.project_workspace_tools"
    )


def test_project_workspace_tools_are_read_only() -> None:
    model = project_workspace_tools.build_project_workspace_read_model() if hasattr(project_workspace_tools, "build_project_workspace_read_model") else None
    status = project_workspace_tools.repo_git_status()
    files = project_workspace_tools.repo_files(page=1, page_size=5)
    tree = project_workspace_tools.repo_tree(depth=1, max_entries=5)

    assert status["read_only"] is True
    assert status["direct_execution_allowed"] is False
    assert status["canonical_write_allowed"] is False
    assert status["pc_control_allowed"] is False
    assert files["read_only"] is True
    assert tree["read_only"] is True
    assert model is None


def test_project_path_guard_blocks_parent_escape() -> None:
    assert project_workspace_tools._safe_project_path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py") is True
    assert project_workspace_tools._safe_project_path("../outside.txt") is False
    assert project_workspace_tools._is_safe_project_text_path("x.py") is True
    assert project_workspace_tools._is_safe_project_text_path("x.png") is False


def test_read_file_snippet_is_read_only() -> None:
    payload = project_workspace_tools.read_file_snippet(
        "tools/jarvis_live_runtime/jarvis_live_brain_loop.py",
        start_line=1,
        end_line=5,
    )

    assert payload["allowed"] is True
    assert payload["read_only"] is True
    assert payload["path"] == "tools/jarvis_live_runtime/jarvis_live_brain_loop.py"
    assert payload["snippet"]


def test_no_project_workspace_functions_remain_defined_in_brain_loop() -> None:
    import ast

    p = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    tree = ast.parse(p.read_text(encoding="utf-8"))

    moved = {
        "repo_git_status",
        "repo_tree",
        "repo_files",
        "repo_search",
        "read_file_snippet",
        "read_file_outline",
        "repo_import_graph",
        "_repo_search_with_rg",
        "_repo_search_with_python",
        "_safe_project_path",
        "_project_tree_summary",
        "_tracked_project_files",
        "_select_project_files_for_context",
        "_read_project_file_snippet",
    }

    found = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in moved
    }
    assert found == set()
