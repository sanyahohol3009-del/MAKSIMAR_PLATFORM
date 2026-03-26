from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_degraded_mode_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.degraded_mode_panel_models import (
    DegradedModePanelContract,
    DegradedModePanelEntry,
)


def build_degraded_mode_panel_contract() -> DegradedModePanelContract:
    """Build unified read-only degraded mode panel contract."""
    degraded_contract = build_degraded_mode_contract()

    entries = tuple(
        DegradedModePanelEntry(
            disabled_feature=rule.disabled_feature,
            safety_critical=rule.safety_critical,
            remains_active=rule.remains_active,
        )
        for rule in degraded_contract.rules
    )

    return DegradedModePanelContract(
        panel_id="panel_degraded_mode",
        total_entries=len(entries),
        entries=entries,
    )
