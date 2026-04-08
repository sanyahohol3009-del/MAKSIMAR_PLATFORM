from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_visible_presentation_contract import (
    build_operator_visible_presentation_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_action_queue_panel_contract import (
    build_operator_action_queue_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_queue_panel_contract import (
    build_operator_approval_queue_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_timeline_panel_contract import (
    build_operator_audit_timeline_panel_contract,
)


BundleState = Literal[
    "operator_bundle_ready",
]

BundleClass = Literal[
    "primary_operator_bundle",
]

ALL_BUNDLE_STATES: tuple[BundleState, ...] = (
    "operator_bundle_ready",
)

ALL_BUNDLE_CLASSES: tuple[BundleClass, ...] = (
    "primary_operator_bundle",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorPresentationBundleEntry:
    """Canonical operator presentation bundle entry."""

    bundle_id: str
    workspace_id: str
    interaction_surface_id: str
    bundle_state: BundleState
    bundle_class: BundleClass
    presentation_entries: int
    action_queue_panel_present: bool
    approval_queue_panel_present: bool
    audit_timeline_panel_present: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator presentation bundle entry."""
        _require_non_empty(self.bundle_id, "bundle_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.interaction_surface_id, "interaction_surface_id")
        _require_non_empty(self.description, "description")

        if self.bundle_state not in ALL_BUNDLE_STATES:
            raise ValueError(
                "bundle_state must be one of "
                f"{ALL_BUNDLE_STATES}, got {self.bundle_state!r}."
            )

        if self.bundle_class not in ALL_BUNDLE_CLASSES:
            raise ValueError(
                "bundle_class must be one of "
                f"{ALL_BUNDLE_CLASSES}, got {self.bundle_class!r}."
            )

        if self.presentation_entries < 1:
            raise ValueError(
                "presentation_entries must be at least 1 for canonical operator bundles."
            )

        if not self.action_queue_panel_present:
            raise ValueError(
                "action_queue_panel_present must remain true for canonical operator bundles."
            )

        if not self.approval_queue_panel_present:
            raise ValueError(
                "approval_queue_panel_present must remain true for canonical operator bundles."
            )

        if not self.audit_timeline_panel_present:
            raise ValueError(
                "audit_timeline_panel_present must remain true for canonical operator bundles."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical operator bundles."
            )


@dataclass(frozen=True, slots=True)
class OperatorPresentationBundleContract:
    """Canonical operator presentation bundle contract."""

    contract_id: str
    total_entries: int
    operator_visible_entries: int
    ready_entries: int
    entries: tuple[OperatorPresentationBundleEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator presentation bundle contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.ready_entries != sum(
            1 for entry in self.entries if entry.bundle_state == "operator_bundle_ready"
        ):
            raise ValueError("ready_entries must match operator_bundle_ready count.")


def build_operator_presentation_bundle_contract() -> OperatorPresentationBundleContract:
    """Build canonical operator presentation bundle contract."""
    visible_presentation_contract = build_operator_visible_presentation_contract()
    action_queue_contract = build_operator_action_queue_panel_contract()
    approval_queue_contract = build_operator_approval_queue_panel_contract()
    audit_timeline_contract = build_operator_audit_timeline_panel_contract()

    entries = (
        OperatorPresentationBundleEntry(
            bundle_id="operator_presentation_bundle_001",
            workspace_id="workspace_operator_main",
            interaction_surface_id="main_operator_interaction_surface_001",
            bundle_state="operator_bundle_ready",
            bundle_class="primary_operator_bundle",
            presentation_entries=visible_presentation_contract.total_entries,
            action_queue_panel_present=action_queue_contract.total_entries == 1,
            approval_queue_panel_present=approval_queue_contract.total_entries == 1,
            audit_timeline_panel_present=audit_timeline_contract.total_entries == 1,
            operator_visible=True,
            description=(
                "Canonical operator presentation bundle combining visible presentations "
                "with action, approval, and audit operator panels."
            ),
        ),
    )

    return OperatorPresentationBundleContract(
        contract_id="operator_presentation_bundle_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        ready_entries=sum(
            1 for entry in entries if entry.bundle_state == "operator_bundle_ready"
        ),
        entries=entries,
    )
