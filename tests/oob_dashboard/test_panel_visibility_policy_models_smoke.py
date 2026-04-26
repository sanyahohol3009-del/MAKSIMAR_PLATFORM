from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_visibility_policy_models import (
    PanelVisibilityPolicyContract,
    PanelVisibilityPolicyEntry,
)


def test_panel_visibility_policy_entry_smoke() -> None:
    entry = PanelVisibilityPolicyEntry(
        panel_id="system_status",
        visibility_policy="always_visible",
        operator_visible=True,
        visible_in_navigation=True,
        visible_in_oob_dashboard=True,
        visible_in_main_dashboard=True,
        description="Visibility description.",
    )

    assert entry.panel_id == "system_status"


def test_panel_visibility_policy_contract_rejects_duplicates() -> None:
    entry_a = PanelVisibilityPolicyEntry(
        panel_id="system_status",
        visibility_policy="always_visible",
        operator_visible=True,
        visible_in_navigation=True,
        visible_in_oob_dashboard=True,
        visible_in_main_dashboard=True,
        description="A",
    )
    entry_b = PanelVisibilityPolicyEntry(
        panel_id="system_status",
        visibility_policy="always_visible",
        operator_visible=True,
        visible_in_navigation=True,
        visible_in_oob_dashboard=True,
        visible_in_main_dashboard=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        PanelVisibilityPolicyContract(entries=(entry_a, entry_b))
