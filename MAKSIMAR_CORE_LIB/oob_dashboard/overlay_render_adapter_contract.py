from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_overlay_backend_contract import (
    build_visual_overlay_backend_contract,
)

OverlayAdapterMode = Literal[
    "canonical_to_overlay_backend",
]

_ALLOWED_OVERLAY_ADAPTER_MODES: tuple[OverlayAdapterMode, ...] = (
    "canonical_to_overlay_backend",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OverlayRenderAdapterEntry:
    adapter_entry_id: str
    backend_id: str
    adapter_target: str
    adapter_mode: OverlayAdapterMode
    canonical_id_preserved: bool
    vendor_overlay_exposed: bool
    truth_leakage_allowed: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.adapter_target, "adapter_target")
        _require_non_empty(self.description, "description")

        if self.adapter_mode not in _ALLOWED_OVERLAY_ADAPTER_MODES:
            raise ValueError(
                f"adapter_mode must be one of {_ALLOWED_OVERLAY_ADAPTER_MODES}, got {self.adapter_mode!r}."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical overlay render adapter entries."
            )
        if self.vendor_overlay_exposed:
            raise ValueError(
                "vendor_overlay_exposed must remain false for canonical overlay render adapter entries."
            )
        if self.truth_leakage_allowed:
            raise ValueError(
                "truth_leakage_allowed must remain false for canonical overlay render adapter entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical overlay render adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical overlay render adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical overlay render adapter entries."
            )


@dataclass(frozen=True, slots=True)
class OverlayRenderAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[OverlayRenderAdapterEntry, ...]

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


def build_overlay_render_adapter_contract() -> OverlayRenderAdapterContract:
    overlay_backend = build_visual_overlay_backend_contract()

    entries = (
        OverlayRenderAdapterEntry(
            adapter_entry_id="overlay_render_adapter_001",
            backend_id=overlay_backend.backend_id,
            adapter_target="signal_overlay_projection",
            adapter_mode="canonical_to_overlay_backend",
            canonical_id_preserved=True,
            vendor_overlay_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical overlay adapter entry for signal overlay projection.",
        ),
        OverlayRenderAdapterEntry(
            adapter_entry_id="overlay_render_adapter_002",
            backend_id=overlay_backend.backend_id,
            adapter_target="topology_overlay_projection",
            adapter_mode="canonical_to_overlay_backend",
            canonical_id_preserved=True,
            vendor_overlay_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical overlay adapter entry for topology overlay projection.",
        ),
        OverlayRenderAdapterEntry(
            adapter_entry_id="overlay_render_adapter_003",
            backend_id=overlay_backend.backend_id,
            adapter_target="explainability_overlay_projection",
            adapter_mode="canonical_to_overlay_backend",
            canonical_id_preserved=True,
            vendor_overlay_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical overlay adapter entry for explainability overlay projection.",
        ),
    )

    return OverlayRenderAdapterContract(
        contract_id="overlay_render_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
