from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_panel_summary_contract import (
    build_foundation_status_panel_summary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_exposure_policy_contract import (
    build_panel_exposure_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_source_binding_contract import (
    build_panel_source_binding_contract,
)


ContentContractKind = Literal[
    "foundation_status_summary_contract",
    "diagnostics_view_contract",
    "interaction_contract",
    "execution_panel_contract",
    "navigation_contract",
]


@dataclass(frozen=True, slots=True)
class PanelContentEntry:
    """Canonical content-contract entry for one panel."""

    panel_id: str
    content_contract_kind: ContentContractKind
    content_contract_name: str
    content_scope: str
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelContentContract:
    """Canonical panel content contract."""

    total_entries: int
    foundation_content_entries: int
    diagnostics_content_entries: int
    interaction_content_entries: int
    execution_content_entries: int
    navigation_content_entries: int
    read_only_entries: int
    interactive_entries: int
    entries: tuple[PanelContentEntry, ...]


def build_panel_content_contract() -> PanelContentContract:
    """Build canonical panel content contract."""
    metadata_contract = build_panel_metadata_contract()
    exposure_contract = build_panel_exposure_policy_contract()
    source_binding_contract = build_panel_source_binding_contract()
    foundation_summary_contract = build_foundation_status_panel_summary_contract()

    metadata_map = {entry.panel_id: entry for entry in metadata_contract.entries}
    exposure_map = {entry.panel_id: entry for entry in exposure_contract.entries}
    source_map = {entry.panel_id: entry for entry in source_binding_contract.entries}
    foundation_ids = {
        entry.panel_id for entry in foundation_summary_contract.entries
    }

    def resolve_content_kind(panel_id: str) -> ContentContractKind:
        if panel_id in foundation_ids:
            return "foundation_status_summary_contract"
        source_binding = source_map[panel_id].source_binding
        if source_binding in (
            "foundation_incident_view",
            "foundation_diagnostics_correlation_view",
            "foundation_live_status_adapter",
        ):
            return "diagnostics_view_contract"
        if source_binding in (
            "dashboard_chat_contract",
            "dashboard_settings_panel",
            "gesture_panel_contract",
        ):
            return "interaction_contract"
        if source_binding == "execution_panel_contract":
            return "execution_panel_contract"
        return "navigation_contract"

    def resolve_content_name(panel_id: str) -> str:
        if panel_id in foundation_ids:
            return "build_foundation_status_panel_summary_contract"
        return source_map[panel_id].source_contract_name

    def resolve_scope(panel_id: str) -> str:
        if panel_id in foundation_ids:
            return "foundation"
        return source_map[panel_id].source_scope

    entries = tuple(
        PanelContentEntry(
            panel_id=panel_id,
            content_contract_kind=resolve_content_kind(panel_id),
            content_contract_name=resolve_content_name(panel_id),
            content_scope=resolve_scope(panel_id),
            read_only=(
                metadata_map[panel_id].read_mode in ("read_only", "hidden_internal")
                or exposure_map[panel_id].visibility_policy
                in ("read_only_public", "hidden_internal")
                or panel_id in foundation_ids
            ),
            description=(
                f"Canonical panel content contract entry for {metadata_map[panel_id].display_title}."
            ),
        )
        for panel_id in metadata_map
    )

    return PanelContentContract(
        total_entries=len(entries),
        foundation_content_entries=sum(
            1
            for entry in entries
            if entry.content_contract_kind == "foundation_status_summary_contract"
        ),
        diagnostics_content_entries=sum(
            1
            for entry in entries
            if entry.content_contract_kind == "diagnostics_view_contract"
        ),
        interaction_content_entries=sum(
            1
            for entry in entries
            if entry.content_contract_kind == "interaction_contract"
        ),
        execution_content_entries=sum(
            1
            for entry in entries
            if entry.content_contract_kind == "execution_panel_contract"
        ),
        navigation_content_entries=sum(
            1
            for entry in entries
            if entry.content_contract_kind == "navigation_contract"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        interactive_entries=sum(1 for entry in entries if not entry.read_only),
        entries=entries,
    )
