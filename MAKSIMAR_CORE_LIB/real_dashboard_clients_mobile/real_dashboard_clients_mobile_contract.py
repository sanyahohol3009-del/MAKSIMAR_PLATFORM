from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.ar_glasses_display_contract import (
    build_ar_glasses_display_contract,
)
from MAKSIMAR_CORE_LIB.end_to_end_orchestration_runtime import (
    build_end_to_end_orchestration_runtime_contract,
)
from MAKSIMAR_CORE_LIB.physics_dashboard_views import (
    build_physics_dashboard_views_contract,
)
from MAKSIMAR_CORE_LIB.real_node_agents import (
    build_real_node_agents_contract,
)
from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


RealClientEntryId = Literal[
    "realclient_dashboard_001",
    "realclient_mobile_001",
    "realclient_ar_glasses_001",
]

ClientKind = Literal[
    "dashboard_client",
    "mobile_client",
    "ar_glasses_client",
]

PresentationMode = Literal[
    "read_only_dashboard",
    "mobile_proxy_view",
    "private_spatial_view",
]

ClientRuntimeStatus = Literal[
    "active",
]


_ENTRY_ID_PATTERN = re.compile(r"^realclient_[a-z][a-z0-9_]*$")
_ORCH_ID_PATTERN = re.compile(r"^orchestration_[a-z][a-z0-9_]*$")
_AGENT_ID_PATTERN = re.compile(r"^nodeagent_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_WRIST_ID_PATTERN = re.compile(r"^wrist_[a-z][a-z0-9_]*$")
_AR_ID_PATTERN = re.compile(r"^ar_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class RealDashboardClientMobileEntry:
    """Canonical real dashboard / clients / mobile entry."""

    real_client_entry_id: RealClientEntryId
    client_kind: ClientKind
    linked_orchestration_entry_id: str
    linked_node_agent_id: str
    linked_panel_id: str | None
    linked_wrist_terminal_id: str | None
    linked_ar_display_id: str | None
    presentation_mode: PresentationMode
    read_only_required: bool
    transport_path_required: bool
    explainable_required: bool
    production_path_allowed: bool
    client_runtime_status: ClientRuntimeStatus
    description: str

    def __post_init__(self) -> None:
        """Validate real dashboard / clients / mobile invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.real_client_entry_id):
            raise ValueError(
                f"Invalid real_client_entry_id: {self.real_client_entry_id}"
            )

        if not _ORCH_ID_PATTERN.fullmatch(self.linked_orchestration_entry_id):
            raise ValueError(
                f"Invalid linked_orchestration_entry_id: {self.linked_orchestration_entry_id}"
            )

        if not _AGENT_ID_PATTERN.fullmatch(self.linked_node_agent_id):
            raise ValueError(
                f"Invalid linked_node_agent_id: {self.linked_node_agent_id}"
            )

        if self.linked_panel_id is not None:
            if not _PANEL_ID_PATTERN.fullmatch(self.linked_panel_id):
                raise ValueError(f"Invalid linked_panel_id: {self.linked_panel_id}")

        if self.linked_wrist_terminal_id is not None:
            if not _WRIST_ID_PATTERN.fullmatch(self.linked_wrist_terminal_id):
                raise ValueError(
                    f"Invalid linked_wrist_terminal_id: {self.linked_wrist_terminal_id}"
                )

        if self.linked_ar_display_id is not None:
            if not _AR_ID_PATTERN.fullmatch(self.linked_ar_display_id):
                raise ValueError(
                    f"Invalid linked_ar_display_id: {self.linked_ar_display_id}"
                )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.real_client_entry_id}"
            )

        if not self.read_only_required:
            raise ValueError(
                f"read_only_required must be True: {self.real_client_entry_id}"
            )

        if not self.transport_path_required:
            raise ValueError(
                f"transport_path_required must be True: {self.real_client_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.real_client_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.real_client_entry_id}"
            )

        if self.client_runtime_status != "active":
            raise ValueError(
                f"client_runtime_status must be active: {self.real_client_entry_id}"
            )

        if self.real_client_entry_id == "realclient_dashboard_001":
            if self.client_kind != "dashboard_client":
                raise ValueError("realclient_dashboard_001 must use dashboard_client")
            if self.linked_orchestration_entry_id != "orchestration_control_plane_001":
                raise ValueError(
                    "realclient_dashboard_001 must link orchestration_control_plane_001"
                )
            if self.linked_node_agent_id != "nodeagent_dev_001":
                raise ValueError(
                    "realclient_dashboard_001 must link nodeagent_dev_001"
                )
            if self.linked_panel_id != "panel_validation_report_001":
                raise ValueError(
                    "realclient_dashboard_001 must link panel_validation_report_001"
                )
            if self.linked_wrist_terminal_id is not None:
                raise ValueError(
                    "realclient_dashboard_001 must not link wrist terminal"
                )
            if self.linked_ar_display_id is not None:
                raise ValueError(
                    "realclient_dashboard_001 must not link ar display"
                )
            if self.presentation_mode != "read_only_dashboard":
                raise ValueError(
                    "realclient_dashboard_001 must use read_only_dashboard"
                )

        if self.real_client_entry_id == "realclient_mobile_001":
            if self.client_kind != "mobile_client":
                raise ValueError("realclient_mobile_001 must use mobile_client")
            if self.linked_orchestration_entry_id != "orchestration_mobile_entry_001":
                raise ValueError(
                    "realclient_mobile_001 must link orchestration_mobile_entry_001"
                )
            if self.linked_node_agent_id != "nodeagent_mobile_001":
                raise ValueError(
                    "realclient_mobile_001 must link nodeagent_mobile_001"
                )
            if self.linked_panel_id != "panel_project_export_001":
                raise ValueError(
                    "realclient_mobile_001 must link panel_project_export_001"
                )
            if self.linked_wrist_terminal_id != "wrist_terminal_core_001":
                raise ValueError(
                    "realclient_mobile_001 must link wrist_terminal_core_001"
                )
            if self.linked_ar_display_id is not None:
                raise ValueError(
                    "realclient_mobile_001 must not link ar display"
                )
            if self.presentation_mode != "mobile_proxy_view":
                raise ValueError(
                    "realclient_mobile_001 must use mobile_proxy_view"
                )

        if self.real_client_entry_id == "realclient_ar_glasses_001":
            if self.client_kind != "ar_glasses_client":
                raise ValueError("realclient_ar_glasses_001 must use ar_glasses_client")
            if self.linked_orchestration_entry_id != "orchestration_mobile_entry_001":
                raise ValueError(
                    "realclient_ar_glasses_001 must link orchestration_mobile_entry_001"
                )
            if self.linked_node_agent_id != "nodeagent_mobile_001":
                raise ValueError(
                    "realclient_ar_glasses_001 must link nodeagent_mobile_001"
                )
            if self.linked_panel_id != "panel_optics_mode_001":
                raise ValueError(
                    "realclient_ar_glasses_001 must link panel_optics_mode_001"
                )
            if self.linked_wrist_terminal_id != "wrist_terminal_core_001":
                raise ValueError(
                    "realclient_ar_glasses_001 must link wrist_terminal_core_001"
                )
            if self.linked_ar_display_id != "ar_glasses_display_core_001":
                raise ValueError(
                    "realclient_ar_glasses_001 must link ar_glasses_display_core_001"
                )
            if self.presentation_mode != "private_spatial_view":
                raise ValueError(
                    "realclient_ar_glasses_001 must use private_spatial_view"
                )


@dataclass(frozen=True, slots=True)
class RealDashboardClientsMobileContract:
    """Unified real dashboard / clients / mobile contract."""

    total_entries: int
    dashboard_entries: int
    mobile_entries: int
    spatial_entries: int
    active_entries: int
    entries: tuple[RealDashboardClientMobileEntry, ...]

    def __post_init__(self) -> None:
        """Validate real dashboard / clients / mobile contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        dashboard_entries = sum(
            1 for entry in self.entries if entry.client_kind == "dashboard_client"
        )
        mobile_entries = sum(
            1 for entry in self.entries if entry.client_kind == "mobile_client"
        )
        spatial_entries = sum(
            1 for entry in self.entries if entry.client_kind == "ar_glasses_client"
        )
        active_entries = sum(
            1 for entry in self.entries if entry.client_runtime_status == "active"
        )

        if self.dashboard_entries != dashboard_entries:
            raise ValueError("dashboard_entries must match computed count")

        if self.mobile_entries != mobile_entries:
            raise ValueError("mobile_entries must match computed count")

        if self.spatial_entries != spatial_entries:
            raise ValueError("spatial_entries must match computed count")

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        entry_ids = tuple(entry.real_client_entry_id for entry in self.entries)
        client_kinds = tuple(entry.client_kind for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate real_client_entry_id values detected")

        if len(set(client_kinds)) != len(client_kinds):
            raise ValueError("Duplicate client_kind values detected")


def build_real_dashboard_clients_mobile_contract() -> RealDashboardClientsMobileContract:
    """Build canonical real dashboard / clients / mobile contract."""
    orchestration_contract = build_end_to_end_orchestration_runtime_contract()
    node_agent_contract = build_real_node_agents_contract()
    physics_dashboard_contract = build_physics_dashboard_views_contract()
    wrist_contract = build_wrist_terminal_contract()
    ar_contract = build_ar_glasses_display_contract()

    orchestration_ids = {entry.orchestration_entry_id for entry in orchestration_contract.entries}
    node_agent_ids = {entry.real_node_agent_entry_id for entry in node_agent_contract.entries}
    panel_ids = {entry.panel_id for entry in physics_dashboard_contract.entries}
    wrist_ids = {entry.wrist_terminal_id for entry in wrist_contract.entries}
    ar_ids = {entry.ar_display_id for entry in ar_contract.entries}

    required_orchestration_ids = {
        "orchestration_control_plane_001",
        "orchestration_mobile_entry_001",
    }
    required_node_agent_ids = {
        "nodeagent_dev_001",
        "nodeagent_mobile_001",
    }
    required_panel_ids = {
        "panel_validation_report_001",
        "panel_project_export_001",
        "panel_optics_mode_001",
    }

    missing_orchestration_ids = required_orchestration_ids - orchestration_ids
    if missing_orchestration_ids:
        raise ValueError(
            f"Missing orchestration ids: {sorted(missing_orchestration_ids)}"
        )

    missing_node_agent_ids = required_node_agent_ids - node_agent_ids
    if missing_node_agent_ids:
        raise ValueError(
            f"Missing node agent ids: {sorted(missing_node_agent_ids)}"
        )

    missing_panel_ids = required_panel_ids - panel_ids
    if missing_panel_ids:
        raise ValueError(f"Missing panel ids: {sorted(missing_panel_ids)}")

    if "wrist_terminal_core_001" not in wrist_ids:
        raise ValueError("Expected wrist_terminal_core_001 in wrist contract")

    if "ar_glasses_display_core_001" not in ar_ids:
        raise ValueError("Expected ar_glasses_display_core_001 in AR contract")

    entries = (
        RealDashboardClientMobileEntry(
            real_client_entry_id="realclient_dashboard_001",
            client_kind="dashboard_client",
            linked_orchestration_entry_id="orchestration_control_plane_001",
            linked_node_agent_id="nodeagent_dev_001",
            linked_panel_id="panel_validation_report_001",
            linked_wrist_terminal_id=None,
            linked_ar_display_id=None,
            presentation_mode="read_only_dashboard",
            read_only_required=True,
            transport_path_required=True,
            explainable_required=True,
            production_path_allowed=True,
            client_runtime_status="active",
            description="Canonical real dashboard client entry.",
        ),
        RealDashboardClientMobileEntry(
            real_client_entry_id="realclient_mobile_001",
            client_kind="mobile_client",
            linked_orchestration_entry_id="orchestration_mobile_entry_001",
            linked_node_agent_id="nodeagent_mobile_001",
            linked_panel_id="panel_project_export_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            linked_ar_display_id=None,
            presentation_mode="mobile_proxy_view",
            read_only_required=True,
            transport_path_required=True,
            explainable_required=True,
            production_path_allowed=True,
            client_runtime_status="active",
            description="Canonical real mobile client entry.",
        ),
        RealDashboardClientMobileEntry(
            real_client_entry_id="realclient_ar_glasses_001",
            client_kind="ar_glasses_client",
            linked_orchestration_entry_id="orchestration_mobile_entry_001",
            linked_node_agent_id="nodeagent_mobile_001",
            linked_panel_id="panel_optics_mode_001",
            linked_wrist_terminal_id="wrist_terminal_core_001",
            linked_ar_display_id="ar_glasses_display_core_001",
            presentation_mode="private_spatial_view",
            read_only_required=True,
            transport_path_required=True,
            explainable_required=True,
            production_path_allowed=True,
            client_runtime_status="active",
            description="Canonical real AR glasses client entry.",
        ),
    )

    dashboard_entries = sum(
        1 for entry in entries if entry.client_kind == "dashboard_client"
    )
    mobile_entries = sum(
        1 for entry in entries if entry.client_kind == "mobile_client"
    )
    spatial_entries = sum(
        1 for entry in entries if entry.client_kind == "ar_glasses_client"
    )
    active_entries = sum(
        1 for entry in entries if entry.client_runtime_status == "active"
    )

    return RealDashboardClientsMobileContract(
        total_entries=len(entries),
        dashboard_entries=dashboard_entries,
        mobile_entries=mobile_entries,
        spatial_entries=spatial_entries,
        active_entries=active_entries,
        entries=entries,
    )
