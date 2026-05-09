from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_router import (
    build_retrieval_route_plan,
)


_EXPECTED_TRACE_STEPS = (
    "query",
    "intent",
    "scope",
    "source_policy",
    "source_selection",
    "evidence_pack",
    "preview_trace",
)


def _ensure_non_empty_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple")
    if not values:
        raise ValueError(f"{field_name} must be non-empty")
    normalized = tuple(value.strip() for value in values if isinstance(value, str) and value.strip())
    if len(normalized) != len(values):
        raise ValueError(f"{field_name} must contain only non-empty strings")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalTrace:
    """Preview trace for retrieval orchestration."""

    trace_steps: tuple[str, ...]
    selected_source_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    policy_gate_passed: bool
    preview_trace_ready: bool

    def __post_init__(self) -> None:
        trace_steps = _ensure_non_empty_tuple(self.trace_steps, "trace_steps")
        selected_source_ids = _ensure_non_empty_tuple(
            self.selected_source_ids,
            "selected_source_ids",
        )
        evidence_ids = _ensure_non_empty_tuple(self.evidence_ids, "evidence_ids")

        if trace_steps != _EXPECTED_TRACE_STEPS:
            raise ValueError("trace_steps must match expected retrieval trace flow")

        policy_gate_passed = _ensure_bool(
            self.policy_gate_passed,
            "policy_gate_passed",
        )
        preview_trace_ready = _ensure_bool(
            self.preview_trace_ready,
            "preview_trace_ready",
        )

        if not policy_gate_passed:
            raise ValueError("policy_gate_passed must be True")
        if not preview_trace_ready:
            raise ValueError("preview_trace_ready must be True")

        object.__setattr__(self, "trace_steps", trace_steps)
        object.__setattr__(self, "selected_source_ids", selected_source_ids)
        object.__setattr__(self, "evidence_ids", evidence_ids)


def build_retrieval_trace() -> RetrievalTrace:
    route_plan = build_retrieval_route_plan()

    return RetrievalTrace(
        trace_steps=_EXPECTED_TRACE_STEPS,
        selected_source_ids=tuple(source.source_id for source in route_plan.selected_sources),
        evidence_ids=tuple(item.evidence_id for item in route_plan.evidence_pack.evidence_items),
        policy_gate_passed=route_plan.policy_gate_passed,
        preview_trace_ready=True,
    )


def build_retrieval_trace_preview() -> Dict[str, object]:
    trace = build_retrieval_trace()

    return {
        "trace_steps": trace.trace_steps,
        "selected_source_ids": trace.selected_source_ids,
        "evidence_ids": trace.evidence_ids,
        "policy_gate_passed": trace.policy_gate_passed,
        "preview_trace_ready": trace.preview_trace_ready,
    }
