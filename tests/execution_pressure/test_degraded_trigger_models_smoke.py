from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_degraded_trigger_contract,
)


def test_degraded_trigger_contract_builds() -> None:
    """Degraded trigger contract should build successfully."""
    contract = build_degraded_trigger_contract()

    assert contract.total_triggers == 4
    assert len(contract.triggers) == 4


def test_degraded_trigger_contract_contains_expected_levels() -> None:
    """Degraded trigger contract should expose expected pressure levels."""
    contract = build_degraded_trigger_contract()

    assert contract.triggers[0].pressure_level == "normal"
    assert contract.triggers[1].pressure_level == "elevated"
    assert contract.triggers[2].pressure_level == "high"
    assert contract.triggers[3].pressure_level == "critical"


def test_degraded_trigger_contract_enforces_high_and_critical_activation() -> None:
    """High and critical pressure should activate degraded triggers."""
    contract = build_degraded_trigger_contract()

    high = contract.triggers[2]
    critical = contract.triggers[3]

    assert high.trigger_enabled is True
    assert high.trigger_scope == "selective_reduction"
    assert high.routing_policy == "prefer_remote_reroute"

    assert critical.trigger_enabled is True
    assert critical.trigger_scope == "broad_protection"
    assert critical.routing_policy == "force_remote_reroute_when_available"


def test_degraded_trigger_contract_keeps_normal_and_elevated_disabled() -> None:
    """Normal and elevated pressure should not activate degraded triggers."""
    contract = build_degraded_trigger_contract()

    normal = contract.triggers[0]
    elevated = contract.triggers[1]

    assert normal.trigger_enabled is False
    assert normal.trigger_scope == "none"
    assert elevated.trigger_enabled is False
    assert elevated.trigger_scope == "none"
