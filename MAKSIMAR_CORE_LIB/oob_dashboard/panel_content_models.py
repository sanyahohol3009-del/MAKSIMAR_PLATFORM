from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PanelContentEntry:
    """Canonical panel content entry."""

    panel_id: str
    content_contract_name: str
    content_kind: str
    content_scope: str
    read_only: bool
    description: str

    def __post_init__(self) -> None:
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.content_contract_name.strip():
            raise ValueError("content_contract_name must not be empty")
        if not self.content_kind.strip():
            raise ValueError("content_kind must not be empty")
        if not self.content_scope.strip():
            raise ValueError("content_scope must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelContentContract:
    """Canonical ordered panel content contract."""

    entries: tuple[PanelContentEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)
