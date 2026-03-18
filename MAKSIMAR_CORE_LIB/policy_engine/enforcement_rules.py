from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.policy_engine.enforcement_models import EnforcementReason


def _as_bool(value: Any) -> bool | None:
    """Convert explicit booleans only."""
    if isinstance(value, bool):
        return value
    return None


def evaluate_approval_required(payload: dict[str, Any]) -> list[EnforcementReason]:
    """Evaluate whether policy requires explicit approval.

    Args:
        payload: Policy payload.

    Returns:
        Reasons affecting decision.
    """
    reasons: list[EnforcementReason] = []

    for section_name, section_value in payload.items():
        if not isinstance(section_value, dict):
            continue

        for key, value in section_value.items():
            if "approval_required" not in key:
                continue

            explicit = _as_bool(value)
            if explicit is True:
                reasons.append(
                    EnforcementReason(
                        path=f"{section_name}.{key}",
                        message="Explicit approval is required by policy.",
                    )
                )

    return reasons


def evaluate_forbidden_flags(payload: dict[str, Any]) -> list[EnforcementReason]:
    """Evaluate whether policy contains explicit forbidden flags.

    Args:
        payload: Policy payload.

    Returns:
        Reasons affecting decision.
    """
    reasons: list[EnforcementReason] = []

    for section_name, section_value in payload.items():
        if not isinstance(section_value, dict):
            continue

        for key, value in section_value.items():
            if not key.endswith("_forbidden"):
                continue

            explicit = _as_bool(value)
            if explicit is True:
                reasons.append(
                    EnforcementReason(
                        path=f"{section_name}.{key}",
                        message="Operation is blocked by explicit forbidden policy flag.",
                    )
                )

    return reasons


def evaluate_rules_text(payload: dict[str, Any]) -> list[EnforcementReason]:
    """Extract human-readable rule lines relevant for review visibility.

    Args:
        payload: Policy payload.

    Returns:
        Informational reasons.
    """
    reasons: list[EnforcementReason] = []

    rules = payload.get("rules")
    if not isinstance(rules, list):
        return reasons

    for index, item in enumerate(rules):
        if isinstance(item, str) and item.strip():
            reasons.append(
                EnforcementReason(
                    path=f"rules[{index}]",
                    message=item.strip(),
                )
            )

    return reasons
