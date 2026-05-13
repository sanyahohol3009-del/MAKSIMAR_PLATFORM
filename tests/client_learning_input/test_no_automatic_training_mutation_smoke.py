from __future__ import annotations

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_client_learning_input_preview


def test_no_automatic_training_mutation_smoke() -> None:
    preview = build_client_learning_input_preview()

    assert preview["automatic_training_allowed"] is False
    assert preview["direct_model_mutation_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["productization_allowed_now"] is False
