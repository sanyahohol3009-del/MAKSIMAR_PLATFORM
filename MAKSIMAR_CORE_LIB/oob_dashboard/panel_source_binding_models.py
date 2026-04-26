from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PanelSourceBindingEntry:
    """Canonical source-binding entry for a panel."""

    panel_id: str
    source_binding: str
    source_contract_name: str
    source_scope: str
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.source_binding.strip():
            raise ValueError("source_binding must not be empty")
        if not self.source_contract_name.strip():
            raise ValueError("source_contract_name must not be empty")
        if not self.source_scope.strip():
            raise ValueError("source_scope must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelSourceBindingContract:
    """Canonical ordered source-binding contract."""

    entries: tuple[PanelSourceBindingEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)
