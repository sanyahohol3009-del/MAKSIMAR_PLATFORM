from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_models import (
    PanelRegistryContract,
    PanelRegistryEntry,
)


def test_panel_registry_entry_smoke() -> None:
    entry = PanelRegistryEntry(
        panel_id="system_status",
        title="System Status",
        panel_family="foundation",
        panel_kind="status",
        source_binding_required=True,
        visibility_policy_required=True,
    )

    assert entry.panel_id == "system_status"
    assert entry.title == "System Status"


def test_panel_registry_entry_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title must not be empty"):
        PanelRegistryEntry(
            panel_id="system_status",
            title="",
            panel_family="foundation",
            panel_kind="status",
            source_binding_required=True,
            visibility_policy_required=True,
        )


def test_panel_registry_contract_rejects_duplicate_ids() -> None:
    entry_a = PanelRegistryEntry(
        panel_id="system_status",
        title="System Status",
        panel_family="foundation",
        panel_kind="status",
        source_binding_required=True,
        visibility_policy_required=True,
    )
    entry_b = PanelRegistryEntry(
        panel_id="system_status",
        title="System Status Copy",
        panel_family="foundation",
        panel_kind="status",
        source_binding_required=True,
        visibility_policy_required=True,
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelRegistryContract(entries=(entry_a, entry_b))
