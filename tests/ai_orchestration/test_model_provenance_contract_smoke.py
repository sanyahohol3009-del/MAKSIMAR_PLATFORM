from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.model_provenance_contract import (
    ModelProvenanceContract,
    build_default_model_provenance_contract,
)


def test_default_model_provenance_contract_is_read_only() -> None:
    contract = build_default_model_provenance_contract()

    assert contract.provenance_id == "model_provenance_v1"
    assert contract.provenance_ready is True
    assert contract.canonical_evidence_memory_write_allowed is False
    assert contract.model_runtime_execution_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True


def test_model_provenance_contract_rejects_evidence_memory_write() -> None:
    with pytest.raises(ValueError, match="canonical_evidence_memory_write_allowed"):
        ModelProvenanceContract(
            provenance_id="bad",
            model_id="model",
            model_family="family",
            route_reason="reason",
            source_binding_ref="ref",
            provenance_ready=True,
            canonical_evidence_memory_write_allowed=True,
            model_runtime_execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_model_provenance_contract_rejects_model_runtime_execution() -> None:
    with pytest.raises(ValueError, match="model_runtime_execution_allowed"):
        ModelProvenanceContract(
            provenance_id="bad",
            model_id="model",
            model_family="family",
            route_reason="reason",
            source_binding_ref="ref",
            provenance_ready=True,
            canonical_evidence_memory_write_allowed=False,
            model_runtime_execution_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
