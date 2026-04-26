from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_source_binding_contract import (
    build_panel_source_binding_contract,
)


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
        """Validate panel content entry invariants."""
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
        """Validate contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)


def build_panel_content_contract() -> PanelContentContract:
    """Build the canonical panel content contract."""
    metadata_contract = build_panel_metadata_contract()
    source_binding_contract = build_panel_source_binding_contract()

    metadata_map = {entry.panel_id: entry for entry in metadata_contract.entries}
    source_map = {entry.panel_id: entry for entry in source_binding_contract.entries}

    content_map: dict[str, tuple[str, str, str, bool, str]] = {
        "system_status": (
            "system_status_panel_content_contract",
            "summary",
            "foundation",
            True,
            "System status exposes canonical runtime summary content.",
        ),
        "guard_chain": (
            "guard_chain_panel_content_contract",
            "summary",
            "foundation",
            True,
            "Guard chain exposes canonical guard-chain summary content.",
        ),
        "incidents": (
            "incidents_panel_content_contract",
            "timeline",
            "foundation",
            True,
            "Incidents expose canonical incident timeline content.",
        ),
        "logs": (
            "logs_panel_content_contract",
            "log_tail",
            "foundation",
            True,
            "Logs expose canonical log-tail content.",
        ),
        "topology": (
            "topology_panel_content_contract",
            "topology",
            "foundation",
            True,
            "Topology exposes canonical runtime-topology content.",
        ),
        "action_queue": (
            "action_queue_panel_content_contract",
            "queue",
            "interaction",
            True,
            "Action queue exposes canonical queued-action content.",
        ),
        "approval_queue": (
            "approval_queue_panel_content_contract",
            "queue",
            "interaction",
            True,
            "Approval queue exposes canonical approval content.",
        ),
        "audit_timeline": (
            "audit_timeline_panel_content_contract",
            "timeline",
            "interaction",
            True,
            "Audit timeline exposes canonical audit content.",
        ),
    }

    entries = tuple(
        PanelContentEntry(
            panel_id=panel_id,
            content_contract_name=content_map[panel_id][0],
            content_kind=content_map[panel_id][1],
            content_scope=content_map[panel_id][2],
            read_only=content_map[panel_id][3],
            description=(
                f"{content_map[panel_id][4]} "
                f"Panel title: {metadata_map[panel_id].title}. "
                f"Source contract: {source_map[panel_id].source_contract_name}."
            ),
        )
        for panel_id in metadata_map
    )

    return PanelContentContract(entries=entries)
