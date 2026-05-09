from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryRetrievalMetricSource = Literal[
    "retrieval_phase",
    "evidence_source_chain",
    "core_evidence_binding",
]
MemoryRetrievalMetricSeverity = Literal["info", "warning", "critical"]

_METRIC_ID_PATTERN = re.compile(r"^msretrieval_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


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
class MemoryRetrievalMetricEntry:
    metric_id: str
    source_component: MemoryRetrievalMetricSource
    selected_source_count: int
    evidence_item_count: int
    ready_item_count: int
    conflict_item_count: int
    trace_ready: bool
    policy_gate_ready: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    backend_execution_allowed: bool
    read_only: bool
    event_severity: MemoryRetrievalMetricSeverity
    alert_emitted: bool
    metric_ready: bool
    description: str

    def __post_init__(self) -> None:
        metric_id = _ensure_non_empty_str(self.metric_id, "metric_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _METRIC_ID_PATTERN.fullmatch(metric_id):
            raise ValueError(f"Invalid metric_id: {metric_id}")

        for field_name in (
            "selected_source_count",
            "evidence_item_count",
            "ready_item_count",
            "conflict_item_count",
        ):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "trace_ready",
            "policy_gate_ready",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "backend_execution_allowed",
            "read_only",
            "alert_emitted",
            "metric_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.evidence_item_count <= 0:
            raise ValueError("evidence_item_count must be >= 1")
        if self.ready_item_count != self.evidence_item_count:
            raise ValueError("ready_item_count must match evidence_item_count")
        if self.conflict_item_count != 0:
            raise ValueError("conflict_item_count must be 0")
        if not self.trace_ready:
            raise ValueError("trace_ready must be True")
        if not self.policy_gate_ready:
            raise ValueError("policy_gate_ready must be True")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.event_severity != "info":
            raise ValueError("event_severity must be info")
        if self.alert_emitted:
            raise ValueError("alert_emitted must be False")
        if not self.metric_ready:
            raise ValueError("metric_ready must be True")

        object.__setattr__(self, "metric_id", metric_id)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class MemoryRetrievalMetricsContract:
    total_entries: int
    ready_entries: int
    conflict_entries: int
    backend_execution_allowed_entries: int
    mgrep_blocked_entries: int
    sqlite_vec_blocked_entries: int
    read_only_entries: int
    entries: tuple[MemoryRetrievalMetricEntry, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        if self.total_entries <= 0:
            raise ValueError("total_entries must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.metric_ready)
        computed_conflict = sum(1 for entry in self.entries if entry.conflict_item_count > 0)
        computed_backend = sum(1 for entry in self.entries if entry.backend_execution_allowed)
        computed_mgrep = sum(1 for entry in self.entries if entry.mgrep_blocked)
        computed_sqlite = sum(1 for entry in self.entries if entry.sqlite_vec_blocked)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_entries != computed_ready:
            raise ValueError("ready_entries must match computed count")
        if self.conflict_entries != computed_conflict:
            raise ValueError("conflict_entries must match computed count")
        if self.backend_execution_allowed_entries != computed_backend:
            raise ValueError("backend_execution_allowed_entries must match computed count")
        if self.mgrep_blocked_entries != computed_mgrep:
            raise ValueError("mgrep_blocked_entries must match computed count")
        if self.sqlite_vec_blocked_entries != computed_sqlite:
            raise ValueError("sqlite_vec_blocked_entries must match computed count")
        if self.read_only_entries != computed_read_only:
            raise ValueError("read_only_entries must match computed count")

        if self.ready_entries != self.total_entries:
            raise ValueError("all retrieval metric entries must be ready")
        if self.conflict_entries != 0:
            raise ValueError("retrieval metric conflict_entries must be 0")
        if self.backend_execution_allowed_entries != 0:
            raise ValueError("backend execution must remain disabled")
        if self.mgrep_blocked_entries != self.total_entries:
            raise ValueError("mgrep must be blocked for all retrieval metrics")
        if self.sqlite_vec_blocked_entries != self.total_entries:
            raise ValueError("sqlite-vec must be blocked for all retrieval metrics")
        if self.read_only_entries != self.total_entries:
            raise ValueError("all retrieval metric entries must be read-only")

        metric_ids = tuple(entry.metric_id for entry in self.entries)
        if len(set(metric_ids)) != len(metric_ids):
            raise ValueError("duplicate metric_id values detected")


def build_memory_retrieval_metrics_contract() -> MemoryRetrievalMetricsContract:
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_evidence_bound_memory_phase_readiness,
        build_evidence_memory_core_binding_contract,
        build_evidence_source_chain_contract,
        build_retrieval_phase_readiness,
    )

    retrieval = build_retrieval_phase_readiness()
    evidence_readiness = build_evidence_bound_memory_phase_readiness()
    source_chain = build_evidence_source_chain_contract()
    core_binding = build_evidence_memory_core_binding_contract()

    entries = (
        MemoryRetrievalMetricEntry(
            metric_id="msretrieval_retrieval_phase",
            source_component="retrieval_phase",
            selected_source_count=retrieval.selected_source_count,
            evidence_item_count=retrieval.evidence_item_count,
            ready_item_count=retrieval.evidence_item_count,
            conflict_item_count=0,
            trace_ready=retrieval.trace_ready,
            policy_gate_ready=retrieval.backend_policy_ready,
            mgrep_blocked=retrieval.mgrep_blocked,
            sqlite_vec_blocked=retrieval.sqlite_vec_blocked,
            backend_execution_allowed=retrieval.backend_execution_allowed,
            read_only=True,
            event_severity="info",
            alert_emitted=False,
            metric_ready=retrieval.phase_ready,
            description="Retrieval phase observability metric.",
        ),
        MemoryRetrievalMetricEntry(
            metric_id="msretrieval_evidence_source_chain",
            source_component="evidence_source_chain",
            selected_source_count=evidence_readiness.retrieval_selected_sources,
            evidence_item_count=source_chain.total_items,
            ready_item_count=source_chain.ready_items,
            conflict_item_count=source_chain.conflict_marked_items,
            trace_ready=evidence_readiness.trace_bound_ready,
            policy_gate_ready=evidence_readiness.retrieval_phase_ready,
            mgrep_blocked=evidence_readiness.mgrep_blocked,
            sqlite_vec_blocked=evidence_readiness.sqlite_vec_blocked,
            backend_execution_allowed=evidence_readiness.backend_execution_allowed,
            read_only=evidence_readiness.read_only,
            event_severity="info",
            alert_emitted=False,
            metric_ready=evidence_readiness.phase_ready,
            description="Evidence source chain observability metric.",
        ),
        MemoryRetrievalMetricEntry(
            metric_id="msretrieval_core_evidence_binding",
            source_component="core_evidence_binding",
            selected_source_count=evidence_readiness.retrieval_selected_sources,
            evidence_item_count=core_binding.total_bindings,
            ready_item_count=core_binding.ready_bindings,
            conflict_item_count=0,
            trace_ready=core_binding.server_phase_ready,
            policy_gate_ready=core_binding.server_phase_ready,
            mgrep_blocked=core_binding.mgrep_blocked,
            sqlite_vec_blocked=core_binding.sqlite_vec_blocked,
            backend_execution_allowed=core_binding.backend_execution_allowed,
            read_only=core_binding.read_only_bindings == core_binding.total_bindings,
            event_severity="info",
            alert_emitted=False,
            metric_ready=core_binding.ready_bindings == core_binding.total_bindings,
            description="CORE/SERVER evidence binding observability metric.",
        ),
    )

    return MemoryRetrievalMetricsContract(
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.metric_ready),
        conflict_entries=sum(1 for entry in entries if entry.conflict_item_count > 0),
        backend_execution_allowed_entries=sum(
            1 for entry in entries if entry.backend_execution_allowed
        ),
        mgrep_blocked_entries=sum(1 for entry in entries if entry.mgrep_blocked),
        sqlite_vec_blocked_entries=sum(1 for entry in entries if entry.sqlite_vec_blocked),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
