from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_taxonomy_contract import (
    build_panel_taxonomy_contract,
)


@dataclass(frozen=True, slots=True)
class PanelFamilyEntry:
    """Canonical panel-family entry."""

    panel_id: str
    panel_family: str
    description: str

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.panel_family.strip():
            raise ValueError("panel_family must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelFamilyContract:
    """Canonical ordered panel-family contract."""

    entries: tuple[PanelFamilyEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise ValueError("entries must not be empty")


def build_panel_family_contract() -> PanelFamilyContract:
    """Build the canonical panel-family contract."""
    taxonomy_contract = build_panel_taxonomy_contract()

    entries = tuple(
        PanelFamilyEntry(
            panel_id=entry.panel_id,
            panel_family=entry.panel_family,
            description=(
                f"Canonical family entry for {entry.panel_id}: {entry.panel_family}."
            ),
        )
        for entry in taxonomy_contract.entries
    )

    return PanelFamilyContract(entries=entries)
