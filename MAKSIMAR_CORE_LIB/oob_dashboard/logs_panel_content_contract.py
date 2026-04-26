from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_diagnostics_correlation_view import (
    build_foundation_diagnostics_correlation_view,
)


LogsPanelState = Literal[
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
]

ALL_LOGS_PANEL_STATES: tuple[LogsPanelState, ...] = (
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class LogsPanelContentEntry:
    """Canonical content entry for the logs panel."""

    panel_id: str
    panel_state: LogsPanelState
    total_log_related_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    source_file_visible_entries: int
    failure_visible_entries: int
    incident_visible_entries: int
    stalled_stage_visible_entries: int
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.panel_state not in ALL_LOGS_PANEL_STATES:
            raise ValueError(
                "panel_state must be one of "
                f"{ALL_LOGS_PANEL_STATES}, got {self.panel_state!r}."
            )

        integer_fields = {
            "total_log_related_entries": self.total_log_related_entries,
            "critical_entries": self.critical_entries,
            "warning_entries": self.warning_entries,
            "info_entries": self.info_entries,
            "source_file_visible_entries": self.source_file_visible_entries,
            "failure_visible_entries": self.failure_visible_entries,
            "incident_visible_entries": self.incident_visible_entries,
            "stalled_stage_visible_entries": self.stalled_stage_visible_entries,
        }
        for field_name, field_value in integer_fields.items():
            if field_value < 0:
                raise ValueError(f"{field_name} must be >= 0.")

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical logs content."
            )

        if not self.visible_in_oob_dashboard:
            raise ValueError(
                "visible_in_oob_dashboard must remain true for canonical logs content."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical logs content."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical logs content."
            )


@dataclass(frozen=True, slots=True)
class LogsPanelContentContract:
    """Canonical content contract for the logs panel."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    operator_visible_entries: int
    entries: tuple[LogsPanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_entries != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_entries must match read_only count.")

        if self.main_dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_main_dashboard
        ):
            raise ValueError(
                "main_dashboard_visible_entries must match visible_in_main_dashboard count."
            )

        if self.oob_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_oob_dashboard
        ):
            raise ValueError(
                "oob_visible_entries must match visible_in_oob_dashboard count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def _derive_logs_panel_state(
    total_entries: int,
    critical_entries: int,
    warning_entries: int,
    source_file_visible_entries: int,
) -> LogsPanelState:
    if total_entries == 0:
        return "empty"
    if source_file_visible_entries == 0:
        return "loading"
    if critical_entries > 0:
        return "incident"
    if warning_entries > 0:
        return "degraded"
    return "normal"


def build_logs_panel_content_contract() -> LogsPanelContentContract:
    """Build canonical content contract for the logs panel."""
    diagnostics_view = build_foundation_diagnostics_correlation_view()

    entry = LogsPanelContentEntry(
        panel_id="logs",
        panel_state=_derive_logs_panel_state(
            total_entries=diagnostics_view.total_entries,
            critical_entries=sum(
                1 for item in diagnostics_view.entries if item.severity == "critical"
            ),
            warning_entries=sum(
                1 for item in diagnostics_view.entries if item.severity == "warning"
            ),
            source_file_visible_entries=sum(
                1 for item in diagnostics_view.entries if item.suspected_source_file != "unknown"
            ),
        ),
        total_log_related_entries=diagnostics_view.total_entries,
        critical_entries=sum(
            1 for item in diagnostics_view.entries if item.severity == "critical"
        ),
        warning_entries=sum(
            1 for item in diagnostics_view.entries if item.severity == "warning"
        ),
        info_entries=sum(
            1 for item in diagnostics_view.entries if item.severity == "info"
        ),
        source_file_visible_entries=sum(
            1
            for item in diagnostics_view.entries
            if item.suspected_source_file != "unknown"
        ),
        failure_visible_entries=diagnostics_view.failure_visible_entries,
        incident_visible_entries=diagnostics_view.incident_visible_entries,
        stalled_stage_visible_entries=sum(
            1 for item in diagnostics_view.entries if item.stalled_stage_visible
        ),
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical logs panel content contract built from "
            "foundation diagnostics correlation view."
        ),
    )

    entries = (entry,)

    return LogsPanelContentContract(
        contract_id="logs_panel_content_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for item in entries if item.read_only),
        main_dashboard_visible_entries=sum(
            1 for item in entries if item.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for item in entries if item.visible_in_oob_dashboard
        ),
        operator_visible_entries=sum(
            1 for item in entries if item.operator_visible
        ),
        entries=entries,
    )
