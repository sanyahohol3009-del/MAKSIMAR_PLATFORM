from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalVendorGateContract,
    build_retrieval_vendor_gate_contract,
    build_retrieval_vendor_source_contracts,
)


def test_retrieval_vendor_gate_contract_blocks_runtime() -> None:
    gate = build_retrieval_vendor_gate_contract()
    read_model = gate.to_read_model()

    assert read_model["vendor_gate_required"] is True
    assert read_model["source_verified_required"] is True
    assert read_model["license_review_required"] is True
    assert read_model["scanner_required"] is True
    assert read_model["manifest_required"] is True
    assert read_model["runtime_enabled"] is False
    assert read_model["install_allowed"] is False
    assert read_model["download_allowed_now"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["source_of_truth"] is False
    assert [source["backend_kind"] for source in read_model["vendor_sources"]] == ["sqlite_vec", "qdrant", "mgrep"]


def test_retrieval_vendor_gate_rejects_runtime_enablement() -> None:
    with pytest.raises(ValueError, match="runtime_enabled"):
        RetrievalVendorGateContract(
            gate_id="retrieval_vendor_gate_contract_v1",
            vendor_sources=build_retrieval_vendor_source_contracts(),
            runtime_enabled=True,
        )
