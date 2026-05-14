from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import (
    build_regulatory_track_entry_preview,
    build_regulatory_track_entry_summary,
)


def test_regulatory_track_entry_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/regulatory_track_entry_surface_inventory_v1.md")
    preview = build_regulatory_track_entry_preview()
    summary = build_regulatory_track_entry_summary()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert summary["summary_ready"] is True
    assert summary["current_step"] == "STEP 1 — Regulatory Track Entry / Surface Inventory"
    assert summary["next_step"] == "STEP 2 — Country / Jurisdiction Registry Binding"
    assert summary["runtime_mutation_allowed"] is False
    assert summary["direct_core_write_allowed"] is False
    assert summary["deployment_allowed_now"] is False
