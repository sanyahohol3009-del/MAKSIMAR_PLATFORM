from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalBackendAdapterStatus,
    build_mgrep_adapter_contract,
    build_qdrant_adapter_contract,
    build_retrieval_backend_status_read_model,
    build_sqlite_vec_adapter_contract,
)


def test_backend_output_requires_normalization_for_all_configured_adapters() -> None:
    status = build_retrieval_backend_status_read_model()
    read_model = status.to_read_model()

    assert read_model["configured_backend_kinds"] == ("mgrep", "sqlite_vec", "qdrant")
    for adapter in read_model["adapter_statuses"]:
        assert adapter["output_requires_normalization"] is True
        assert adapter["source_ref_required"] is True
        assert adapter["evidence_binding_required"] is True
        assert adapter["source_of_truth"] is False
        assert adapter["direct_canonical_write_allowed"] is False
        assert adapter["runtime_mutation_allowed"] is False
        assert adapter["direct_execution_allowed"] is False
        assert adapter["network_allowed_by_default"] is False


def test_adapter_status_rejects_non_normalized_output_claim() -> None:
    with pytest.raises(ValueError, match="output_requires_normalization"):
        RetrievalBackendAdapterStatus(
            adapter_id="retrieval_backend_adapter_mgrep",
            backend_kind="mgrep",
            contract_mode="adapter_only",
            source_of_truth=False,
            output_requires_normalization=False,
            source_ref_required=True,
            evidence_binding_required=True,
            execution_allowed_now=False,
            runtime_mutation_allowed=False,
            direct_canonical_write_allowed=False,
            network_allowed_by_default=False,
        )


def test_phase_7_3_status_extends_existing_phase_7_adapter_contracts() -> None:
    statuses = {
        status.backend_kind: status
        for status in (
            RetrievalBackendAdapterStatus.from_contract(build_mgrep_adapter_contract()),
            RetrievalBackendAdapterStatus.from_contract(build_sqlite_vec_adapter_contract()),
            RetrievalBackendAdapterStatus.from_contract(build_qdrant_adapter_contract()),
        )
    }

    assert tuple(statuses) == ("mgrep", "sqlite_vec", "qdrant")
    assert all(status.contract_mode == "adapter_only" for status in statuses.values())
    assert statuses["qdrant"].network_service_adapter_candidate is True
    assert statuses["qdrant"].runtime_container_required_now is False
    assert statuses["qdrant"].qdrant_server_required_now is False
