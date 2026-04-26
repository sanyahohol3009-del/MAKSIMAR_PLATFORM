from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.display_runtime_resolver_models import (
    DisplayRuntimeResolverContract,
    DisplayRuntimeResolverEntry,
)


def test_display_runtime_resolver_entry_smoke() -> None:
    entry = DisplayRuntimeResolverEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        resolved_display_role="foundation_primary_display",
        resolved_display_zone="foundation_main_zone",
        fallback_display_target_id="display_foundation_secondary",
        description="Resolver description.",
    )

    assert entry.panel_id == "system_status"


def test_display_runtime_resolver_contract_rejects_duplicates() -> None:
    entry_a = DisplayRuntimeResolverEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        resolved_display_role="foundation_primary_display",
        resolved_display_zone="foundation_main_zone",
        fallback_display_target_id="display_foundation_secondary",
        description="A",
    )
    entry_b = DisplayRuntimeResolverEntry(
        panel_id="system_status",
        view_id="view_foundation_status",
        display_target_id="display_foundation_primary",
        resolved_display_role="foundation_primary_display",
        resolved_display_zone="foundation_main_zone",
        fallback_display_target_id="display_foundation_secondary",
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate panel_id detected"):
        DisplayRuntimeResolverContract(entries=(entry_a, entry_b))
