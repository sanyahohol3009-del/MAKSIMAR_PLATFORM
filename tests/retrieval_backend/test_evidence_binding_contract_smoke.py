from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    EvidenceBindingContract,
    EvidenceBoundRetrievalResult,
    build_default_evidence_binding_contract,
    build_default_evidence_bound_retrieval_result,
)


def test_evidence_binding_contract_smoke() -> None:
    binding = build_default_evidence_binding_contract()
    read_model = binding.to_read_model()

    assert isinstance(binding, EvidenceBindingContract)
    assert read_model["source_ref"]
    assert read_model["evidence_id"] == "evidence_retrieval_backend_contract"
    assert read_model["evidence_kind"] == "retrieval_preview"
    assert read_model["confidence"] == 1.0
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_id_required"] is True
    assert read_model["citation_required"] is True
    assert read_model["canonical_truth_claim_allowed"] is False


def test_evidence_binding_rejects_missing_source_ref_and_evidence_id() -> None:
    with pytest.raises(ValueError, match="source_ref"):
        EvidenceBindingContract(
            source_ref="",
            evidence_id="evidence_missing_source",
            evidence_kind="source_ref",
            confidence=0.5,
            trace_id="trace_missing_source",
        )

    with pytest.raises(ValueError, match="evidence_id"):
        EvidenceBindingContract(
            source_ref="MAKSIMAR_CORE_LIB/evidence_memory",
            evidence_id="",
            evidence_kind="source_ref",
            confidence=0.5,
            trace_id="trace_missing_evidence",
        )


def test_evidence_bound_result_is_not_truth_or_write_surface() -> None:
    result = build_default_evidence_bound_retrieval_result()
    read_model = result.to_read_model()

    assert isinstance(result, EvidenceBoundRetrievalResult)
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["adapter_result_only"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["direct_canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False


def test_evidence_bound_result_rejects_missing_binding() -> None:
    with pytest.raises(TypeError, match="evidence_binding"):
        EvidenceBoundRetrievalResult(
            result_id="retrieval_result_missing_binding",
            result_text="invalid retrieval result",
            score=0.1,
            evidence_binding=None,  # type: ignore[arg-type]
        )
