from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import PanelId


@dataclass(frozen=True, slots=True)
class PanelRegistryEntry:
    """Canonical registry entry for a known panel."""

    panel_id: PanelId
    title: str
    panel_family: str
    panel_kind: str
    source_binding_required: bool
    visibility_policy_required: bool

    def __post_init__(self) -> None:
        """Validate registry entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.panel_family.strip():
            raise ValueError("panel_family must not be empty")

        if not self.panel_kind.strip():
            raise ValueError("panel_kind must not be empty")


@dataclass(frozen=True, slots=True)
class PanelRegistryContract:
    """Canonical ordered registry of known panels."""

    entries: tuple[PanelRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate registry-level invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)
