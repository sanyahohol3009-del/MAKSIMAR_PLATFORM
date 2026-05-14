from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_track_entry_preview


def test_regulatory_track_preview_builder_smoke() -> None:
    preview = build_regulatory_track_entry_preview()

    assert preview["preview_ready"] is True
    assert preview["next_step"] == "STEP 2 — Country / Jurisdiction Registry Binding"
    assert preview["stage_count"] == 9
    assert preview["rule_count"] == 5
    assert preview["reopen_memory_v5_1_allowed"] is False
    assert preview["no_second_memory_world"] is True
    assert preview["mempalace_source_of_truth_allowed"] is False
