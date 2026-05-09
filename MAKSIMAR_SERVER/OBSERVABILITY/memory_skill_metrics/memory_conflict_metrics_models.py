from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryConflictMetricSource = Literal[
    "core_evidence_memory",
    "server_evidence_source_chain",
    "core_server_evidence_binding",
]
MemoryConflictMetricSeverity = Literal["info", "warning", "critical"]

_METRIC_ID_PATTERN = re.compile(r"^msconflict_[a-z][a-z0-9_]*$")


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
class MemoryConflictMetricEntry:
    metric_id: str
    source_component: MemoryConflictMetricSource
    total_items: int
    conflict_items: int
    conflict_clear: bool
    resolution_required_items: int
    evidence_truth_ready: bool
    knowledge_graph_projection_only: bool
    read_only: bool
    event_severity: MemoryConflictMetricSeverity
    alert_emitted: bool
    metric_ready: bool
    description: str

    def __post_init__(self) -> None:
        metric_id = _ensure_non_empty_str(self.metric_id, "metric_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _METRIC_ID_PATTERN.fullmatch(metric_id):
            raise ValueError(f"Invalid metric_id: {metric_id}")

        for field_name in ("total_items", "conflict_items", "resolution_required_items"):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "conflict_clear",
            "evidence_truth_ready",
            "knowledge_graph_projection_only",
            "read_only",
            "alert_emitted",
            "metric_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.total_items <= 0:
            raise ValueError("total_items must be >= 1")
        if self.conflict_items != 0:
            raise ValueError("conflict_items must be 0")
        if not self.conflict_clear:
            raise ValueError("conflict_clear must be True")
        if self.resolution_required_items != 0:
            raise ValueError("resolution_required_items must be 0")
        if not self.evidence_truth_ready:
            raise ValueError("evidence_truth_ready must be True")
        if not self.knowledge_graph_projection_only:
            raise ValueError("knowledge_graph_projection_only must be True")
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
class MemoryConflictMetricsContract:
    total_entries: int
    ready_entries: int
    conflict_entries: int
    resolution_required_entries: int
    evidence_truth_ready_entries: int
    knowledge_graph_projection_entries: int
    read_only_entries: int
    entries: tuple[MemoryConflictMetricEntry, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        if self.total_entries <= 0:
            raise ValueError("total_entries must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.metric_ready)
        computed_conflict = sum(1 for entry in self.entries if entry.conflict_items > 0)
        computed_resolution = sum(
            1 for entry in self.entries if entry.resolution_required_items > 0
        )
        computed_truth = sum(1 for entry in self.entries if entry.evidence_truth_ready)
        computed_projection = sum(
            1 for entry in self.entries if entry.knowledge_graph_projection_only
        )
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_entries != computed_ready:
            raise ValueError("ready_entries must match computed count")
        if self.conflict_entries != computed_conflict:
            raise ValueError("conflict_entries must match computed count")
        if self.resolution_required_entries != computed_resolution:
            raise ValueError("resolution_required_entries must match computed count")
        if self.evidence_truth_ready_entries != computed_truth:
            raise ValueError("evidence_truth_ready_entries must match computed count")
        if self.knowledge_graph_projection_entries != computed_projection:
            raise ValueError("knowledge_graph_projection_entries must match computed count")
        if self.read_only_entries != computed_read_only:
            raise ValueError("read_only_entries must match computed count")

        if self.ready_entries != self.total_entries:
            raise ValueError("all conflict metric entries must be ready")
        if self.conflict_entries != 0:
            raise ValueError("conflict_entries must be 0")
        if self.resolution_required_entries != 0:
            raise ValueError("resolution_required_entries must be 0")
        if self.evidence_truth_ready_entries != self.total_entries:
            raise ValueError("all entries must confirm evidence truth")
        if self.knowledge_graph_projection_entries != self.total_entries:
            raise ValueError("all entries must confirm projection-only graph")
        if self.read_only_entries != self.total_entries:
            raise ValueError("all conflict metric entries must be read-only")

        metric_ids = tuple(entry.metric_id for entry in self.entries)
        if len(set(metric_ids)) != len(metric_ids):
            raise ValueError("duplicate metric_id values detected")


def build_memory_conflict_metrics_contract() -> MemoryConflictMetricsContract:
    from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_evidence_memory_core_binding_contract,
        build_evidence_source_chain_contract,
    )

    core = build_evidence_memory_contract()
    source_chain = build_evidence_source_chain_contract()
    core_binding = build_evidence_memory_core_binding_contract()

    entries = (
        MemoryConflictMetricEntry(
            metric_id="msconflict_core_evidence_memory",
            source_component="core_evidence_memory",
            total_items=core.total_records,
            conflict_items=core.conflict_detected_records,
            conflict_clear=core.conflict_detected_records == 0,
            resolution_required_items=0,
            evidence_truth_ready=core.memory_truth_records == core.total_records,
            knowledge_graph_projection_only=(
                core.knowledge_graph_projection_records == core.total_records
            ),
            read_only=core.read_only_records == core.total_records,
            event_severity="info",
            alert_emitted=False,
            metric_ready=core.ready_records == core.total_records,
            description="CORE evidence memory conflict observability metric.",
        ),
        MemoryConflictMetricEntry(
            metric_id="msconflict_server_evidence_source_chain",
            source_component="server_evidence_source_chain",
            total_items=source_chain.total_items,
            conflict_items=source_chain.conflict_marked_items,
            conflict_clear=source_chain.conflict_marked_items == 0,
            resolution_required_items=0,
            evidence_truth_ready=source_chain.ready_items == source_chain.total_items,
            knowledge_graph_projection_only=True,
            read_only=True,
            event_severity="info",
            alert_emitted=False,
            metric_ready=source_chain.ready_items == source_chain.total_items,
            description="SERVER evidence source chain conflict observability metric.",
        ),
        MemoryConflictMetricEntry(
            metric_id="msconflict_core_server_evidence_binding",
            source_component="core_server_evidence_binding",
            total_items=core_binding.total_bindings,
            conflict_items=0,
            conflict_clear=core_binding.conflict_clear_bindings == core_binding.total_bindings,
            resolution_required_items=0,
            evidence_truth_ready=(
                core_binding.memory_truth_bindings == core_binding.total_bindings
            ),
            knowledge_graph_projection_only=(
                core_binding.knowledge_graph_projection_bindings
                == core_binding.total_bindings
            ),
            read_only=core_binding.read_only_bindings == core_binding.total_bindings,
            event_severity="info",
            alert_emitted=False,
            metric_ready=core_binding.ready_bindings == core_binding.total_bindings,
            description="CORE/SERVER evidence binding conflict observability metric.",
        ),
    )

    return MemoryConflictMetricsContract(
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.metric_ready),
        conflict_entries=sum(1 for entry in entries if entry.conflict_items > 0),
        resolution_required_entries=sum(
            1 for entry in entries if entry.resolution_required_items > 0
        ),
        evidence_truth_ready_entries=sum(
            1 for entry in entries if entry.evidence_truth_ready
        ),
        knowledge_graph_projection_entries=sum(
            1 for entry in entries if entry.knowledge_graph_projection_only
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
