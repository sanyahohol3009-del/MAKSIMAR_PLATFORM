from __future__ import annotations

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_learning_input_pack


def test_learning_input_pack_models_smoke() -> None:
    pack = build_learning_input_pack()

    assert pack.pack_ready is True
    assert pack.phase_id == "PHASE 6.6"
    assert len(pack.items) >= 5
    assert pack.tenant_boundary_ready is True
    assert pack.privacy_boundary_ready is True
    assert pack.automatic_training_allowed is False
    assert pack.direct_model_mutation_allowed is False
