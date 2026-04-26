from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_models import (
    PanelBindingContract,
    PanelBindingEntry,
)


def test_panel_binding_entry_smoke() -> None:
    entry = PanelBindingEntry(
        panel_id="system_status",
        display_target_id="display_foundation_primary",
        binding_reason="foundation_visibility",
        is_default_target=True,
        eligible_for_main_dashboard=True,
        eligible_for_oob_dashboard=True,
        description="Binding description.",
    )

    assert entry.panel_id == "system_status"


def test_panel_binding_contract_rejects_duplicates() -> None:
    entry_a = PanelBindingEntry(
        panel_id="system_status",
        display_target_id="display_foundation_primary",
        binding_reason="foundation_visibility",
        is_default_target=True,
        eligible_for_main_dashboard=True,
        eligible_for_oob_dashboard=True,
        description="A",
    )
    entry_b = PanelBindingEntry(
        panel_id="system_status",
        display_target_id="display_foundation_primary",
        binding_reason="foundation_visibility",
        is_default_target=True,
        eligible_for_main_dashboard=True,
        eligible_for_oob_dashboard=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelBindingContract(entries=(entry_a, entry_b))
