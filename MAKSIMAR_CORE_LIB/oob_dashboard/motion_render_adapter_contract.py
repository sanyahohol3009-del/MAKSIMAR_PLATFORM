from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

MotionAdapterMode = Literal[
    "canonical_to_motion_backend",
]

_ALLOWED_MOTION_ADAPTER_MODES: tuple[MotionAdapterMode, ...] = (
    "canonical_to_motion_backend",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MotionRenderAdapterEntry:
    adapter_entry_id: str
    adapter_target: str
    adapter_mode: MotionAdapterMode
    motion_policy_id: str
    canonical_id_preserved: bool
    vendor_motion_exposed: bool
    truth_leakage_allowed: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.adapter_target, "adapter_target")
        _require_non_empty(self.motion_policy_id, "motion_policy_id")
        _require_non_empty(self.description, "description")

        if self.adapter_mode not in _ALLOWED_MOTION_ADAPTER_MODES:
            raise ValueError(
                f"adapter_mode must be one of {_ALLOWED_MOTION_ADAPTER_MODES}, got {self.adapter_mode!r}."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical motion render adapter entries."
            )
        if self.vendor_motion_exposed:
            raise ValueError(
                "vendor_motion_exposed must remain false for canonical motion render adapter entries."
            )
        if self.truth_leakage_allowed:
            raise ValueError(
                "truth_leakage_allowed must remain false for canonical motion render adapter entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical motion render adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical motion render adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical motion render adapter entries."
            )


@dataclass(frozen=True, slots=True)
class MotionRenderAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[MotionRenderAdapterEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.replaceable_entries != sum(
            1 for entry in self.entries if entry.replaceable
        ):
            raise ValueError("replaceable_entries must match replaceable count.")
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


def build_motion_render_adapter_contract() -> MotionRenderAdapterContract:
    entries = (
        MotionRenderAdapterEntry(
            adapter_entry_id="motion_render_adapter_001",
            adapter_target="hud_transition_projection",
            adapter_mode="canonical_to_motion_backend",
            motion_policy_id="motion_policy_hud_transition",
            canonical_id_preserved=True,
            vendor_motion_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical motion adapter entry for HUD transition projection.",
        ),
        MotionRenderAdapterEntry(
            adapter_entry_id="motion_render_adapter_002",
            adapter_target="status_pulse_projection",
            adapter_mode="canonical_to_motion_backend",
            motion_policy_id="motion_policy_status_pulse",
            canonical_id_preserved=True,
            vendor_motion_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical motion adapter entry for status pulse projection.",
        ),
        MotionRenderAdapterEntry(
            adapter_entry_id="motion_render_adapter_003",
            adapter_target="panel_reveal_projection",
            adapter_mode="canonical_to_motion_backend",
            motion_policy_id="motion_policy_panel_reveal",
            canonical_id_preserved=True,
            vendor_motion_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical motion adapter entry for panel reveal projection.",
        ),
    )

    return MotionRenderAdapterContract(
        contract_id="motion_render_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
