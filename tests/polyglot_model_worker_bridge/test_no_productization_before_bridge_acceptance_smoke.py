from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_polyglot_model_worker_preview


def test_no_productization_before_bridge_acceptance_smoke() -> None:
    preview = build_polyglot_model_worker_preview()

    assert preview["direct_model_mutation_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["deployment_allowed"] is False
    assert preview["productization_allowed_now"] is False
