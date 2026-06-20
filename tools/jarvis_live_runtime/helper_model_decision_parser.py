from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_profiles,
)
from MAKSIMAR_CORE_LIB.swarm_coordination.swarm_agent_role_contract import SWARM_AGENT_ROLES


HELPER_RISK_CLASSES = ("read_only", "safe_direct", "risk_gate")
_REQUIRED_FIELDS = (
    "intent_family",
    "task_complexity",
    "selected_model_role_id",
    "selected_tools",
    "selected_agent_roles",
    "risk_class",
    "workflow_steps",
    "confidence",
    "reason",
)


def _model_profiles() -> dict[str, dict[str, Any]]:
    return {profile.role_id: profile.to_read_model() for profile in build_jarvis_live_runtime_model_role_profiles()}


def _require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    normalized_items: list[str] = []
    for item in value:
        if isinstance(item, dict) and field_name == "workflow_steps":
            step_name = item.get("step_name") or item.get("action") or item.get("name")
            normalized_items.append(_require_non_empty_string(step_name, field_name))
            continue
        normalized_items.append(_require_non_empty_string(item, field_name))
    normalized = tuple(normalized_items)
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence must be numeric") from exc

    # Helper models sometimes return percent scale: 90 -> 0.90.
    # But values just above 1.0, like 1.2 in tests, mean overconfident float and clamp to 1.0.
    if confidence >= 2.0 and confidence <= 100.0:
        confidence = confidence / 100.0
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence



@dataclass(frozen=True, slots=True)
class HelperModelDecision:
    intent_family: str
    task_complexity: str
    selected_model_role_id: str
    selected_model_id: str
    selected_tools: tuple[str, ...]
    selected_agent_roles: tuple[str, ...]
    risk_class: str
    workflow_steps: tuple[str, ...]
    confidence: float
    reason: str
    heavy_model_selected: bool
    parallel_heavy_model_allowed: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "intent_family": self.intent_family,
            "task_complexity": self.task_complexity,
            "selected_model_role_id": self.selected_model_role_id,
            "selected_model_id": self.selected_model_id,
            "selected_tools": self.selected_tools,
            "selected_agent_roles": self.selected_agent_roles,
            "risk_class": self.risk_class,
            "workflow_steps": self.workflow_steps,
            "confidence": self.confidence,
            "reason": self.reason,
            "heavy_model_selected": self.heavy_model_selected,
            "parallel_heavy_model_allowed": self.parallel_heavy_model_allowed,
        }


def parse_helper_model_decision_payload(payload: dict[str, Any] | str) -> HelperModelDecision:
    if isinstance(payload, str):
        try:
            raw = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ValueError("helper decision must be valid JSON") from exc
    elif isinstance(payload, dict):
        raw = dict(payload)
    else:
        raise TypeError("payload must be dict or JSON string")

    missing = tuple(field for field in _REQUIRED_FIELDS if field not in raw)
    if missing:
        raise ValueError(f"missing helper decision fields: {missing!r}")

    profiles = _model_profiles()
    intent_family = _require_non_empty_string(raw["intent_family"], "intent_family")
    task_complexity = _require_non_empty_string(raw["task_complexity"], "task_complexity")
    task_complexity = {
        "low": "light",
        "simple": "light",
        "normal": "medium",
        "complex": "heavy",
        "high": "heavy",
        "advanced": "heavy",
        "severe": "heavy",
        "complicated": "heavy",
    }.get(task_complexity.casefold(), task_complexity)
    if task_complexity not in {"light", "medium", "heavy"}:
        raise ValueError(f"unknown task_complexity: {task_complexity!r}")
    selected_model_role_id = _require_non_empty_string(raw["selected_model_role_id"], "selected_model_role_id")
    if selected_model_role_id not in profiles:
        raise ValueError(f"unknown selected_model_role_id: {selected_model_role_id!r}")
    selected_tools = _require_string_list(raw["selected_tools"], "selected_tools")
    selected_agent_roles = _require_string_list(raw["selected_agent_roles"], "selected_agent_roles")
    unknown_agent_roles = tuple(role for role in selected_agent_roles if role not in SWARM_AGENT_ROLES)
    if unknown_agent_roles:
        raise ValueError(f"unknown selected_agent_roles: {unknown_agent_roles!r}")
    risk_class = _require_non_empty_string(raw["risk_class"], "risk_class")
    if risk_class not in HELPER_RISK_CLASSES:
        raise ValueError(f"unknown risk_class: {risk_class!r}")
    workflow_steps = _require_string_list(raw["workflow_steps"], "workflow_steps")
    reason = _require_non_empty_string(raw["reason"], "reason")
    confidence = _normalize_confidence(raw["confidence"])
    profile = profiles[selected_model_role_id]
    heavy = bool(profile["role_id"] == "heavy_coder_model" or profile.get("exclusive_gpu") is True)
    return HelperModelDecision(
        intent_family=intent_family,
        task_complexity=task_complexity,
        selected_model_role_id=selected_model_role_id,
        selected_model_id=str(profile["model_id"]),
        selected_tools=selected_tools,
        selected_agent_roles=selected_agent_roles,
        risk_class=risk_class,
        workflow_steps=workflow_steps,
        confidence=confidence,
        reason=reason,
        heavy_model_selected=heavy,
        parallel_heavy_model_allowed=False if heavy else True,
    )
