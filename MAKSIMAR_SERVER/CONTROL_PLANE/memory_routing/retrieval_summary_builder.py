from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_router import (
    build_retrieval_route_plan,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_trace_builder import (
    build_retrieval_trace,
)


def build_retrieval_summary() -> Dict[str, object]:
    route_plan = build_retrieval_route_plan()
    trace = build_retrieval_trace()

    return {
        "request_id": route_plan.request.request_id,
        "intent": route_plan.request.intent,
        "requested_domain": route_plan.request.requested_domain,
        "selected_source_count": route_plan.selected_source_count,
        "evidence_item_count": route_plan.evidence_item_count,
        "citation_required_items": route_plan.evidence_pack.citation_required_items,
        "conflict_marked_items": route_plan.evidence_pack.conflict_marked_items,
        "policy_gate_passed": route_plan.policy_gate_passed,
        "backend_execution_required": route_plan.backend_execution_required,
        "route_ready": route_plan.route_ready,
        "preview_trace_ready": trace.preview_trace_ready,
        "retrieval_summary_ready": True,
    }
