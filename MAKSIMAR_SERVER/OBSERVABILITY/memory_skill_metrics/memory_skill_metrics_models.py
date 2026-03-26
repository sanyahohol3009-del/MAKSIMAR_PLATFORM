from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemorySkillMetricSource = Literal[
    "memory_registry",
    "skill_adapter_registry",
    "ai_router_binding",
]

MemorySkillMetricSeverity = Literal[
    "info",
    "warning",
    "critical",
]


_METRIC_ID_PATTERN = re.compile(r"^msmetric_[a-z][a-z0-9_]*$")
_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_SKILL_ID_PATTERN = re.compile(r"^skill_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_WORKER_ID_PATTERN = re.compile(r"^worker_[a-z][a-z0-9_]*_001$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_ROUTE_REQUEST_ID_PATTERN = re.compile(r"^route_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class MemorySkillMetricEntry:
    """Canonical observability metric entry for memory and skill bindings."""

    metric_id: str
    source_component: MemorySkillMetricSource
    module_slug: str
    linked_memory_tier_id: str
    linked_skill_id: str
    linked_worker_id: str
    linked_panel_id: str
    route_request_id: str
    active: bool
    explanation_available: bool
    policy_compatible: bool
    multilingual_ready: bool
    event_severity: MemorySkillMetricSeverity
    alert_emitted: bool
    description: str

    def __post_init__(self) -> None:
        """Validate memory/skill metric invariants."""
        if not _METRIC_ID_PATTERN.fullmatch(self.metric_id):
            raise ValueError(f"Invalid metric_id: {self.metric_id}")

        if not self.module_slug.strip():
            raise ValueError("module_slug must not be empty")

        if not _PANEL_ID_PATTERN.fullmatch(self.linked_panel_id):
            raise ValueError(f"Invalid linked_panel_id: {self.linked_panel_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.metric_id}")

        if not self.active:
            raise ValueError(f"metric target must be active: {self.metric_id}")

        if not self.explanation_available:
            raise ValueError(
                f"memory/skill observability metric must be explanation-ready: {self.metric_id}"
            )

        if not self.policy_compatible:
            raise ValueError(
                f"memory/skill observability metric must be policy-compatible: {self.metric_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"memory/skill observability metric must be multilingual-ready: {self.metric_id}"
            )

        if self.event_severity != "info":
            raise ValueError(
                f"memory/skill observability metric must use severity='info': {self.metric_id}"
            )

        if self.alert_emitted:
            raise ValueError(
                f"memory/skill observability metric must not emit alerts: {self.metric_id}"
            )

        if self.source_component == "memory_registry":
            if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.linked_memory_tier_id):
                raise ValueError(
                    f"memory_registry metric must define linked_memory_tier_id: {self.metric_id}"
                )
            if self.linked_skill_id != "":
                raise ValueError(
                    f"memory_registry metric must not define linked_skill_id: {self.metric_id}"
                )
            if self.linked_worker_id != "":
                raise ValueError(
                    f"memory_registry metric must not define linked_worker_id: {self.metric_id}"
                )
            if self.route_request_id != "":
                raise ValueError(
                    f"memory_registry metric must not define route_request_id: {self.metric_id}"
                )

        if self.source_component == "skill_adapter_registry":
            if self.linked_memory_tier_id != "":
                raise ValueError(
                    f"skill_adapter_registry metric must not define linked_memory_tier_id: {self.metric_id}"
                )
            if not _SKILL_ID_PATTERN.fullmatch(self.linked_skill_id):
                raise ValueError(
                    f"skill_adapter_registry metric must define linked_skill_id: {self.metric_id}"
                )
            if not _WORKER_ID_PATTERN.fullmatch(self.linked_worker_id):
                raise ValueError(
                    f"skill_adapter_registry metric must define linked_worker_id: {self.metric_id}"
                )
            if self.route_request_id != "":
                raise ValueError(
                    f"skill_adapter_registry metric must not define route_request_id: {self.metric_id}"
                )

        if self.source_component == "ai_router_binding":
            if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.linked_memory_tier_id):
                raise ValueError(
                    f"ai_router_binding metric must define linked_memory_tier_id: {self.metric_id}"
                )
            if not _SKILL_ID_PATTERN.fullmatch(self.linked_skill_id):
                raise ValueError(
                    f"ai_router_binding metric must define linked_skill_id: {self.metric_id}"
                )
            if not _WORKER_ID_PATTERN.fullmatch(self.linked_worker_id):
                raise ValueError(
                    f"ai_router_binding metric must define linked_worker_id: {self.metric_id}"
                )
            if not _ROUTE_REQUEST_ID_PATTERN.fullmatch(self.route_request_id):
                raise ValueError(
                    f"ai_router_binding metric must define route_request_id: {self.metric_id}"
                )


@dataclass(frozen=True, slots=True)
class MemorySkillMetricsContract:
    """Unified observability contract for memory and skill metrics."""

    total_entries: int
    active_entries: int
    explanation_ready_entries: int
    policy_compatible_entries: int
    router_binding_entries: int
    entries: tuple[MemorySkillMetricEntry, ...]

    def __post_init__(self) -> None:
        """Validate memory/skill metrics contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        explanation_ready_entries = sum(
            1 for entry in self.entries if entry.explanation_available
        )
        policy_compatible_entries = sum(
            1 for entry in self.entries if entry.policy_compatible
        )
        router_binding_entries = sum(
            1 for entry in self.entries if entry.source_component == "ai_router_binding"
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.explanation_ready_entries != explanation_ready_entries:
            raise ValueError("explanation_ready_entries must match computed count")

        if self.policy_compatible_entries != policy_compatible_entries:
            raise ValueError("policy_compatible_entries must match computed count")

        if self.router_binding_entries != router_binding_entries:
            raise ValueError("router_binding_entries must match computed count")

        metric_ids = tuple(entry.metric_id for entry in self.entries)
        if len(set(metric_ids)) != len(metric_ids):
            raise ValueError("Duplicate metric_id values detected")
