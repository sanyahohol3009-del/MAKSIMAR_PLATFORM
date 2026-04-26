
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)


@dataclass(frozen=True, slots=True)
class DisplayRoleEntry:
    """Canonical display-role entry."""

    display_target_id: str
    display_role: str
    description: str

    def __post_init__(self) -> None:
        """Validate display-role entry invariants."""
        if not self.display_target_id.strip():
            raise ValueError("display_target_id must not be empty")

        if not self.display_role.strip():
            raise ValueError("display_role must not be empty")

        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class DisplayRoleContract:
    """Canonical ordered display-role contract."""

    entries: tuple[DisplayRoleEntry, ...]

    def __post_init__(self) -> None:
        """Validate display-role contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_target_ids: set[str] = set()
        seen_roles: set[str] = set()

        for entry in self.entries:
            if entry.display_target_id in seen_target_ids:
                raise ValueError(
                    f"duplicate display_target_id detected: {entry.display_target_id}"
                )
            seen_target_ids.add(entry.display_target_id)

            if entry.display_role in seen_roles:
                raise ValueError(
                    f"duplicate display_role detected: {entry.display_role}"
                )
            seen_roles.add(entry.display_role)


def build_display_role_contract() -> DisplayRoleContract:
    """Build the canonical display-role contract."""
    vocabulary_contract = build_display_target_vocabulary_contract()

    entries = tuple(
        DisplayRoleEntry(
            display_target_id=entry.display_target_id,
            display_role=entry.display_role,
            description=(
                f"Canonical display role mapping for {entry.display_target_id}: "
                f"{entry.display_role}."
            ),
        )
        for entry in vocabulary_contract.entries
    )

    return DisplayRoleContract(entries=entries)
