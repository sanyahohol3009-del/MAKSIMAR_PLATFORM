from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryAdapterSelectionMetricSource = Literal[
    "skill_adapter_registry",
    "retrieval_backend_policy",
]
MemoryAdapterSelectionMetricSeverity = Literal["info", "warning", "critical"]

_METRIC_ID_PATTERN = re.compile(r"^msadapter_[a-z][a-z0-9_]*$")


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
class MemoryAdapterSelectionMetricEntry:
    metric_id: str
    source_component: MemoryAdapterSelectionMetricSource
    total_adapters: int
    active_adapters: int
    sandboxed_adapters: int
    engine_adapter_required_items: int
    blocked_backend_items: int
    backend_execution_allowed: bool
    mgrep_blocked: bool
    sqlite_vec_blocked: bool
    policy_gate_ready: bool
    read_only: bool
    event_severity: MemoryAdapterSelectionMetricSeverity
    alert_emitted: bool
    metric_ready: bool
    description: str

    def __post_init__(self) -> None:
        metric_id = _ensure_non_empty_str(self.metric_id, "metric_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _METRIC_ID_PATTERN.fullmatch(metric_id):
            raise ValueError(f"Invalid metric_id: {metric_id}")

        for field_name in (
            "total_adapters",
            "active_adapters",
            "sandboxed_adapters",
            "engine_adapter_required_items",
            "blocked_backend_items",
        ):
            _ensure_non_negative_int(getattr(self, field_name), field_name)

        for field_name in (
            "backend_execution_allowed",
            "mgrep_blocked",
            "sqlite_vec_blocked",
            "policy_gate_ready",
            "read_only",
            "alert_emitted",
            "metric_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.total_adapters <= 0:
            raise ValueError("total_adapters must be >= 1")
        if self.active_adapters <= 0:
            raise ValueError("active_adapters must be >= 1")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")
        if not self.mgrep_blocked:
            raise ValueError("mgrep_blocked must be True")
        if not self.sqlite_vec_blocked:
            raise ValueError("sqlite_vec_blocked must be True")
        if not self.policy_gate_ready:
            raise ValueError("policy_gate_ready must be True")
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
class MemoryAdapterSelectionMetricsContract:
    total_entries: int
    ready_entries: int
    backend_execution_allowed_entries: int
    policy_gate_ready_entries: int
    mgrep_blocked_entries: int
    sqlite_vec_blocked_entries: int
    read_only_entries: int
    entries: tuple[MemoryAdapterSelectionMetricEntry, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        if self.total_entries <= 0:
            raise ValueError("total_entries must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.metric_ready)
        computed_backend = sum(1 for entry in self.entries if entry.backend_execution_allowed)
        computed_policy = sum(1 for entry in self.entries if entry.policy_gate_ready)
        computed_mgrep = sum(1 for entry in self.entries if entry.mgrep_blocked)
        computed_sqlite = sum(1 for entry in self.entries if entry.sqlite_vec_blocked)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        if self.ready_entries != computed_ready:
            raise ValueError("ready_entries must match computed count")
        if self.backend_execution_allowed_entries != computed_backend:
            raise ValueError("backend_execution_allowed_entries must match computed count")
        if self.policy_gate_ready_entries != computed_policy:
            raise ValueError("policy_gate_ready_entries must match computed count")
        if self.mgrep_blocked_entries != computed_mgrep:
            raise ValueError("mgrep_blocked_entries must match computed count")
        if self.sqlite_vec_blocked_entries != computed_sqlite:
            raise ValueError("sqlite_vec_blocked_entries must match computed count")
        if self.read_only_entries != computed_read_only:
            raise ValueError("read_only_entries must match computed count")

        if self.ready_entries != self.total_entries:
            raise ValueError("all adapter selection metrics must be ready")
        if self.backend_execution_allowed_entries != 0:
            raise ValueError("backend execution must remain disabled")
        if self.policy_gate_ready_entries != self.total_entries:
            raise ValueError("all adapter metrics must be policy-gate ready")
        if self.mgrep_blocked_entries != self.total_entries:
            raise ValueError("mgrep must be blocked in all adapter metrics")
        if self.sqlite_vec_blocked_entries != self.total_entries:
            raise ValueError("sqlite-vec must be blocked in all adapter metrics")
        if self.read_only_entries != self.total_entries:
            raise ValueError("all adapter metrics must be read-only")


def build_memory_adapter_selection_metrics_contract() -> MemoryAdapterSelectionMetricsContract:
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_retrieval_backend_policy_gate,
    )
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
        build_skill_adapter_registry_contract,
    )

    skill_registry = build_skill_adapter_registry_contract()
    backend_policy = build_retrieval_backend_policy_gate()

    entries = (
        MemoryAdapterSelectionMetricEntry(
            metric_id="msadapter_skill_adapter_registry",
            source_component="skill_adapter_registry",
            total_adapters=skill_registry.total_entries,
            active_adapters=skill_registry.active_entries,
            sandboxed_adapters=skill_registry.sandboxed_entries,
            engine_adapter_required_items=skill_registry.engine_adapter_entries,
            blocked_backend_items=backend_policy.blocked_backends,
            backend_execution_allowed=backend_policy.backend_execution_allowed,
            mgrep_blocked=backend_policy.mgrep_blocked,
            sqlite_vec_blocked=backend_policy.sqlite_vec_blocked,
            policy_gate_ready=backend_policy.policy_gate_ready,
            read_only=True,
            event_severity="info",
            alert_emitted=False,
            metric_ready=skill_registry.active_entries == skill_registry.total_entries
            and backend_policy.policy_gate_ready,
            description="Skill adapter registry selection observability metric.",
        ),
        MemoryAdapterSelectionMetricEntry(
            metric_id="msadapter_retrieval_backend_policy",
            source_component="retrieval_backend_policy",
            total_adapters=backend_policy.total_backends,
            active_adapters=backend_policy.approved_backends,
            sandboxed_adapters=backend_policy.adapter_required_backends,
            engine_adapter_required_items=backend_policy.adapter_required_backends,
            blocked_backend_items=backend_policy.blocked_backends,
            backend_execution_allowed=backend_policy.backend_execution_allowed,
            mgrep_blocked=backend_policy.mgrep_blocked,
            sqlite_vec_blocked=backend_policy.sqlite_vec_blocked,
            policy_gate_ready=backend_policy.policy_gate_ready,
            read_only=True,
            event_severity="info",
            alert_emitted=False,
            metric_ready=backend_policy.policy_gate_ready,
            description="Retrieval backend policy selection observability metric.",
        ),
    )

    return MemoryAdapterSelectionMetricsContract(
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.metric_ready),
        backend_execution_allowed_entries=sum(
            1 for entry in entries if entry.backend_execution_allowed
        ),
        policy_gate_ready_entries=sum(1 for entry in entries if entry.policy_gate_ready),
        mgrep_blocked_entries=sum(1 for entry in entries if entry.mgrep_blocked),
        sqlite_vec_blocked_entries=sum(1 for entry in entries if entry.sqlite_vec_blocked),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
