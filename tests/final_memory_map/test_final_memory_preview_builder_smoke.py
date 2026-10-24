from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_preview


def test_final_memory_preview_builder_smoke() -> None:
    preview = build_final_memory_preview()

    assert preview["preview_ready"] is True
    assert preview["dashboard_read_only"] is True
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False


def test_final_memory_receipt_journal_uses_existing_session_store_owner():
    from pathlib import Path
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import _session_turn_log_path
    preview = build_final_memory_preview()
    assert Path(preview["evidence"]["journal"]).resolve() == _session_turn_log_path().resolve()
    assert preview["experience"]["separate_store"] is False
