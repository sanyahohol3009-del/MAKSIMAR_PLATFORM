from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_panel_registry_contract,
)


@dataclass(frozen=True, slots=True)
class PanelRegistryReadRow:
    """Read-only row used for terminal/operator preview."""

    panel_id: str
    title: str
    panel_family: str
    panel_kind: str
    source_binding_required: bool
    visibility_policy_required: bool


@dataclass(frozen=True, slots=True)
class PanelRegistryReadModel:
    """Read-only registry view for operator/developer inspection."""

    rows: tuple[PanelRegistryReadRow, ...]

    def __post_init__(self) -> None:
        """Validate read-model invariants."""
        if not self.rows:
            raise ValueError("rows must not be empty")


def build_panel_registry_read_model() -> PanelRegistryReadModel:
    """Build the canonical panel registry read model."""
    registry = build_panel_registry_contract()

    rows = tuple(
        PanelRegistryReadRow(
            panel_id=entry.panel_id,
            title=entry.title,
            panel_family=entry.panel_family,
            panel_kind=entry.panel_kind,
            source_binding_required=entry.source_binding_required,
            visibility_policy_required=entry.visibility_policy_required,
        )
        for entry in registry.entries
    )

    return PanelRegistryReadModel(rows=rows)
