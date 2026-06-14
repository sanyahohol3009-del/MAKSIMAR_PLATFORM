from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalVendorSourceContract,
    build_retrieval_vendor_source_contracts,
)


def test_retrieval_vendor_source_contracts_are_fail_closed() -> None:
    contracts = build_retrieval_vendor_source_contracts()
    by_kind = {contract.backend_kind: contract.to_read_model() for contract in contracts}

    assert set(by_kind) == {"sqlite_vec", "qdrant", "mgrep"}
    assert by_kind["sqlite_vec"]["source_url"] == "https://github.com/asg017/sqlite-vec"
    assert by_kind["qdrant"]["source_url"] == "https://github.com/qdrant/qdrant"
    assert by_kind["mgrep"]["source_url"] == "unresolved_until_verified"
    assert by_kind["mgrep"]["fail_closed_until_source_verified"] is True

    for read_model in by_kind.values():
        assert read_model["vendor_gate_required"] is True
        assert read_model["vendor_gate_completed"] is False
        assert read_model["runtime_enabled"] is False
        assert read_model["install_allowed"] is False
        assert read_model["download_allowed_now"] is False
        assert read_model["write_allowed"] is False
        assert read_model["source_of_truth"] is False
        assert read_model["direct_execution_allowed"] is False
        assert read_model["network_allowed_by_default"] is False
        assert read_model["license_status"] == "pending_vendor_gate"
        assert read_model["scan_status"] == "not_scanned"


def test_mgrep_source_must_fail_closed_until_verified() -> None:
    with pytest.raises(ValueError, match="mgrep must fail closed"):
        RetrievalVendorSourceContract(
            vendor_source_id="retrieval_vendor_source_mgrep",
            backend_kind="mgrep",
            source_url="unresolved_until_verified",
            source_status="unresolved_until_verified",
            source_ref="EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml#mgrep",
            version_ref="unresolved_until_verified",
        )
