from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_source_chain_builder import (
    build_evidence_source_chain_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_source_chain_preview import (
    build_evidence_source_chain_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_phase_readiness_gate import (
    build_retrieval_phase_readiness,
)


_EXPECTED_EVIDENCE_BOUND_MEMORY_FLOW = (
    "retrieval_phase_readiness",
    "evidence_source_chain",
    "source_bound_gate",
    "provenance_bound_gate",
    "trace_bound_gate",
    "citation_required_gate",
    "conflict_clear_gate",
    "backend_policy_gate",
    "evidence_bound_memory_readiness",
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
class EvidenceBoundMemoryPhaseReadiness:
    total_items: int
    source_bound_items: int
    provenance_bound_items: int
    trace_bound_items: int
    citation_required_items: int
    conflict_marked_items: int
    dashboard_visible_items: int
    ready_items: int
    retrieval_selected_sources: int
    retrieval_evidence_items: int
    flow: tuple[str, ...]
    retrieval_phase_ready: bool
    evidence_source_chain_ready: bool
    source_bound_ready: bool
    provenance_bound_ready: bool
    trace_bound_ready: bool
    citation_gate_ready: bool
    conflict_gate_ready: bool
    dashboard_visibility_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    read_only: bool
    no_mutation_surface: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        for field_name in (
            "total_items",
            "source_bound_items",
            "provenance_bound_items",
            "trace_bound_items",
            "citation_required_items",
            "conflict_marked_items",
            "dashboard_visible_items",
            "ready_items",
            "retrieval_selected_sources",
            "retrieval_evidence_items",
        ):
            value = _ensure_non_negative_int(getattr(self, field_name), field_name)
            if field_name != "conflict_marked_items" and value <= 0:
                raise ValueError(f"{field_name} must be >= 1")

        if tuple(self.flow) != _EXPECTED_EVIDENCE_BOUND_MEMORY_FLOW:
            raise ValueError("flow must match expected evidence-bound memory flow")

        for field_name in (
            "retrieval_phase_ready",
            "evidence_source_chain_ready",
            "source_bound_ready",
            "provenance_bound_ready",
            "trace_bound_ready",
            "citation_gate_ready",
            "conflict_gate_ready",
            "dashboard_visibility_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
            "read_only",
            "no_mutation_surface",
            "phase_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.source_bound_items != self.total_items:
            raise ValueError("all evidence items must be source-bound")
        if self.provenance_bound_items != self.total_items:
            raise ValueError("all evidence items must be provenance-bound")
        if self.trace_bound_items != self.total_items:
            raise ValueError("all evidence items must be trace-bound")
        if self.citation_required_items != self.total_items:
            raise ValueError("all evidence items must require citation")
        if self.conflict_marked_items != 0:
            raise ValueError("conflict_marked_items must be 0")
        if self.dashboard_visible_items != self.total_items:
            raise ValueError("all evidence items must be dashboard-visible")
        if self.ready_items != self.total_items:
            raise ValueError("all evidence items must be ready")
        if self.retrieval_evidence_items != self.total_items:
            raise ValueError("retrieval_evidence_items must match total_items")

        if not self.retrieval_phase_ready:
            raise ValueError("retrieval_phase_ready must be True")
        if not self.evidence_source_chain_ready:
            raise ValueError("evidence_source_chain_ready must be True")
        if not self.source_bound_ready:
            raise ValueError("source_bound_ready must be True")
        if not self.provenance_bound_ready:
            raise ValueError("provenance_bound_ready must be True")
        if not self.trace_bound_ready:
            raise ValueError("trace_bound_ready must be True")
        if not self.citation_gate_ready:
            raise ValueError("citation_gate_ready must be True")
        if not self.conflict_gate_ready:
            raise ValueError("conflict_gate_ready must be True")
        if not self.dashboard_visibility_ready:
            raise ValueError("dashboard_visibility_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.no_mutation_surface:
            raise ValueError("no_mutation_surface must be True")
        if not self.phase_ready:
            raise ValueError("phase_ready must be True")


def build_evidence_bound_memory_phase_readiness() -> EvidenceBoundMemoryPhaseReadiness:
    retrieval = build_retrieval_phase_readiness()
    chain = build_evidence_source_chain_contract()
    chain_preview = build_evidence_source_chain_preview()

    source_bound_ready = chain.source_bound_items == chain.total_items
    provenance_bound_ready = chain.provenance_bound_items == chain.total_items
    trace_bound_ready = chain.trace_bound_items == chain.total_items
    citation_gate_ready = chain.citation_required_items == chain.total_items
    conflict_gate_ready = chain.conflict_marked_items == 0
    dashboard_visibility_ready = chain.dashboard_visible_items == chain.total_items
    evidence_source_chain_ready = (
        bool(chain_preview["phase_batch_ready"])
        and chain.ready_items == chain.total_items
    )

    read_only = (
        retrieval.phase_ready
        and evidence_source_chain_ready
        and retrieval.backend_execution_allowed is False
    )
    no_mutation_surface = (
        read_only
        and retrieval.backend_execution_allowed is False
        and chain.backend_execution_allowed is False
    )

    phase_ready = (
        retrieval.phase_ready
        and evidence_source_chain_ready
        and source_bound_ready
        and provenance_bound_ready
        and trace_bound_ready
        and citation_gate_ready
        and conflict_gate_ready
        and dashboard_visibility_ready
        and retrieval.mgrep_blocked
        and retrieval.sqlite_vec_blocked
        and not retrieval.backend_execution_allowed
        and chain.mgrep_blocked
        and chain.sqlite_vec_blocked
        and not chain.backend_execution_allowed
        and read_only
        and no_mutation_surface
    )

    return EvidenceBoundMemoryPhaseReadiness(
        total_items=chain.total_items,
        source_bound_items=chain.source_bound_items,
        provenance_bound_items=chain.provenance_bound_items,
        trace_bound_items=chain.trace_bound_items,
        citation_required_items=chain.citation_required_items,
        conflict_marked_items=chain.conflict_marked_items,
        dashboard_visible_items=chain.dashboard_visible_items,
        ready_items=chain.ready_items,
        retrieval_selected_sources=retrieval.selected_source_count,
        retrieval_evidence_items=retrieval.evidence_item_count,
        flow=_EXPECTED_EVIDENCE_BOUND_MEMORY_FLOW,
        retrieval_phase_ready=retrieval.phase_ready,
        evidence_source_chain_ready=evidence_source_chain_ready,
        source_bound_ready=source_bound_ready,
        provenance_bound_ready=provenance_bound_ready,
        trace_bound_ready=trace_bound_ready,
        citation_gate_ready=citation_gate_ready,
        conflict_gate_ready=conflict_gate_ready,
        dashboard_visibility_ready=dashboard_visibility_ready,
        mgrep_blocked=retrieval.mgrep_blocked and chain.mgrep_blocked,
        sqlite_vec_blocked=retrieval.sqlite_vec_blocked and chain.sqlite_vec_blocked,
        backend_execution_allowed=(
            retrieval.backend_execution_allowed or chain.backend_execution_allowed
        ),
        read_only=read_only,
        no_mutation_surface=no_mutation_surface,
        phase_ready=phase_ready,
    )


def build_evidence_bound_memory_phase_preview() -> Dict[str, object]:
    readiness = build_evidence_bound_memory_phase_readiness()

    return {
        "flow": readiness.flow,
        "total_items": readiness.total_items,
        "source_bound_items": readiness.source_bound_items,
        "provenance_bound_items": readiness.provenance_bound_items,
        "trace_bound_items": readiness.trace_bound_items,
        "citation_required_items": readiness.citation_required_items,
        "conflict_marked_items": readiness.conflict_marked_items,
        "dashboard_visible_items": readiness.dashboard_visible_items,
        "ready_items": readiness.ready_items,
        "retrieval_selected_sources": readiness.retrieval_selected_sources,
        "retrieval_evidence_items": readiness.retrieval_evidence_items,
        "retrieval_phase_ready": readiness.retrieval_phase_ready,
        "evidence_source_chain_ready": readiness.evidence_source_chain_ready,
        "source_bound_ready": readiness.source_bound_ready,
        "provenance_bound_ready": readiness.provenance_bound_ready,
        "trace_bound_ready": readiness.trace_bound_ready,
        "citation_gate_ready": readiness.citation_gate_ready,
        "conflict_gate_ready": readiness.conflict_gate_ready,
        "dashboard_visibility_ready": readiness.dashboard_visibility_ready,
        "mgrep_blocked": readiness.mgrep_blocked,
        "sqlite_vec_blocked": readiness.sqlite_vec_blocked,
        "backend_execution_allowed": readiness.backend_execution_allowed,
        "read_only": readiness.read_only,
        "no_mutation_surface": readiness.no_mutation_surface,
        "phase_ready": readiness.phase_ready,
        "preview_ready": True,
    }
