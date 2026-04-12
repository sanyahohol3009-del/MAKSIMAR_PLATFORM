from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_contract import (
    build_operator_workspace_binding_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardEntry:
    """Canonical operator interaction guard entry."""

    dashboard_id: str
    workspace_id: str
    interaction_surface: str
    guard_state: str
    guard_decision: str
    direct_execution_allowed: bool
    read_only_allowed: bool
    with_approval_allowed: bool
    approval_required_for_mutation: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.interaction_surface, "interaction_surface")
        _require_non_empty(self.guard_state, "guard_state")
        _require_non_empty(self.guard_decision, "guard_decision")
        _require_non_empty(self.description, "description")

        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical entries."
            )
        if self.read_only_allowed:
            raise ValueError(
                "read_only_allowed must remain false for canonical entries."
            )
        if not self.with_approval_allowed:
            raise ValueError(
                "with_approval_allowed must remain true for canonical entries."
            )
        if not self.approval_required_for_mutation:
            raise ValueError(
                "approval_required_for_mutation must remain true for canonical entries."
            )
        if not self.operator_visible:
            raise ValueError("operator_visible must remain true for canonical entries.")


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardContract:
    """Canonical operator interaction guard contract."""

    contract_id: str
    total_entries: int
    allowed_read_only_entries: int
    allowed_with_approval_entries: int
    blocked_direct_execution_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorInteractionGuardEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.allowed_read_only_entries != sum(
            1 for entry in self.entries if entry.read_only_allowed
        ):
            raise ValueError(
                "allowed_read_only_entries must match read_only_allowed count."
            )
        if self.allowed_with_approval_entries != sum(
            1 for entry in self.entries if entry.with_approval_allowed
        ):
            raise ValueError(
                "allowed_with_approval_entries must match with_approval_allowed count."
            )
        if self.blocked_direct_execution_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed
        ):
            raise ValueError(
                "blocked_direct_execution_entries must match direct_execution_allowed count."
            )
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_interaction_guard_contract() -> OperatorInteractionGuardContract:
    """Build canonical operator interaction guard contract."""
    binding = build_operator_workspace_binding_contract().entries[0]

    entries = (
        OperatorInteractionGuardEntry(
            dashboard_id=binding.dashboard_id,
            workspace_id=binding.workspace_id,
            interaction_surface="dashboard_read_model",
            guard_state="operator_interaction_guard_enabled",
            guard_decision="allowed_with_approval",
            direct_execution_allowed=False,
            read_only_allowed=False,
            with_approval_allowed=True,
            approval_required_for_mutation=True,
            operator_visible=True,
            description="Canonical operator interaction guard entry.",
        ),
    )

    return OperatorInteractionGuardContract(
        contract_id="operator_interaction_guard_contract_001",
        total_entries=len(entries),
        allowed_read_only_entries=sum(
            1 for entry in entries if entry.read_only_allowed
        ),
        allowed_with_approval_entries=sum(
            1 for entry in entries if entry.with_approval_allowed
        ),
        blocked_direct_execution_entries=sum(
            1 for entry in entries if entry.direct_execution_allowed
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
