from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_release_preview


def test_memory_full_preview_path_smoke() -> None:
    preview = build_memory_release_preview()

    assert preview["preview_path"] == (
        "phase_5_2_final_memory_map",
        "phase_6_0_acceptance_gates",
        "phase_6_0_write_safety",
        "phase_6_0_operator_review",
        "phase_6_0_release_candidate",
        "phase_6_0_release_preview",
    )
