from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.feature_gating_models import (
    FeatureGateEntry,
    FeatureGatingContract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.advanced_memory_profile_contract import (
    build_advanced_memory_profile_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.multi_gpu_profile_contract import (
    build_multi_gpu_profile_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.node_runtime_health_contract import (
    build_node_runtime_health_contract,
)


def build_feature_gating_contract() -> FeatureGatingContract:
    """Build feature-gating contract from detected runtime capabilities."""
    runtime = build_node_runtime_health_contract()
    memory = build_advanced_memory_profile_contract()
    gpu = build_multi_gpu_profile_contract()

    memory_by_node = {entry.node_id: entry for entry in memory.nodes}
    gpu_by_node = {entry.node_id: entry for entry in gpu.nodes}

    entries: list[FeatureGateEntry] = []

    for node in runtime.nodes:
        memory_profile = memory_by_node[node.node_id]
        gpu_profile = gpu_by_node[node.node_id]

        ai_chat_availability = "supported"
        ai_chat_reason = "baseline_runtime_available"

        if node.ram_total_gb < 8:
            ai_chat_availability = "degraded"
            ai_chat_reason = "limited_system_memory"

        if node.health_score < 50:
            ai_chat_availability = "degraded"
            ai_chat_reason = "low_runtime_health"

        entries.append(
            FeatureGateEntry(
                node_id=node.node_id,
                feature_id="ai_chat",
                availability=ai_chat_availability,
                reason=ai_chat_reason,
            )
        )

        media_render_availability = "supported"
        media_render_reason = "gpu_and_memory_requirements_met"

        if gpu_profile.gpu_count == 0:
            media_render_availability = "degraded"
            media_render_reason = "no_detected_gpu"

        if memory_profile.ram_total_gb < 16:
            media_render_availability = "degraded"
            media_render_reason = "limited_system_memory_for_render"

        if node.health_score < 40:
            media_render_availability = "unsupported"
            media_render_reason = "runtime_health_too_low"

        entries.append(
            FeatureGateEntry(
                node_id=node.node_id,
                feature_id="media_render",
                availability=media_render_availability,
                reason=media_render_reason,
            )
        )

        simulation_availability = "supported"
        simulation_reason = "cpu_memory_requirements_met"

        if node.cpu_cores < 8:
            simulation_availability = "degraded"
            simulation_reason = "limited_cpu_capacity"

        if memory_profile.ram_total_gb < 32:
            simulation_availability = "degraded"
            simulation_reason = "limited_memory_capacity"

        if node.queue_depth > 8 or node.health_score < 35:
            simulation_availability = "unsupported"
            simulation_reason = "runtime_pressure_too_high"

        entries.append(
            FeatureGateEntry(
                node_id=node.node_id,
                feature_id="simulation_task",
                availability=simulation_availability,
                reason=simulation_reason,
            )
        )

    return FeatureGatingContract(
        total_entries=len(entries),
        entries=tuple(entries),
    )
