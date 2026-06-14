from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    EvidenceBindingContract,
    EvidenceBoundRetrievalResult,
    build_default_evidence_bound_retrieval_result,
    build_mgrep_adapter_contract,
    build_qdrant_adapter_contract,
    build_sqlite_vec_adapter_contract,
)


def test_adapter_cannot_be_evidence_source_of_truth_smoke() -> None:
    adapters = (
        build_mgrep_adapter_contract(),
        build_sqlite_vec_adapter_contract(),
        build_qdrant_adapter_contract(),
    )
    result = build_default_evidence_bound_retrieval_result()

    for adapter in adapters:
        validated = adapter.validate_output(result)
        read_model = validated.to_read_model()
        assert read_model["evidence_binding"]["source_ref"]
        assert read_model["evidence_binding"]["evidence_id"]
        assert read_model["evidence_binding"]["canonical_truth_claim_allowed"] is False
        assert read_model["source_of_truth"] is False
        assert read_model["direct_canonical_write_allowed"] is False
        assert read_model["runtime_mutation_allowed"] is False


def test_evidence_binding_rejects_canonical_truth_claim() -> None:
    with pytest.raises(ValueError, match="canonical truth"):
        EvidenceBindingContract(
            source_ref="MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_evidence_pack_models.py",
            evidence_id="evidence_truth_claim",
            evidence_kind="retrieval_preview",
            confidence=0.9,
            trace_id="trace_truth_claim",
            canonical_truth_claim_allowed=True,
        )


def test_adapter_result_rejects_missing_source_ref_and_missing_evidence_binding() -> None:
    with pytest.raises(ValueError, match="source_ref"):
        EvidenceBindingContract(
            source_ref="",
            evidence_id="evidence_missing_source_ref",
            evidence_kind="retrieval_preview",
            confidence=0.9,
            trace_id="trace_missing_source_ref",
        )

    with pytest.raises(TypeError, match="evidence_binding"):
        EvidenceBoundRetrievalResult(
            result_id="retrieval_result_missing_adapter_evidence",
            result_text="invalid",
            score=0.1,
            evidence_binding=None,  # type: ignore[arg-type]
        )
