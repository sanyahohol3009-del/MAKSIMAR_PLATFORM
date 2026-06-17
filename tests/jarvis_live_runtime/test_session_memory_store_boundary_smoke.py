from __future__ import annotations

import inspect
from pathlib import Path

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import session_memory_store


def test_brain_loop_uses_extracted_session_memory_store() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop._load_session_state).__name__ == (
        "tools.jarvis_live_runtime.session_memory_store"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._append_turn).__name__ == (
        "tools.jarvis_live_runtime.session_memory_store"
    )
    assert inspect.getmodule(jarvis_live_brain_loop._memory_truth_split).__name__ == (
        "tools.jarvis_live_runtime.session_memory_store"
    )


def test_empty_session_state_is_safe_by_default() -> None:
    state = session_memory_store._empty_session_state()

    assert state["local_session_persistence"] is True
    assert state["canonical_memory_write_allowed"] is False
    assert state["pc_control_allowed"] is False
    assert state["memory_enabled"] is True
    assert state["session_memory_write_enabled"] is True
    assert state["runtime_history_append_enabled"] is False
    assert state["memory_truth_split"]["canonical_truth"] == "read_only_not_written_by_live_chat"


def test_append_turn_keeps_local_only_bounds() -> None:
    state = session_memory_store._empty_session_state()

    for idx in range(8):
        session_memory_store._append_turn(state, "user", f"message {idx}")

    assert len(state["recent_turns"]) == 4
    assert state["recent_turns"][-1]["text"] == "message 7"
    assert state["canonical_memory_write_allowed"] is False
    assert state["pc_control_allowed"] is False


def test_style_profile_preserves_owner_identity() -> None:
    state = session_memory_store._empty_session_state()
    session_memory_store._update_style_preferences(state, "говори по братски")

    profile = session_memory_store._stable_style_profile_from_state(state)

    assert profile["user_name"] == "Александр"
    assert profile["assistant_identity"] == "JARVIS"
    assert "брат" in profile["explicit_owner_style_preference"]


def test_session_functions_no_longer_defined_in_brain_loop() -> None:
    import ast

    p = Path("tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    tree = ast.parse(p.read_text(encoding="utf-8"))

    moved = {
        "_append_assistant_and_summarize",
        "_append_turn",
        "_append_local_chat_memory_record",
        "_session_turn_log_path",
        "_read_recent_local_chat_records",
        "_load_session_state",
        "_save_session_state",
        "_empty_session_state",
        "_normalize_session_state",
        "_stable_style_profile_from_state",
        "_update_style_preferences",
        "_extract_style_preference",
        "_memory_enablement_flags",
        "_memory_truth_split",
        "_timestamp",
        "_day_bucket",
        "_brief_turn_summary",
        "_detect_active_task",
        "_build_rolling_summary",
        "_extract_active_topics",
        "_format_turns",
        "_format_style_profile",
    }

    found = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in moved
    }
    assert found == set()
