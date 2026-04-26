from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class SecurityTelemetryPanelEntry:
    telemetry_id: str
    telemetry_scope: str
    security_state: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.telemetry_id, "telemetry_id")
        _require_non_empty(self.telemetry_scope, "telemetry_scope")
        _require_non_empty(self.security_state, "security_state")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical security-telemetry panel entries."
            )


@dataclass(frozen=True, slots=True)
class SecurityTelemetryPanelContract:
    panel_id: str
    total_entries: int
    operator_visible_entries: int
    entries: Tuple[SecurityTelemetryPanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical security-telemetry panel contract."
            )


def build_security_telemetry_panel_contract() -> SecurityTelemetryPanelContract:
    entries = (
        SecurityTelemetryPanelEntry(
            telemetry_id="security_telemetry_guard_chain",
            telemetry_scope="guard_chain",
            security_state="stable",
            operator_visible=True,
            description="Canonical guard-chain security telemetry state.",
        ),
        SecurityTelemetryPanelEntry(
            telemetry_id="security_telemetry_audit_path",
            telemetry_scope="audit_path",
            security_state="visible_and_intact",
            operator_visible=True,
            description="Canonical audit-path security telemetry state.",
        ),
        SecurityTelemetryPanelEntry(
            telemetry_id="security_telemetry_consent_boundary",
            telemetry_scope="consent_boundary",
            security_state="enforced",
            operator_visible=True,
            description="Canonical consent-boundary security telemetry state.",
        ),
    )

    return SecurityTelemetryPanelContract(
        panel_id="panel_security_telemetry",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical security-telemetry panel contract.",
    )
