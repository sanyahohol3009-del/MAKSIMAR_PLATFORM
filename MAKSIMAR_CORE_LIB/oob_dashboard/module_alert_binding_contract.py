from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.module_permission_matrix_contract import (
    build_module_permission_matrix_contract,
)

AlertChannel = Literal[
    "foundation_alert_channel",
    "interaction_alert_channel",
    "optional_alert_channel",
]

SeverityLevel = Literal[
    "info",
    "warning",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleAlertBindingEntry:
    alert_binding_id: str
    module_id: str
    alert_channel: AlertChannel
    severity_level: SeverityLevel
    audit_visible: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.alert_binding_id, "alert_binding_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.description, "description")

        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical module alert binding entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module alert binding entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module alert binding entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleAlertBindingContract:
    contract_id: str
    total_entries: int
    audit_visible_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[ModuleAlertBindingEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.audit_visible_entries != sum(
            1 for entry in self.entries if entry.audit_visible
        ):
            raise ValueError(
                "audit_visible_entries must match audit_visible count."
            )
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_module_alert_binding_contract() -> ModuleAlertBindingContract:
    permission_contract = build_module_permission_matrix_contract()

    channel_map = {
        "read_only": "foundation_alert_channel",
        "operator_interaction": "interaction_alert_channel",
        "optional_extension": "optional_alert_channel",
    }

    entries = tuple(
        ModuleAlertBindingEntry(
            alert_binding_id=f"module_alert_binding_{index:03d}",
            module_id=entry.module_id,
            alert_channel=channel_map[entry.permission_level],
            severity_level="warning" if entry.approval_required else "info",
            audit_visible=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical alert binding entry for {entry.module_id}.",
        )
        for index, entry in enumerate(permission_contract.entries, start=1)
    )

    return ModuleAlertBindingContract(
        contract_id="module_alert_binding_contract_001",
        total_entries=len(entries),
        audit_visible_entries=sum(1 for entry in entries if entry.audit_visible),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
