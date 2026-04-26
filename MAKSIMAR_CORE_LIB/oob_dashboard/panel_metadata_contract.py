from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataContract,
    PanelMetadataEntry,
)


def build_panel_metadata_contract() -> PanelMetadataContract:
    """Build the canonical panel metadata contract."""
    entries = (
        PanelMetadataEntry(
            panel_id="system_status",
            title="System Status",
            short_label="Status",
            description="High-level runtime health and canonical system state.",
            panel_family="foundation",
            panel_kind="status",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="guard_chain",
            title="Guard Chain",
            short_label="Guards",
            description="Supervisor, core guard, and kernel watchdog truth chain.",
            panel_family="foundation",
            panel_kind="guard",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="incidents",
            title="Incidents",
            short_label="Incidents",
            description="Ordered incident stream with source and severity visibility.",
            panel_family="foundation",
            panel_kind="incident",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="logs",
            title="Logs",
            short_label="Logs",
            description="Runtime and guard log tail visibility for operator review.",
            panel_family="foundation",
            panel_kind="log",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="topology",
            title="Topology",
            short_label="Topology",
            description="Canonical runtime topology and visibility surface.",
            panel_family="foundation",
            panel_kind="topology",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="action_queue",
            title="Action Queue",
            short_label="Actions",
            description="Queued operator actions pending downstream handling.",
            panel_family="interaction",
            panel_kind="queue",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="approval_queue",
            title="Approval Queue",
            short_label="Approvals",
            description="Pending approvals awaiting operator decision.",
            panel_family="interaction",
            panel_kind="queue",
            default_visible=True,
            operator_visible=True,
        ),
        PanelMetadataEntry(
            panel_id="audit_timeline",
            title="Audit Timeline",
            short_label="Audit",
            description="Canonical audit trail for operator-visible actions.",
            panel_family="interaction",
            panel_kind="audit",
            default_visible=True,
            operator_visible=True,
        ),
    )

    contract = PanelMetadataContract(entries=entries)

    contract_ids = tuple(entry.panel_id for entry in contract.entries)
    if contract_ids != build_canonical_panel_ids():
        raise ValueError("panel metadata order must match canonical panel id order")

    return contract
