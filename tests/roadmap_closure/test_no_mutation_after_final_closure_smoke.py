from __future__ import annotations

from MAKSIMAR_SERVER.ROADMAP_CLOSURE import build_final_closure_preview


def test_no_mutation_after_final_closure_smoke() -> None:
    preview = build_final_closure_preview()

    assert preview["direct_core_write_allowed"] is False
    assert preview["auto_apply_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["deployment_allowed_now"] is False
    assert preview["external_release_allowed_now"] is False
