from __future__ import annotations

from MAKSIMAR_CORE_LIB.security_layer.security_semantic_duplicate_binding import (
    build_security_semantic_duplicate_binding,
)


def test_security_semantic_duplicate_binding_is_read_only_and_safe() -> None:
    binding = build_security_semantic_duplicate_binding(
        existing_source_count=262,
        migration_candidate_count=225,
        wrap_as_adapter_count=107,
        create_new_count=0,
    )

    assert binding.true_duplicate_risk_count == 0
    assert binding.high_risk_count == 0
    assert binding.scan_readonly is True
    assert binding.delete_allowed is False
    assert binding.move_allowed is False
    assert binding.runtime_mutation_allowed is False
    assert binding.canonical_write_allowed is False
    assert binding.dashboard_safe is True
    assert binding.to_dict()["decision"] == (
        "create_new_security_models_reference_existing_policy_surfaces"
    )
