from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

VisualBackendType = Literal[
    "graph_backend",
    "chart_backend",
    "overlay_backend",
]

_ALLOWED_VISUAL_BACKEND_TYPES: tuple[VisualBackendType, ...] = (
    "graph_backend",
    "chart_backend",
    "overlay_backend",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBackendEntry:
    backend_id: str
    backend_name: str
    backend_type: VisualBackendType
    backend_vendor_mode: str
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.backend_name, "backend_name")
        _require_non_empty(self.backend_vendor_mode, "backend_vendor_mode")
        _require_non_empty(self.description, "description")

        if self.backend_type not in _ALLOWED_VISUAL_BACKEND_TYPES:
            raise ValueError(
                f"backend_type must be one of {_ALLOWED_VISUAL_BACKEND_TYPES}, got {self.backend_type!r}."
            )
        if self.backend_vendor_mode != "optional_external_backend":
            raise ValueError(
                "backend_vendor_mode must remain optional_external_backend for canonical visual backend entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical visual backend entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual backend entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual backend entries."
            )


@dataclass(frozen=True, slots=True)
class VisualBackendContract:
    contract_id: str
    total_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualBackendEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.replaceable_entries != sum(
            1 for entry in self.entries if entry.replaceable
        ):
            raise ValueError(
                "replaceable_entries must match replaceable count."
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
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )


def build_visual_backend_contract() -> VisualBackendContract:
    entries = (
        VisualBackendEntry(
            backend_id="visual_backend_graph_001",
            backend_name="react_flow_adapter_backend",
            backend_type="graph_backend",
            backend_vendor_mode="optional_external_backend",
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceable graph backend entry.",
        ),
        VisualBackendEntry(
            backend_id="visual_backend_chart_001",
            backend_name="echarts_adapter_backend",
            backend_type="chart_backend",
            backend_vendor_mode="optional_external_backend",
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceable chart backend entry.",
        ),
        VisualBackendEntry(
            backend_id="visual_backend_overlay_001",
            backend_name="internal_overlay_adapter_backend",
            backend_type="overlay_backend",
            backend_vendor_mode="optional_external_backend",
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical replaceable overlay backend entry.",
        ),
    )

    return VisualBackendContract(
        contract_id="visual_backend_contract_001",
        total_entries=len(entries),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
