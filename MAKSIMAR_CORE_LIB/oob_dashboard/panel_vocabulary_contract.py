from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import build_canonical_panel_ids
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_vocabulary_models import (
    PanelVocabularyContract,
    PanelVocabularyEntry,
)


def build_panel_vocabulary_contract() -> PanelVocabularyContract:
    """Build the canonical ordered panel vocabulary contract."""
    entries = (
        PanelVocabularyEntry(
            panel_id="system_status",
            title="System Status",
            description="High-level runtime health and canonical system state.",
            panel_family="foundation",
            panel_kind="status",
            display_priority=0,
        ),
        PanelVocabularyEntry(
            panel_id="guard_chain",
            title="Guard Chain",
            description="Supervisor, core guard, and kernel watchdog truth chain.",
            panel_family="foundation",
            panel_kind="guard",
            display_priority=1,
        ),
        PanelVocabularyEntry(
            panel_id="incidents",
            title="Incidents",
            description="Ordered incident stream with source and severity visibility.",
            panel_family="foundation",
            panel_kind="incident",
            display_priority=2,
        ),
        PanelVocabularyEntry(
            panel_id="logs",
            title="Logs",
            description="Runtime and guard log tail visibility for operator review.",
            panel_family="foundation",
            panel_kind="log",
            display_priority=3,
        ),
        PanelVocabularyEntry(
            panel_id="topology",
            title="Topology",
            description="Canonical runtime topology and visibility surface.",
            panel_family="foundation",
            panel_kind="topology",
            display_priority=4,
        ),
        PanelVocabularyEntry(
            panel_id="action_queue",
            title="Action Queue",
            description="Queued operator actions pending downstream handling.",
            panel_family="interaction",
            panel_kind="queue",
            display_priority=5,
        ),
        PanelVocabularyEntry(
            panel_id="approval_queue",
            title="Approval Queue",
            description="Pending approvals awaiting operator decision.",
            panel_family="interaction",
            panel_kind="queue",
            display_priority=6,
        ),
        PanelVocabularyEntry(
            panel_id="audit_timeline",
            title="Audit Timeline",
            description="Canonical audit trail for operator-visible actions.",
            panel_family="interaction",
            panel_kind="audit",
            display_priority=7,
        ),
    )

    contract = PanelVocabularyContract(entries=entries)

    canonical_ids = build_canonical_panel_ids()
    contract_ids = tuple(entry.panel_id for entry in contract.entries)
    if contract_ids != canonical_ids:
        raise ValueError("panel vocabulary order must match canonical panel id order")

    expected_priorities = tuple(range(len(contract.entries)))
    actual_priorities = tuple(entry.display_priority for entry in contract.entries)
    if actual_priorities != expected_priorities:
        raise ValueError(
            "display_priority values must form a contiguous canonical sequence"
        )

    return contract
