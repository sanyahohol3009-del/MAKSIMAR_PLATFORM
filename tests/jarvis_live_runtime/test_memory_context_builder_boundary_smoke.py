from __future__ import annotations

import ast
import inspect
from pathlib import Path

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import memory_context_builder


def test_brain_loop_uses_extracted_memory_context_builder() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop.JarvisBrainContext).__name__ == (
        "tools.jarvis_live_runtime.memory_context_builder"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.build_jarvis_live_brain_context).__name__ == (
        "tools.jarvis_live_runtime.memory_context_builder"
    )


def test_memory_federation_aggregator_moved_to_builder() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._retrieve_memory_federation_snippets).__name__ == (
        "tools.jarvis_live_runtime.memory_context_builder"
    )


def test_context_builder_returns_safe_context() -> None:
    context = memory_context_builder.build_jarvis_live_brain_context(
        "привет",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
        session_id="boundary_test",
    )

    assert context.user_text == "привет"
    assert context.session_id == "boundary_test"
    assert context.pc_control_allowed is False
    assert context.canonical_memory_write_allowed is False
    assert context.admission_status["pc_control_allowed"] is False


def test_context_builder_definitions_no_longer_defined_in_brain_loop() -> None:
    tree = ast.parse(Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py").read_text(encoding="utf-8"))

    moved = {
        "JarvisBrainContext",
        "build_jarvis_live_brain_context",
        "_retrieve_memory_federation_snippets",
    }
    found = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name in moved
    }
    assert found == set()
