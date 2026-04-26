from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PanelZoneEntry:
    """Canonical panel zone / slot vocabulary entry."""

    layout_zone: str
    layout_slot_id: str
    slot_family: str
    slot_order: int
    description: str

    def __post_init__(self) -> None:
        """Validate panel-zone entry invariants."""
        if not self.layout_zone.strip():
            raise ValueError("layout_zone must not be empty")

        if not self.layout_slot_id.strip():
            raise ValueError("layout_slot_id must not be empty")

        if not self.slot_family.strip():
            raise ValueError("slot_family must not be empty")

        if self.slot_order < 0:
            raise ValueError("slot_order must be >= 0")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelZoneVocabularyContract:
    """Canonical ordered panel zone / slot vocabulary contract."""

    entries: tuple[PanelZoneEntry, ...]

    def __post_init__(self) -> None:
        """Validate panel-zone vocabulary contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_pairs: set[tuple[str, str]] = set()
        for entry in self.entries:
            key = (entry.layout_zone, entry.layout_slot_id)
            if key in seen_pairs:
                raise ValueError(
                    "duplicate layout_zone/layout_slot_id detected: "
                    f"{entry.layout_zone}/{entry.layout_slot_id}"
                )
            seen_pairs.add(key)
