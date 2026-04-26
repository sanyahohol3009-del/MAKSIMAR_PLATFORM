from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


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
        """Validate source-binding entry invariants."""
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
        """Validate contract invariants."""
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_ids: set[str] = set()
        for entry in self.entries:
            if entry.panel_id in seen_ids:
                raise ValueError(f"duplicate panel_id detected: {entry.panel_id}")
            seen_ids.add(entry.panel_id)


def build_panel_source_binding_contract() -> PanelSourceBindingContract:
    """Build the canonical panel source-binding contract."""
    metadata_contract = build_panel_metadata_contract()
    metadata_entries = metadata_contract.entries

    binding_map: dict[str, tuple[str, str, str, bool, str]] = {
        "system_status": (
            "runtime_summary",
            "system_status_panel_content_contract",
            "foundation",
            True,
            "System status reads canonical runtime summary artifacts.",
        ),
        "guard_chain": (
            "guard_chain_summary",
            "guard_chain_panel_content_contract",
            "foundation",
            True,
            "Guard chain reads canonical guard-chain summary artifacts.",
        ),
        "incidents": (
            "incident_stream",
            "incidents_panel_content_contract",
            "foundation",
            True,
            "Incidents read canonical incident stream artifacts.",
        ),
        "logs": (
            "log_tail",
            "logs_panel_content_contract",
            "foundation",
            True,
            "Logs read canonical log tail artifacts.",
        ),
        "topology": (
            "runtime_topology",
            "topology_panel_content_contract",
            "foundation",
            True,
            "Topology reads canonical runtime topology artifacts.",
        ),
        "action_queue": (
            "action_queue_state",
            "action_queue_panel_content_contract",
            "interaction",
            True,
            "Action queue reads canonical queued-action artifacts.",
        ),
        "approval_queue": (
            "approval_queue_state",
            "approval_queue_panel_content_contract",
            "interaction",
            True,
            "Approval queue reads canonical approval artifacts.",
        ),
        "audit_timeline": (
            "audit_timeline_state",
            "audit_timeline_panel_content_contract",
            "interaction",
            True,
            "Audit timeline reads canonical audit artifacts.",
        ),
    }

    entries = tuple(
        PanelSourceBindingEntry(
            panel_id=entry.panel_id,
            source_binding=binding_map[entry.panel_id][0],
            source_contract_name=binding_map[entry.panel_id][1],
            source_scope=binding_map[entry.panel_id][2],
            read_only=binding_map[entry.panel_id][3],
            description=binding_map[entry.panel_id][4],
        )
        for entry in metadata_entries
    )

    return PanelSourceBindingContract(entries=entries)
