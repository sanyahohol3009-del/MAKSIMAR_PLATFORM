from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.controlled_codegen_context_summary_builder import (
    build_controlled_codegen_context_summary,
)


def test_controlled_codegen_final_acceptance_smoke() -> None:
    preview = build_codegen_preview()
    summary = build_controlled_codegen_context_summary()
    doc = Path("docs/architecture/foundation/phase_6_3_controlled_codegen_context_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["sandbox_owner_review_allowed_next"] is True
    assert preview["direct_core_write_allowed"] is False
