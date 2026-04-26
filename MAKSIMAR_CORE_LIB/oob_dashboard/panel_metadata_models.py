from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import PanelId


@dataclass(frozen=True, slots=True)
class PanelMetadataEntry:
    """Canonical metadata entry for a panel."""

    panel_id: PanelId
    title: str
    short_label: str
    description: str
    panel_family: str
    panel_kind: str
    default_visible: bool
    operator_visible: bool

    def __post_init__(self) -> None:
        """Validate metadata invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.short_label.strip():
            raise ValueError("short_label must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")

        if not self.panel_family.strip():
            raise ValueError("panel_family must not be empty")

        if not self.panel_kind.strip():
            raise ValueError("panel_kind must not be empty")


@dataclass(frozen=True, slots=True)
class PanelMetadataContract:
    """Canonical ordered metadata contract."""

    entries: tuple[PanelMetadataEntry, ...]

    def __post_init__(self) -> None:
        """Validate metadata contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        seen_labels: set[str] = set()

        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)

            normalized_label = entry.short_label.strip().lower()
            if normalized_label in seen_labels:
                raise ValueError(
                    f"duplicate short_label detected: {entry.short_label}"
                )
            seen_labels.add(normalized_label)
