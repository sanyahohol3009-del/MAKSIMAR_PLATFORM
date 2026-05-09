from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_backend_policy_gate import (
    build_retrieval_backend_policy_gate,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_batch2_preview_builder import (
    build_retrieval_batch2_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_preview_builder import (
    build_retrieval_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_registry_binding_builder import (
    build_retrieval_registry_binding_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_trace_builder import (
    build_retrieval_trace,
)


_EXPECTED_PHASE_FLOW = (
    "retrieval_request",
    "retrieval_scope",
    "source_selection_policy",
    "evidence_pack",
    "registry_ai_observability_binding",
    "backend_policy_gate",
    "preview_trace",
    "phase_readiness",
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
class RetrievalPhaseReadiness:
    selected_source_count: int
    evidence_item_count: int
    registry_total_bindings: int
    registry_ready_bindings: int
    observability_router_binding_entries: int
    approved_backends: int
    blocked_backends: int
    flow: tuple[str, ...]
    route_ready: bool
    preview_ready: bool
    batch2_ready: bool
    registry_binding_ready: bool
    observability_ready: bool
    trace_ready: bool
    backend_policy_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        selected_source_count = _ensure_non_negative_int(
            self.selected_source_count,
            "selected_source_count",
        )
        evidence_item_count = _ensure_non_negative_int(
            self.evidence_item_count,
            "evidence_item_count",
        )
        registry_total_bindings = _ensure_non_negative_int(
            self.registry_total_bindings,
            "registry_total_bindings",
        )
        registry_ready_bindings = _ensure_non_negative_int(
            self.registry_ready_bindings,
            "registry_ready_bindings",
        )
        observability_router_binding_entries = _ensure_non_negative_int(
            self.observability_router_binding_entries,
            "observability_router_binding_entries",
        )
        approved_backends = _ensure_non_negative_int(self.approved_backends, "approved_backends")
        blocked_backends = _ensure_non_negative_int(self.blocked_backends, "blocked_backends")

        if tuple(self.flow) != _EXPECTED_PHASE_FLOW:
            raise ValueError("flow must match expected PHASE 1.7 flow")

        for field_name in (
            "route_ready",
            "preview_ready",
            "batch2_ready",
            "registry_binding_ready",
            "observability_ready",
            "trace_ready",
            "backend_policy_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
            "phase_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if selected_source_count <= 0:
            raise ValueError("selected_source_count must be >= 1")
        if evidence_item_count <= 0:
            raise ValueError("evidence_item_count must be >= 1")
        if registry_total_bindings <= 0:
            raise ValueError("registry_total_bindings must be >= 1")
        if registry_ready_bindings != registry_total_bindings:
            raise ValueError("all registry bindings must be ready")
        if observability_router_binding_entries <= 0:
            raise ValueError("observability_router_binding_entries must be >= 1")
        if approved_backends <= 0:
            raise ValueError("approved_backends must be >= 1")
        if blocked_backends <= 0:
            raise ValueError("blocked_backends must be >= 1")
        if not self.route_ready:
            raise ValueError("route_ready must be True")
        if not self.preview_ready:
            raise ValueError("preview_ready must be True")
        if not self.batch2_ready:
            raise ValueError("batch2_ready must be True")
        if not self.registry_binding_ready:
            raise ValueError("registry_binding_ready must be True")
        if not self.observability_ready:
            raise ValueError("observability_ready must be True")
        if not self.trace_ready:
            raise ValueError("trace_ready must be True")
        if not self.backend_policy_ready:
            raise ValueError("backend_policy_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False in PHASE 1.7")
        if not self.phase_ready:
            raise ValueError("phase_ready must be True")

        object.__setattr__(self, "selected_source_count", selected_source_count)
        object.__setattr__(self, "evidence_item_count", evidence_item_count)
        object.__setattr__(self, "registry_total_bindings", registry_total_bindings)
        object.__setattr__(self, "registry_ready_bindings", registry_ready_bindings)
        object.__setattr__(
            self,
            "observability_router_binding_entries",
            observability_router_binding_entries,
        )
        object.__setattr__(self, "approved_backends", approved_backends)
        object.__setattr__(self, "blocked_backends", blocked_backends)


def build_retrieval_phase_readiness() -> RetrievalPhaseReadiness:
    retrieval_preview = build_retrieval_preview()
    batch2_preview = build_retrieval_batch2_preview()
    registry_binding = build_retrieval_registry_binding_contract()
    trace = build_retrieval_trace()
    backend_gate = build_retrieval_backend_policy_gate()

    phase_ready = (
        bool(retrieval_preview["route_ready"])
        and bool(retrieval_preview["preview_ready"])
        and bool(batch2_preview["batch2_ready"])
        and registry_binding.binding_ready
        and bool(batch2_preview["observability_ready"])
        and trace.preview_trace_ready
        and backend_gate.policy_gate_ready
        and backend_gate.mgrep_blocked
        and backend_gate.sqlite_vec_blocked
        and not backend_gate.backend_execution_allowed
    )

    return RetrievalPhaseReadiness(
        selected_source_count=int(retrieval_preview["selected_source_count"]),
        evidence_item_count=int(retrieval_preview["evidence_item_count"]),
        registry_total_bindings=registry_binding.total_bindings,
        registry_ready_bindings=registry_binding.ready_bindings,
        observability_router_binding_entries=int(
            batch2_preview["observability_router_binding_entries"]
        ),
        approved_backends=backend_gate.approved_backends,
        blocked_backends=backend_gate.blocked_backends,
        flow=_EXPECTED_PHASE_FLOW,
        route_ready=bool(retrieval_preview["route_ready"]),
        preview_ready=bool(retrieval_preview["preview_ready"]),
        batch2_ready=bool(batch2_preview["batch2_ready"]),
        registry_binding_ready=registry_binding.binding_ready,
        observability_ready=bool(batch2_preview["observability_ready"]),
        trace_ready=trace.preview_trace_ready,
        backend_policy_ready=backend_gate.policy_gate_ready,
        mgrep_blocked=backend_gate.mgrep_blocked,
        sqlite_vec_blocked=backend_gate.sqlite_vec_blocked,
        backend_execution_allowed=backend_gate.backend_execution_allowed,
        phase_ready=phase_ready,
    )
