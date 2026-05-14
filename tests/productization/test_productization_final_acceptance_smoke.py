from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.PRODUCTIZATION import build_productization_preview
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.productization_summary_builder import (
    build_productization_summary,
)


def test_productization_final_acceptance_smoke() -> None:
    preview = build_productization_preview()
    summary = build_productization_summary()
    doc = Path("docs/architecture/foundation/phase_6_8_productization_sale_ready_sovereign_ai_acceptance_v1.md")

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert preview["sale_ready_claim_allowed"] is True
    assert preview["roadmap_v5_1_closure_allowed_next"] is True
