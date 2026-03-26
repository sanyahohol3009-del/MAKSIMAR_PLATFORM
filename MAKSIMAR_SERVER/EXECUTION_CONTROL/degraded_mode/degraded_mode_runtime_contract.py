from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_degraded_trigger_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.backpressure import (
    build_server_backpressure_runtime_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.degraded_mode.degraded_mode_runtime_models import (
    DegradedModeRuntimeContract,
    DegradedModeRuntimeEntry,
)


def build_degraded_mode_runtime_contract() -> DegradedModeRuntimeContract:
    """Build server-side degraded mode runtime contract."""
    backpressure = build_server_backpressure_runtime_contract()
    degraded_triggers = build_degraded_trigger_contract()

    trigger_by_level = {
        entry.pressure_level: entry for entry in degraded_triggers.triggers
    }

    entries = []
    for runtime_entry in backpressure.entries:
        trigger = trigger_by_level[runtime_entry.pressure_level]

        degraded_mode_active = (
            runtime_entry.degraded_mode_required
            and trigger.trigger_enabled
        )

        trigger_scope = (
            trigger.trigger_scope
            if degraded_mode_active
            else "none"
        )
        feature_reduction_active = (
            trigger.feature_reduction_required
            if degraded_mode_active
            else False
        )
        routing_policy = (
            trigger.routing_policy
            if degraded_mode_active
            else "no_reroute"
        )
        observability_alert_active = (
            trigger.observability_alert_required
            if degraded_mode_active
            else False
        )

        entries.append(
            DegradedModeRuntimeEntry(
                node_id=runtime_entry.node_id,
                pressure_level=runtime_entry.pressure_level,
                degraded_mode_active=degraded_mode_active,
                trigger_scope=trigger_scope,  # type: ignore[arg-type]
                feature_reduction_active=feature_reduction_active,
                routing_policy=routing_policy,  # type: ignore[arg-type]
                observability_alert_active=observability_alert_active,
                reason=(
                    f"pressure_level={runtime_entry.pressure_level};"
                    f"trigger_enabled={trigger.trigger_enabled};"
                    f"degraded_mode_required={runtime_entry.degraded_mode_required}"
                ),
            )
        )

    active_entries = sum(1 for entry in entries if entry.degraded_mode_active)

    return DegradedModeRuntimeContract(
        total_entries=len(entries),
        active_entries=active_entries,
        entries=tuple(entries),
    )
