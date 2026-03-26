from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_feature_gating_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_contract import (
    build_multi_node_health_registry_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.workload_placement_models import (
    DistributedWorkloadPlacementContract,
    DistributedWorkloadPlacementEntry,
)


@dataclass(frozen=True, slots=True)
class _PlacementCandidate:
    """Internal placement candidate."""

    node_id: str
    health_state: str
    connectivity_state: str
    queue_depth: int
    health_score: int
    feature_availability: str


def _availability_rank(availability: str) -> int:
    """Return sort rank for feature availability."""
    if availability == "supported":
        return 0
    if availability == "degraded":
        return 1
    return 2


def _health_rank(health_state: str) -> int:
    """Return sort rank for node health."""
    if health_state == "healthy":
        return 0
    if health_state == "warning":
        return 1
    return 2


def _select_best_candidate(
    *,
    feature_id: str,
) -> DistributedWorkloadPlacementEntry:
    """Select best node for a workload using health and feature-gating data."""
    health_registry = build_multi_node_health_registry_contract()
    feature_gating = build_feature_gating_contract()

    health_by_node = {entry.node_id: entry for entry in health_registry.nodes}
    candidates: list[_PlacementCandidate] = []

    for entry in feature_gating.entries:
        if entry.feature_id != feature_id:
            continue

        node_health = health_by_node[entry.node_id]

        if node_health.connectivity_state == "offline":
            continue
        if node_health.health_state == "critical":
            continue

        candidates.append(
            _PlacementCandidate(
                node_id=entry.node_id,
                health_state=node_health.health_state,
                connectivity_state=node_health.connectivity_state,
                queue_depth=node_health.queue_depth,
                health_score=node_health.health_score,
                feature_availability=entry.availability,
            )
        )

    candidates.sort(
        key=lambda item: (
            _availability_rank(item.feature_availability),
            _health_rank(item.health_state),
            item.queue_depth,
            -item.health_score,
            item.node_id,
        )
    )

    if not candidates:
        return DistributedWorkloadPlacementEntry(
            workload_id=f"placement_{feature_id}",
            workload_kind=feature_id,  # type: ignore[arg-type]
            selected_node_id="unavailable",
            decision_status="unavailable",
            reason="no_eligible_nodes",
            selected_node_health_state="critical",
            selected_feature_availability="unsupported",
        )

    selected = candidates[0]

    decision_status = "selected"
    reason = "best_runtime_match"

    if selected.feature_availability == "degraded":
        decision_status = "degraded_selected"
        reason = "selected_under_degraded_capability"

    return DistributedWorkloadPlacementEntry(
        workload_id=f"placement_{feature_id}",
        workload_kind=feature_id,  # type: ignore[arg-type]
        selected_node_id=selected.node_id,
        decision_status=decision_status,
        reason=reason,
        selected_node_health_state=selected.health_state,
        selected_feature_availability=selected.feature_availability,
    )


def build_distributed_workload_placement_contract() -> (
    DistributedWorkloadPlacementContract
):
    """Build distributed workload placement contract."""
    decisions = (
        _select_best_candidate(feature_id="ai_chat"),
        _select_best_candidate(feature_id="media_render"),
        _select_best_candidate(feature_id="simulation_task"),
    )

    return DistributedWorkloadPlacementContract(
        total_decisions=len(decisions),
        decisions=decisions,
    )
