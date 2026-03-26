from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.degraded_mode_models import (
    DegradedModeContract,
    DegradedModeRule,
)


def build_degraded_mode_contract() -> DegradedModeContract:
    """Build unified degraded mode contract."""

    rules = (
        DegradedModeRule(
            disabled_feature="voice_duplex",
            safety_critical=False,
            remains_active=False,
        ),
        DegradedModeRule(
            disabled_feature="heavy_render",
            safety_critical=False,
            remains_active=False,
        ),
        DegradedModeRule(
            disabled_feature="background_indexing",
            safety_critical=False,
            remains_active=False,
        ),
        DegradedModeRule(
            disabled_feature="chat_and_safety",
            safety_critical=True,
            remains_active=True,
        ),
    )

    return DegradedModeContract(
        total_rules=len(rules),
        rules=rules,
    )
