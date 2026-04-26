from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


@dataclass(frozen=True, slots=True)
class PanelTaxonomyEntry:
    """Canonical taxonomy entry for a panel."""

    panel_id: str
    panel_family: str
    panel_kind: str
    panel_role: str
    description: str

    def __post_init__(self) -> None:
        """Validate taxonomy entry invariants."""
        if not self.panel_id.strip():
            raise ValueError("panel_id must not be empty")
        if not self.panel_family.strip():
            raise ValueError("panel_family must not be empty")
        if not self.panel_kind.strip():
            raise ValueError("panel_kind must not be empty")
        if not self.panel_role.strip():
            raise ValueError("panel_role must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")


@dataclass(frozen=True, slots=True)
class PanelTaxonomyContract:
    """Canonical ordered taxonomy contract."""

    entries: tuple[PanelTaxonomyEntry, ...]

    def __post_init__(self) -> None:
        """Validate contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)


def resolve_panel_role(panel_id: str) -> str:
    """Resolve canonical panel role."""
    if panel_id in {
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    }:
        return "read_only_monitoring"

    if panel_id in {
        "action_queue",
        "approval_queue",
        "audit_timeline",
    }:
        return "operator_interaction"

    raise ValueError(f"unsupported panel_id for panel_role: {panel_id}")


def build_panel_taxonomy_contract() -> PanelTaxonomyContract:
    """Build the canonical panel taxonomy contract."""
    metadata_contract = build_panel_metadata_contract()

    entries = tuple(
        PanelTaxonomyEntry(
            panel_id=entry.panel_id,
            panel_family=entry.panel_family,
            panel_kind=entry.panel_kind,
            panel_role=resolve_panel_role(entry.panel_id),
            description=(
                f"Canonical taxonomy entry for {entry.title} "
                f"({entry.panel_family}/{entry.panel_kind})."
            ),
        )
        for entry in metadata_contract.entries
    )

    return PanelTaxonomyContract(entries=entries)
