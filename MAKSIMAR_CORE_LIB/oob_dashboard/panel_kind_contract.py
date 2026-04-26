from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_taxonomy_contract import (
    build_panel_taxonomy_contract,
)


@dataclass(frozen=True, slots=True)
class PanelKindEntry:
    """Canonical panel-kind entry."""

    panel_id: str
    panel_kind: str
    description: str

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.panel_kind.strip():
            raise ValueError("panel_kind must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelKindContract:
    """Canonical ordered panel-kind contract."""

    entries: tuple[PanelKindEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise ValueError("entries must not be empty")


def build_panel_kind_contract() -> PanelKindContract:
    """Build the canonical panel-kind contract."""
    taxonomy_contract = build_panel_taxonomy_contract()

    entries = tuple(
        PanelKindEntry(
            panel_id=entry.panel_id,
            panel_kind=entry.panel_kind,
            description=f"Canonical kind entry for {entry.panel_id}: {entry.panel_kind}.",
        )
        for entry in taxonomy_contract.entries
    )

    return PanelKindContract(entries=entries)
