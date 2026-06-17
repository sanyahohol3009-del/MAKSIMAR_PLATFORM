from __future__ import annotations

import ast
import inspect
from pathlib import Path

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import memory_context_sources


def test_brain_loop_uses_extracted_memory_context_sources() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._retrieve_history_snippets).__name__ == (
        "tools.jarvis_live_runtime.memory_context_sources"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._retrieve_local_chat_memory_snippets).__name__ == (
        "tools.jarvis_live_runtime.memory_context_sources"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._build_memory_surface_inventory).__name__ == (
        "tools.jarvis_live_runtime.memory_context_sources"
    )


def test_memory_federation_aggregator_remains_patchable_in_brain_loop() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._retrieve_memory_federation_snippets).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_brain_loop"
    )


def test_memory_context_sources_are_read_only_by_default() -> None:
    inventory = memory_context_sources._build_memory_surface_inventory()

    assert inventory
    assert all(surface["canonical_memory_write_allowed"] is False for surface in inventory)
    assert all(surface["pc_control_allowed"] is False for surface in inventory)
    assert all(surface["forbidden_direct_write"] is True for surface in inventory)


def test_memory_context_query_helpers_preserve_voice_and_gpt_terms() -> None:
    terms = memory_context_sources._memory_query_terms("Джарвис помнишь что говорили про голос и GPT")
    assert "голос" in terms
    assert "voice" in terms
    assert "gpt" in terms


def test_deep_memory_and_project_visibility_markers_still_work() -> None:
    assert memory_context_sources._needs_deep_memory("что у нас по проекту и voice")
    assert memory_context_sources._needs_project_visibility("покажи дерево проекта")
    assert not memory_context_sources._needs_project_visibility("привет как дела")


def test_moved_leaf_functions_no_longer_defined_in_brain_loop() -> None:
    tree = ast.parse(Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(encoding="utf-8"))
    moved = {
        "_memory_query_terms",
        "_asks_style_memory_recall",
        "_asks_memory_recall",
        "_has_stored_memory_for_recall",
        "_retrieve_history_snippets",
        "_retrieve_project_workspace_snippets",
        "_retrieve_memory_engine_snippets",
        "_retrieve_enterprise_memory_snippets",
        "_retrieve_regulatory_memory_snippets",
        "_retrieve_vector_memory_snippets",
        "_retrieve_mempalace_status_snippets",
        "_retrieve_local_chat_memory_snippets",
        "_build_memory_surface_inventory",
        "_mempalace_status",
        "_needs_deep_memory",
        "_needs_project_visibility",
    }
    found = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in moved
    }
    assert found == set()
