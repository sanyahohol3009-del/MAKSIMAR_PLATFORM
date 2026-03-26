from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.backpressure import (
    build_server_backpressure_runtime_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.degraded_mode import (
    build_degraded_mode_runtime_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_multi_node_health_registry_contract,
)
from MAKSIMAR_SERVER.RUNTIME.pressure_state.pressure_state_runtime_models import (
    PressureStateRuntimeContract,
    PressureStateRuntimeEntry,
)


def _resolve_runtime_state(
    *,
    pressure_level: str,
    degraded_mode_active: bool,
    throttling_active: bool,
    overload_protection_active: bool,
) -> str:
    """Resolve runtime pressure state from backpressure and degraded mode signals."""
    if pressure_level == "critical":
        return "protected"
    if pressure_level == "high":
        return "degraded"
    if pressure_level == "elevated":
        return "throttled"
    return "open"


def build_pressure_state_runtime_contract() -> PressureStateRuntimeContract:
    """Build unified server-side pressure state runtime contract."""
    backpressure = build_server_backpressure_runtime_contract()
    degraded_mode = build_degraded_mode_runtime_contract()
    health_registry = build_multi_node_health_registry_contract()

    degraded_by_node = {
        entry.node_id: entry for entry in degraded_mode.entries
    }
    health_by_node = {
        entry.node_id: entry for entry in health_registry.nodes
    }

    entries = []
    for backpressure_entry in backpressure.entries:
        degraded_entry = degraded_by_node[backpressure_entry.node_id]
        health_entry = health_by_node[backpressure_entry.node_id]

        runtime_state = _resolve_runtime_state(
            pressure_level=backpressure_entry.pressure_level,
            degraded_mode_active=degraded_entry.degraded_mode_active,
            throttling_active=backpressure_entry.throttling_active,
            overload_protection_active=backpressure_entry.overload_protection_active,
        )

        entries.append(
            PressureStateRuntimeEntry(
                node_id=backpressure_entry.node_id,
                pressure_level=backpressure_entry.pressure_level,
                runtime_state=runtime_state,  # type: ignore[arg-type]
                primary_signal_kind=backpressure_entry.primary_signal_kind,
                primary_signal_value=backpressure_entry.primary_signal_value,
                admission_decision=backpressure_entry.admission_decision,
                throttling_active=backpressure_entry.throttling_active,
                degraded_mode_active=degraded_entry.degraded_mode_active,
                overload_protection_active=backpressure_entry.overload_protection_active,
                health_state=health_entry.health_state,  # type: ignore[arg-type]
                queue_depth=health_entry.queue_depth,
                reason=(
                    f"pressure_level={backpressure_entry.pressure_level};"
                    f"runtime_state={runtime_state};"
                    f"degraded_mode_active={degraded_entry.degraded_mode_active}"
                ),
            )
        )

    elevated_or_higher_entries = sum(
        1
        for entry in entries
        if entry.pressure_level in ("elevated", "high", "critical")
    )
    degraded_active_entries = sum(
        1 for entry in entries if entry.degraded_mode_active
    )

    return PressureStateRuntimeContract(
        total_entries=len(entries),
        elevated_or_higher_entries=elevated_or_higher_entries,
        degraded_active_entries=degraded_active_entries,
        entries=tuple(entries),
    )
