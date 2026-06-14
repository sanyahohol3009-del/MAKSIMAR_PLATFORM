from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalBackendAdapterContract,
    build_default_evidence_bound_retrieval_result,
    build_default_retrieval_backend_adapter_contract,
)


def test_retrieval_backend_adapter_contract_smoke() -> None:
    contract = build_default_retrieval_backend_adapter_contract()
    read_model = contract.to_read_model()

    assert isinstance(contract, RetrievalBackendAdapterContract)
    assert read_model["backend_kind"] == "in_memory_reference"
    assert read_model["adapter_mode"] == "adapter_only"
    assert read_model["truth_status"] == "not_source_of_truth"
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["adapter_only"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["direct_canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["auto_promotion_allowed"] is False
    assert read_model["direct_execution_allowed"] is False


def test_retrieval_backend_adapter_allows_declared_backend_candidates_only() -> None:
    for backend_kind in ("mgrep", "sqlite_vec", "qdrant", "in_memory_reference"):
        contract = RetrievalBackendAdapterContract(
            adapter_id=f"retrieval_backend_adapter_{backend_kind}",
            backend_kind=backend_kind,  # type: ignore[arg-type]
            adapter_mode="adapter_only",
            truth_status="not_source_of_truth",
            allowed_domains=("technical_memory",),
        )
        assert contract.backend_kind == backend_kind

    with pytest.raises(ValueError, match="unsupported backend_kind"):
        RetrievalBackendAdapterContract(
            adapter_id="retrieval_backend_adapter_unknown",
            backend_kind="unknown",  # type: ignore[arg-type]
            adapter_mode="adapter_only",
            truth_status="not_source_of_truth",
            allowed_domains=("technical_memory",),
        )


def test_retrieval_backend_adapter_rejects_truth_write_runtime_network_execution() -> None:
    with pytest.raises(ValueError, match="source of truth"):
        RetrievalBackendAdapterContract(
            adapter_id="retrieval_backend_adapter_bad_truth",
            backend_kind="qdrant",
            adapter_mode="adapter_only",
            truth_status="not_source_of_truth",
            allowed_domains=("technical_memory",),
            source_of_truth=True,
        )

    unsafe_fields = (
        "direct_canonical_write_allowed",
        "runtime_mutation_allowed",
        "network_allowed_by_default",
        "auto_promotion_allowed",
        "direct_execution_allowed",
    )
    for field_name in unsafe_fields:
        with pytest.raises(ValueError, match=field_name):
            RetrievalBackendAdapterContract(
                adapter_id=f"retrieval_backend_adapter_bad_{field_name}",
                backend_kind="qdrant",
                adapter_mode="adapter_only",
                truth_status="not_source_of_truth",
                allowed_domains=("technical_memory",),
                **{field_name: True},
            )


def test_retrieval_backend_adapter_validates_evidence_bound_result() -> None:
    contract = build_default_retrieval_backend_adapter_contract()
    result = build_default_evidence_bound_retrieval_result()

    assert contract.validate_result(result) is result
    with pytest.raises(TypeError, match="EvidenceBoundRetrievalResult"):
        contract.validate_result(object())  # type: ignore[arg-type]
