from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_router import (
    build_retrieval_route_plan,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_summary_builder import (
    build_retrieval_summary,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_trace_builder import (
    build_retrieval_trace_preview,
)


_RETRIEVAL_PREVIEW_FLOW = (
    "query",
    "intent",
    "domain_scope",
    "policy_gate",
    "source_priority",
    "retrieval_source",
    "evidence_pack",
    "preview_trace",
)


def build_retrieval_preview() -> Dict[str, object]:
    route_plan = build_retrieval_route_plan()
    summary = build_retrieval_summary()
    trace_preview = build_retrieval_trace_preview()

    return {
        "flow": _RETRIEVAL_PREVIEW_FLOW,
        "request_id": route_plan.request.request_id,
        "query": route_plan.request.query,
        "intent": route_plan.request.intent,
        "selected_source_count": route_plan.selected_source_count,
        "evidence_item_count": route_plan.evidence_item_count,
        "selected_sources": tuple(
            {
                "source_id": source.source_id,
                "source_kind": source.source_kind,
                "memory_domain": source.memory_domain,
                "registry_ref": source.registry_ref,
                "priority": source.priority,
                "backend_adapter_required": source.backend_adapter_required,
            }
            for source in route_plan.selected_sources
        ),
        "evidence_pack": tuple(
            {
                "evidence_id": item.evidence_id,
                "source_id": item.source_id,
                "artifact_ref": item.artifact_ref,
                "citation_required": item.citation_required,
                "conflict_marker": item.conflict_marker,
            }
            for item in route_plan.evidence_pack.evidence_items
        ),
        "summary_ready": summary["retrieval_summary_ready"],
        "preview_trace_ready": trace_preview["preview_trace_ready"],
        "policy_gate_passed": route_plan.policy_gate_passed,
        "backend_execution_required": route_plan.backend_execution_required,
        "route_ready": route_plan.route_ready,
        "preview_ready": True,
    }
