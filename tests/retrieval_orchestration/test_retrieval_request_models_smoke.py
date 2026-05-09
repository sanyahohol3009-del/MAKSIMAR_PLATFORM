from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    RetrievalRequest,
)


def test_retrieval_request_models_smoke() -> None:
    request = RetrievalRequest(
        request_id="retrieval_req_project_memory_status",
        query="Show project memory status",
        intent="technical_memory",
        language_code="mixed",
        requested_domain="any",
        max_results=6,
        evidence_required=True,
        preview_required=True,
        policy_gate_required=True,
    )

    assert request.request_id == "retrieval_req_project_memory_status"
    assert request.evidence_required is True
    assert request.preview_required is True
    assert request.policy_gate_required is True
