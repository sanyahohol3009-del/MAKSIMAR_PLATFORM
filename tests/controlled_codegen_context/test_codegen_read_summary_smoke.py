from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_read_summary


def test_codegen_read_summary_smoke() -> None:
    summary = build_codegen_read_summary()

    assert summary["summary_ready"] is True
    assert summary["phase_id"] == "PHASE 6.3"
    assert summary["track_scope"] == "controlled_codegen_context"
    assert summary["direct_core_write_allowed"] is False
    assert summary["sandbox_execution_allowed_now"] is False
    assert summary["sandbox_owner_review_allowed_next"] is True
