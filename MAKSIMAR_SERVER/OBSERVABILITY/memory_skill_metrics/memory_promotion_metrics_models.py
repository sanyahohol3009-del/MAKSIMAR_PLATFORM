from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryPromotionMetricSource = Literal[
    "core_evidence_memory",
    "server_evidence_readiness",
    "core_server_binding",
]
MemoryPromotionMetricSeverity = Literal["info", "warning", "critical"]

_METRIC_ID_PATTERN = re.compile(r"^mspromotion_[a-z][a-z0-9_]*$")


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
class MemoryPromotionMetricEntry:
    metric_id: str
    source_component: MemoryPromotionMetricSource
    candidate_items: int
    promotion_ready_items: int
    auto_promotion_allowed: bool
    approval_required: bool
    conflict_clear: bool
    citation_ready: bool
    read_only: bool
    event_severity: MemoryPromotionMetricSeverity
    alert_emitted: bool
    metric_ready: bool
    description: str

    def __post_init__(self) -> None:
        metric_id = _ensure_non_empty_str(self.metric_id, "metric_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _METRIC_ID_PATTERN.fullmatch(metric_id):
            raise ValueError(f"Invalid metric_id: {metric_id}")

        for field_name in ("candidate_items", "promotion_ready_items"):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "auto_promotion_allowed",
            "approval_required",
            "conflict_clear",
            "citation_ready",
            "read_only",
            "alert_emitted",
            "metric_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.candidate_items <= 0:
            raise ValueError("candidate_items must be >= 1")
        if self.promotion_ready_items != self.candidate_items:
            raise ValueError("promotion_ready_items must match candidate_items")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.conflict_clear:
            raise ValueError("conflict_clear must be True")
        if not self.citation_ready:
            raise ValueError("citation_ready must be True")
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
class MemoryPromotionMetricsContract:
    total_entries: int
    ready_entries: int
    auto_promotion_allowed_entries: int
    approval_required_entries: int
    conflict_clear_entries: int
    citation_ready_entries: int
    read_only_entries: int
    entries: tuple[MemoryPromotionMetricEntry, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        if self.total_entries <= 0:
            raise ValueError("total_entries must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.metric_ready)
        computed_auto = sum(1 for entry in self.entries if entry.auto_promotion_allowed)
        computed_approval = sum(1 for entry in self.entries if entry.approval_required)
        computed_conflict = sum(1 for entry in self.entries if entry.conflict_clear)
        computed_citation = sum(1 for entry in self.entries if entry.citation_ready)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_entries != computed_ready:
            raise ValueError("ready_entries must match computed count")
        if self.auto_promotion_allowed_entries != computed_auto:
            raise ValueError("auto_promotion_allowed_entries must match computed count")
        if self.approval_required_entries != computed_approval:
            raise ValueError("approval_required_entries must match computed count")
        if self.conflict_clear_entries != computed_conflict:
            raise ValueError("conflict_clear_entries must match computed count")
        if self.citation_ready_entries != computed_citation:
            raise ValueError("citation_ready_entries must match computed count")
        if self.read_only_entries != computed_read_only:
            raise ValueError("read_only_entries must match computed count")

        if self.ready_entries != self.total_entries:
            raise ValueError("all promotion metric entries must be ready")
        if self.auto_promotion_allowed_entries != 0:
            raise ValueError("auto promotion must stay disabled")
        if self.approval_required_entries != self.total_entries:
            raise ValueError("all promotion metrics must require approval")
        if self.conflict_clear_entries != self.total_entries:
            raise ValueError("all promotion metrics must be conflict-clear")
        if self.citation_ready_entries != self.total_entries:
            raise ValueError("all promotion metrics must be citation-ready")
        if self.read_only_entries != self.total_entries:
            raise ValueError("all promotion metrics must be read-only")

        metric_ids = tuple(entry.metric_id for entry in self.entries)
        if len(set(metric_ids)) != len(metric_ids):
            raise ValueError("duplicate metric_id values detected")


def build_memory_promotion_metrics_contract() -> MemoryPromotionMetricsContract:
    from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_contract
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_evidence_bound_memory_phase_readiness,
        build_evidence_memory_core_binding_contract,
    )

    core = build_evidence_memory_contract()
    server_readiness = build_evidence_bound_memory_phase_readiness()
    core_binding = build_evidence_memory_core_binding_contract()

    entries = (
        MemoryPromotionMetricEntry(
            metric_id="mspromotion_core_evidence_memory",
            source_component="core_evidence_memory",
            candidate_items=core.total_records,
            promotion_ready_items=core.ready_records,
            auto_promotion_allowed=False,
            approval_required=True,
            conflict_clear=core.conflict_detected_records == 0,
            citation_ready=core.citation_required_records == core.total_records,
            read_only=core.read_only_records == core.total_records,
            event_severity="info",
            alert_emitted=False,
            metric_ready=core.ready_records == core.total_records,
            description="CORE evidence memory promotion observability metric.",
        ),
        MemoryPromotionMetricEntry(
            metric_id="mspromotion_server_evidence_readiness",
            source_component="server_evidence_readiness",
            candidate_items=server_readiness.total_items,
            promotion_ready_items=server_readiness.ready_items,
            auto_promotion_allowed=False,
            approval_required=True,
            conflict_clear=server_readiness.conflict_gate_ready,
            citation_ready=server_readiness.citation_gate_ready,
            read_only=server_readiness.read_only,
            event_severity="info",
            alert_emitted=False,
            metric_ready=server_readiness.phase_ready,
            description="SERVER evidence readiness promotion observability metric.",
        ),
        MemoryPromotionMetricEntry(
            metric_id="mspromotion_core_server_binding",
            source_component="core_server_binding",
            candidate_items=core_binding.total_bindings,
            promotion_ready_items=core_binding.ready_bindings,
            auto_promotion_allowed=False,
            approval_required=True,
            conflict_clear=core_binding.conflict_clear_bindings == core_binding.total_bindings,
            citation_ready=core_binding.citation_required_bindings == core_binding.total_bindings,
            read_only=core_binding.read_only_bindings == core_binding.total_bindings,
            event_severity="info",
            alert_emitted=False,
            metric_ready=core_binding.ready_bindings == core_binding.total_bindings,
            description="CORE/SERVER binding promotion observability metric.",
        ),
    )

    return MemoryPromotionMetricsContract(
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.metric_ready),
        auto_promotion_allowed_entries=sum(
            1 for entry in entries if entry.auto_promotion_allowed
        ),
        approval_required_entries=sum(1 for entry in entries if entry.approval_required),
        conflict_clear_entries=sum(1 for entry in entries if entry.conflict_clear),
        citation_ready_entries=sum(1 for entry in entries if entry.citation_ready),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
