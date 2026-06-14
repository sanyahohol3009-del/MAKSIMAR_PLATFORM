from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalPolicyGateContract,
    build_default_retrieval_policy_gate_contract,
    build_mgrep_adapter_contract,
    build_qdrant_adapter_contract,
    build_sqlite_vec_adapter_contract,
)


def test_retrieval_policy_gate_contract_blocks_runtime_and_truth() -> None:
    gate = build_default_retrieval_policy_gate_contract()
    read_model = gate.to_read_model()

    assert read_model["policy_mode"] == "adapter_contract_only"
    assert read_model["allowed_backend_candidates"] == (
        "mgrep",
        "sqlite_vec",
        "qdrant",
        "in_memory_reference",
    )
    assert read_model["execution_allowed_now"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["auto_promotion_allowed"] is False
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["backend_is_source_of_truth"] is False


def test_retrieval_policy_gate_rejects_unsafe_states() -> None:
    unsafe_values = (
        ("execution_allowed_now", True),
        ("network_allowed_by_default", True),
        ("canonical_write_allowed", True),
        ("runtime_mutation_allowed", True),
        ("direct_execution_allowed", True),
        ("auto_promotion_allowed", True),
        ("source_ref_required", False),
        ("evidence_binding_required", False),
        ("backend_is_source_of_truth", True),
    )

    for field_name, value in unsafe_values:
        with pytest.raises(ValueError, match=field_name):
            RetrievalPolicyGateContract(
                policy_id="retrieval_policy_gate_contract_test",
                policy_mode="adapter_contract_only",
                allowed_backend_candidates=("mgrep", "sqlite_vec", "qdrant", "in_memory_reference"),
                **{field_name: value},
            )


def test_all_retrieval_backend_adapters_are_not_source_of_truth() -> None:
    adapters = (
        build_mgrep_adapter_contract(),
        build_sqlite_vec_adapter_contract(),
        build_qdrant_adapter_contract(),
    )

    for adapter in adapters:
        read_model = adapter.to_read_model()
        assert read_model["source_of_truth"] is False
        assert read_model["source_ref_required"] is True
        assert read_model["evidence_binding_required"] is True
        assert read_model["runtime_mutation_allowed"] is False
        assert read_model["network_allowed_by_default"] is False
