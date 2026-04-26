from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_taxonomy_contract import (
    build_panel_taxonomy_contract,
)


@dataclass(frozen=True, slots=True)
class PanelRoleEntry:
    """Canonical panel-role entry."""

    panel_id: str
    panel_role: str
    description: str

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.panel_role.strip():
            raise ValueError("panel_role must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelRoleContract:
    """Canonical ordered panel-role contract."""

    entries: tuple[PanelRoleEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise ValueError("entries must not be empty")


def build_panel_role_contract() -> PanelRoleContract:
    """Build the canonical panel-role contract."""
    taxonomy_contract = build_panel_taxonomy_contract()

    entries = tuple(
        PanelRoleEntry(
            panel_id=entry.panel_id,
            panel_role=entry.panel_role,
            description=f"Canonical role entry for {entry.panel_id}: {entry.panel_role}.",
        )
        for entry in taxonomy_contract.entries
    )

    return PanelRoleContract(entries=entries)
