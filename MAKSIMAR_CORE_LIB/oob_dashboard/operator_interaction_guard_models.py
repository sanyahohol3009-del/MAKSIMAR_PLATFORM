from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardEntry:
    """Canonical operator interaction guard entry."""

    dashboard_id: str
    interaction_surface_id: str
    guard_mode: str
    direct_execution_allowed: bool
    approval_required: bool
    policy_gate_required: bool
    forbidden_state_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate interaction-guard entry invariants."""
        if not self.dashboard_id.strip():
            raise ValueError("dashboard_id must not be empty")

        if not self.interaction_surface_id.strip():
            raise ValueError("interaction_surface_id must not be empty")

        if not self.guard_mode.strip():
            raise ValueError("guard_mode must not be empty")

        if self.direct_execution_allowed is not False:
            raise ValueError("direct_execution_allowed must be False")

        if self.approval_required is not True:
            raise ValueError("approval_required must be True")

        if self.policy_gate_required is not True:
            raise ValueError("policy_gate_required must be True")

        if self.forbidden_state_visible is not True:
            raise ValueError("forbidden_state_visible must be True")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardContract:
    """Canonical operator interaction guard contract."""

    entries: tuple[OperatorInteractionGuardEntry, ...]

    def __post_init__(self) -> None:
        """Validate interaction-guard contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_dashboard_ids: set[str] = set()
        for entry in self.entries:
            if entry.dashboard_id in seen_dashboard_ids:
                raise ValueError(
                    f"duplicate dashboard_id detected: {entry.dashboard_id}"
                )
            seen_dashboard_ids.add(entry.dashboard_id)
