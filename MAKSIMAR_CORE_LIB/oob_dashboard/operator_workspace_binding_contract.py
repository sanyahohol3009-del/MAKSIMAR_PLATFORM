from __future__ import annotations

from dataclasses import dataclass


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingEntry:
    """Canonical operator workspace binding entry."""

    dashboard_id: str
    workspace_id: str
    workspace_role: str
    display_target_id: str
    binding_state: str
    interactive: bool
    supports_interaction: bool
    read_only: bool
    is_primary_operator_workspace: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.workspace_role, "workspace_role")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.binding_state, "binding_state")
        _require_non_empty(self.description, "description")

        if not self.interactive:
            raise ValueError("interactive must remain true for canonical entries.")
        if not self.supports_interaction:
            raise ValueError(
                "supports_interaction must remain true for canonical entries."
            )
        if self.read_only:
            raise ValueError("read_only must remain false for canonical entries.")
        if not self.is_primary_operator_workspace:
            raise ValueError(
                "is_primary_operator_workspace must remain true for canonical entries."
            )
        if not self.operator_visible:
            raise ValueError("operator_visible must remain true for canonical entries.")


@dataclass(frozen=True, slots=True)
class OperatorWorkspaceBindingContract:
    """Canonical operator workspace binding contract."""

    contract_id: str
    total_entries: int
    primary_operator_workspace_entries: int
    interactive_entries: int
    read_only_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorWorkspaceBindingEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.primary_operator_workspace_entries != sum(
            1 for entry in self.entries if entry.is_primary_operator_workspace
        ):
            raise ValueError(
                "primary_operator_workspace_entries must match canonical count."
            )
        if self.interactive_entries != sum(
            1 for entry in self.entries if entry.interactive
        ):
            raise ValueError("interactive_entries must match interactive count.")
        if self.read_only_entries != sum(
            1 for entry in self.entries if entry.read_only
        ):
            raise ValueError("read_only_entries must match read_only count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_workspace_binding_contract() -> OperatorWorkspaceBindingContract:
    """Build canonical operator workspace binding contract."""
    entries = (
        OperatorWorkspaceBindingEntry(
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            workspace_role="operator_surface",
            display_target_id="display_primary_operator",
            binding_state="operator_workspace_bound",
            interactive=True,
            supports_interaction=True,
            read_only=False,
            is_primary_operator_workspace=True,
            operator_visible=True,
            description="Canonical main operator dashboard binding.",
        ),
    )

    return OperatorWorkspaceBindingContract(
        contract_id="operator_workspace_binding_contract_001",
        total_entries=len(entries),
        primary_operator_workspace_entries=sum(
            1 for entry in entries if entry.is_primary_operator_workspace
        ),
        interactive_entries=sum(1 for entry in entries if entry.interactive),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
