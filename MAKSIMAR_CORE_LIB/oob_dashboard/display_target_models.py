from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DisplayTargetEntry:
    """Canonical display target entry."""

    display_target_id: str
    display_role: str
    display_zone: str
    description: str

    def __post_init__(self) -> None:
        """Validate display target invariants."""
        if not self.display_target_id.strip():
            raise ValueError("display_target_id must not be empty")

        if not self.display_role.strip():
            raise ValueError("display_role must not be empty")

        if not self.display_zone.strip():
            raise ValueError("display_zone must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class DisplayTargetVocabularyContract:
    """Canonical ordered display target vocabulary contract."""

    entries: tuple[DisplayTargetEntry, ...]

    def __post_init__(self) -> None:
        """Validate vocabulary contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        seen_roles: set[str] = set()

        for entry in self.entries:
            if entry.display_target_id in seen_ids:
                raise ValueError(
                    f"duplicate display_target_id detected: {entry.display_target_id}"
                )
            seen_ids.add(entry.display_target_id)

            if entry.display_role in seen_roles:
                raise ValueError(
                    f"duplicate display_role detected: {entry.display_role}"
                )
            seen_roles.add(entry.display_role)
