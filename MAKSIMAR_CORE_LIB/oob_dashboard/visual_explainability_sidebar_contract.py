from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualExplainabilitySidebarEntry:
    explainability_sidebar_entry_id: str
    panel_id: str
    explainability_enabled: bool
    sidebar_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.explainability_sidebar_entry_id,
            "explainability_sidebar_entry_id",
        )
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if not self.explainability_enabled:
            raise ValueError(
                "explainability_enabled must remain true for canonical visual explainability sidebar entries."
            )
        if not self.sidebar_ready:
            raise ValueError(
                "sidebar_ready must remain true for canonical visual explainability sidebar entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual explainability sidebar entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual explainability sidebar entries."
            )


@dataclass(frozen=True, slots=True)
class VisualExplainabilitySidebarContract:
    contract_id: str
    total_entries: int
    sidebar_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VisualExplainabilitySidebarEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.sidebar_ready_entries != sum(
            1 for entry in self.entries if entry.sidebar_ready
        ):
            raise ValueError("sidebar_ready_entries must match sidebar_ready count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_visual_explainability_sidebar_contract() -> VisualExplainabilitySidebarContract:
    mapping_contract = build_panel_to_visual_mapping_contract()

    entries = tuple(
        VisualExplainabilitySidebarEntry(
            explainability_sidebar_entry_id=(
                f"visual_explainability_sidebar_{index:03d}"
            ),
            panel_id=entry.panel_id,
            explainability_enabled=True,
            sidebar_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical visual explainability sidebar entry for {entry.panel_id}.",
        )
        for index, entry in enumerate(mapping_contract.entries, start=1)
        if entry.explainability_enabled
    )

    return VisualExplainabilitySidebarContract(
        contract_id="visual_explainability_sidebar_contract_001",
        total_entries=len(entries),
        sidebar_ready_entries=sum(1 for entry in entries if entry.sidebar_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
