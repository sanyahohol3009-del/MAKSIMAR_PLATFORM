from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import PanelId


PanelFamily = str
PanelKind = str


@dataclass(frozen=True, slots=True)
class PanelVocabularyEntry:
    """Canonical vocabulary entry describing a known panel."""

    panel_id: PanelId
    title: str
    description: str
    panel_family: PanelFamily
    panel_kind: PanelKind
    display_priority: int

    def __post_init__(self) -> None:
        """Validate panel vocabulary invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")

        if self.panel_id != self.panel_id.strip():
            raise ValueError("panel_id must not contain leading/trailing whitespace")

        if " " in self.panel_id:
            raise ValueError("panel_id must not contain spaces")

        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")

        if not self.panel_family.strip():
            raise ValueError("panel_family must not be empty")

        if not self.panel_kind.strip():
            raise ValueError("panel_kind must not be empty")

        if self.display_priority < 0:
            raise ValueError("display_priority must be >= 0")


@dataclass(frozen=True, slots=True)
class PanelVocabularyContract:
    """Canonical ordered panel vocabulary contract."""

    entries: tuple[PanelVocabularyEntry, ...]

    def __post_init__(self) -> None:
        """Validate contract-level invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        seen_priorities: set[int] = set()

        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)

            if entry.display_priority in seen_priorities:
                raise ValueError(
                    "display_priority values must be unique within the vocabulary"
                )
            seen_priorities.add(entry.display_priority)
