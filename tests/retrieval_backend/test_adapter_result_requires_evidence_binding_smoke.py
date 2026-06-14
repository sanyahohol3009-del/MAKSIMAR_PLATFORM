from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    EvidenceBoundRetrievalResult,
    RetrievalBackendAdapterContract,
    build_default_evidence_binding_contract,
    build_default_retrieval_backend_adapter_contract,
)


def test_adapter_result_requires_evidence_binding_smoke() -> None:
    adapter = build_default_retrieval_backend_adapter_contract()
    binding = build_default_evidence_binding_contract()
    result = EvidenceBoundRetrievalResult(
        result_id="retrieval_result_evidence_bound",
        result_text="Result is tied to source_ref and evidence_id.",
        score=0.9,
        evidence_binding=binding,
    )

    validated = adapter.validate_result(result)

    assert validated.evidence_binding.source_ref
    assert validated.evidence_binding.evidence_id
    assert validated.evidence_binding.trace_id
    assert validated.source_of_truth is False
    assert validated.direct_canonical_write_allowed is False
    assert validated.runtime_mutation_allowed is False


def test_adapter_result_without_evidence_binding_is_invalid() -> None:
    adapter = build_default_retrieval_backend_adapter_contract()

    with pytest.raises(TypeError, match="EvidenceBoundRetrievalResult"):
        adapter.validate_result(
            {
                "result_id": "retrieval_result_unbound",
                "source_ref": "",
                "evidence_id": "",
            }  # type: ignore[arg-type]
        )

    with pytest.raises(TypeError, match="evidence_binding"):
        EvidenceBoundRetrievalResult(
            result_id="retrieval_result_missing_evidence_binding",
            result_text="invalid",
            score=0.1,
            evidence_binding=None,  # type: ignore[arg-type]
        )


def test_adapter_contract_rejects_missing_evidence_requirement() -> None:
    with pytest.raises(ValueError, match="evidence_binding_required"):
        RetrievalBackendAdapterContract(
            adapter_id="retrieval_backend_adapter_no_evidence",
            backend_kind="qdrant",
            adapter_mode="adapter_only",
            truth_status="not_source_of_truth",
            allowed_domains=("technical_memory",),
            evidence_binding_required=False,
        )
