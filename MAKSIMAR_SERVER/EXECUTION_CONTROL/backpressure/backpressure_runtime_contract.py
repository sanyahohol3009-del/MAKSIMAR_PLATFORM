from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_pressure_decision_contract,
    build_pressure_signal_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.backpressure.backpressure_runtime_models import (
    ServerBackpressureRuntimeContract,
    ServerBackpressureRuntimeEntry,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_multi_node_health_registry_contract,
)


def _pressure_level_rank(level: str) -> int:
    """Return sortable rank for pressure level."""
    if level == "normal":
        return 0
    if level == "elevated":
        return 1
    if level == "high":
        return 2
    return 3


def _resolve_level_from_signal_value(
    *,
    signal_kind: str,
    observed_value: int,
) -> str:
    """Resolve pressure level from canonical signal thresholds."""
    signal_contract = build_pressure_signal_contract()
    signal_entry = next(
        entry for entry in signal_contract.signals if entry.signal_kind == signal_kind
    )

    if observed_value >= signal_entry.critical_threshold:
        return "critical"
    if observed_value >= signal_entry.high_threshold:
        return "high"
    if observed_value >= signal_entry.elevated_threshold:
        return "elevated"
    return signal_entry.default_level_below_elevated


def build_server_backpressure_runtime_contract() -> ServerBackpressureRuntimeContract:
    """Build server-side backpressure runtime contract."""
    health_registry = build_multi_node_health_registry_contract()
    pressure_decisions = build_pressure_decision_contract()

    decisions_by_level = {
        entry.pressure_level: entry for entry in pressure_decisions.rules
    }

    entries: list[ServerBackpressureRuntimeEntry] = []

    for node in health_registry.nodes:
        observed_signals = (
            ("cpu_pressure", node.cpu_pressure_percent),
            ("ram_pressure", node.ram_pressure_percent),
            ("queue_pressure", node.queue_depth),
        )

        resolved_signals = tuple(
            (
                signal_kind,
                observed_value,
                _resolve_level_from_signal_value(
                    signal_kind=signal_kind,
                    observed_value=observed_value,
                ),
            )
            for signal_kind, observed_value in observed_signals
        )

        primary_signal_kind, primary_signal_value, pressure_level = max(
            resolved_signals,
            key=lambda item: (
                _pressure_level_rank(item[2]),
                item[1],
                item[0],
            ),
        )

        if node.health_state == "critical" or node.connectivity_state == "offline":
            pressure_level = "critical"
            primary_signal_kind = "queue_pressure"
            primary_signal_value = max(node.queue_depth, primary_signal_value)

        decision = decisions_by_level[pressure_level]

        throttling_active = decision.admission_decision in (
            "accept_with_throttle",
            "delay_new_work",
            "reject_new_work",
        )
        overload_protection_active = pressure_level in ("high", "critical")

        entries.append(
            ServerBackpressureRuntimeEntry(
                node_id=node.node_id,
                pressure_level=pressure_level,  # type: ignore[arg-type]
                primary_signal_kind=primary_signal_kind,  # type: ignore[arg-type]
                primary_signal_value=primary_signal_value,
                primary_action=decision.primary_action,
                admission_decision=decision.admission_decision,
                throttling_active=throttling_active,
                degraded_mode_required=decision.degraded_mode_required,
                remote_reroute_preferred=decision.remote_reroute_preferred,
                overload_protection_active=overload_protection_active,
                reason=(
                    f"primary_signal={primary_signal_kind};"
                    f"value={primary_signal_value};"
                    f"resolved_level={pressure_level}"
                ),
            )
        )

    return ServerBackpressureRuntimeContract(
        total_entries=len(entries),
        entries=tuple(entries),
    )
