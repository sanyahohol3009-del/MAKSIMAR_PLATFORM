from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_evidence_pack_models import (
    RetrievalEvidenceItem,
    RetrievalEvidencePack,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_request_models import (
    RetrievalRequest,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_scope_models import (
    RetrievalScope,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_selection_policy import (
    select_retrieval_sources,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_source_binding_models import (
    RetrievalSourceBinding,
)


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalRoutePlan:
    """Deterministic retrieval route plan.

    This is not a search result. It is an orchestration plan with selected
    sources and an evidence pack skeleton derived from approved sources.
    """

    request: RetrievalRequest
    scope: RetrievalScope
    selected_sources: tuple[RetrievalSourceBinding, ...]
    evidence_pack: RetrievalEvidencePack
    selected_source_count: int
    evidence_item_count: int
    policy_gate_passed: bool
    backend_execution_required: bool
    route_ready: bool

    def __post_init__(self) -> None:
        selected_source_count = _ensure_non_negative_int(
            self.selected_source_count,
            "selected_source_count",
        )
        evidence_item_count = _ensure_non_negative_int(
            self.evidence_item_count,
            "evidence_item_count",
        )

        if selected_source_count != len(self.selected_sources):
            raise ValueError("selected_source_count must match selected_sources length")
        if evidence_item_count != self.evidence_pack.total_items:
            raise ValueError("evidence_item_count must match evidence pack total_items")
        if evidence_item_count > self.request.max_results:
            raise ValueError("evidence_item_count must not exceed request.max_results")

        for field_name in (
            "policy_gate_passed",
            "backend_execution_required",
            "route_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.policy_gate_passed:
            raise ValueError("policy_gate_passed must be True")
        if not self.route_ready:
            raise ValueError("route_ready must be True")

        object.__setattr__(self, "selected_source_count", selected_source_count)
        object.__setattr__(self, "evidence_item_count", evidence_item_count)


def build_default_retrieval_request() -> RetrievalRequest:
    return RetrievalRequest(
        request_id="retrieval_req_project_memory_status",
        query="Show project memory and artifact status with evidence",
        intent="technical_memory",
        language_code="mixed",
        requested_domain="any",
        max_results=6,
        evidence_required=True,
        preview_required=True,
        policy_gate_required=True,
    )


def build_default_retrieval_scope() -> RetrievalScope:
    return RetrievalScope(
        scope_id="retrieval_scope_project_memory",
        allowed_memory_domains=(
            "project_history",
            "technical_memory",
            "storage_registry",
            "media_memory",
            "global_memory_registry",
        ),
        allowed_source_kinds=(
            "history_ingestion",
            "history_binding",
            "storage_registry",
            "media_memory",
            "memory_registry",
            "ai_router_binding",
        ),
        forbidden_source_kinds=(
            "raw_binary_payload",
            "unapproved_external_backend",
            "direct_filesystem_write",
        ),
        tenant_boundary_required=True,
        policy_gate_required=True,
        cross_domain_allowed=True,
    )


def build_default_retrieval_source_bindings() -> tuple[RetrievalSourceBinding, ...]:
    return (
        RetrievalSourceBinding(
            source_id="retrieval_source_history_ingestion",
            source_kind="history_ingestion",
            memory_domain="project_history",
            registry_ref="MAKSIMAR_CORE_LIB/memory_engine/history_ingestion",
            priority=10,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
        RetrievalSourceBinding(
            source_id="retrieval_source_history_binding",
            source_kind="history_binding",
            memory_domain="project_history",
            registry_ref="MAKSIMAR_CORE_LIB/memory_engine/history_binding",
            priority=20,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
        RetrievalSourceBinding(
            source_id="retrieval_source_storage_registry",
            source_kind="storage_registry",
            memory_domain="storage_registry",
            registry_ref="MAKSIMAR_CORE_LIB/memory_engine/storage_registry",
            priority=30,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
        RetrievalSourceBinding(
            source_id="retrieval_source_media_memory",
            source_kind="media_memory",
            memory_domain="media_memory",
            registry_ref="MAKSIMAR_CORE_LIB/memory_engine/media_memory",
            priority=40,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
        RetrievalSourceBinding(
            source_id="retrieval_source_memory_registry",
            source_kind="memory_registry",
            memory_domain="global_memory_registry",
            registry_ref="MAKSIMAR_SERVER/MEMORY_REGISTRY",
            priority=50,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
        RetrievalSourceBinding(
            source_id="retrieval_source_ai_router_binding",
            source_kind="ai_router_binding",
            memory_domain="technical_memory",
            registry_ref="MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding",
            priority=60,
            evidence_supported=True,
            trace_supported=True,
            policy_allowed=True,
            backend_adapter_required=False,
        ),
    )


def build_retrieval_evidence_pack(
    request: RetrievalRequest,
    selected_sources: tuple[RetrievalSourceBinding, ...],
) -> RetrievalEvidencePack:
    evidence_items = tuple(
        RetrievalEvidenceItem(
            evidence_id=f"evidence_{source.source_kind}",
            source_id=source.source_id,
            source_event_ref=f"source_event://{source.source_kind}/preview",
            artifact_ref=f"artifact://retrieval/{source.source_kind}/preview",
            source_version="v1",
            summary=f"Evidence preview from {source.source_kind}",
            citation_required=True,
            conflict_marker="",
        )
        for source in selected_sources[: request.max_results]
    )

    return RetrievalEvidencePack(
        request_id=request.request_id,
        total_items=len(evidence_items),
        citation_required_items=sum(1 for item in evidence_items if item.citation_required),
        conflict_marked_items=sum(1 for item in evidence_items if item.conflict_marker),
        evidence_items=evidence_items,
    )


def build_retrieval_route_plan() -> RetrievalRoutePlan:
    request = build_default_retrieval_request()
    scope = build_default_retrieval_scope()
    sources = build_default_retrieval_source_bindings()
    selected_sources = select_retrieval_sources(request, scope, sources)
    evidence_pack = build_retrieval_evidence_pack(request, selected_sources)

    backend_execution_required = any(source.backend_adapter_required for source in selected_sources)

    return RetrievalRoutePlan(
        request=request,
        scope=scope,
        selected_sources=selected_sources,
        evidence_pack=evidence_pack,
        selected_source_count=len(selected_sources),
        evidence_item_count=evidence_pack.total_items,
        policy_gate_passed=True,
        backend_execution_required=backend_execution_required,
        route_ready=True,
    )
