from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_owner_review_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.sandbox_owner_review_summary_builder import (
    build_sandbox_owner_review_summary,
)


def test_sandbox_owner_review_final_acceptance_smoke() -> None:
    preview = build_sandbox_owner_review_preview()
    summary = build_sandbox_owner_review_summary()
    doc = Path("docs/architecture/foundation/phase_6_4_sandbox_simulation_owner_review_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["self_expansion_allowed_next"] is True
    assert preview["productization_allowed_now"] is False
