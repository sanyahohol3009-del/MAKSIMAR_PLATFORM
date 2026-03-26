from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_multi_gpu_profile_contract,
    build_node_runtime_health_contract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.health_registry_models import (
    MultiNodeHealthEntry,
    MultiNodeHealthRegistryContract,
)
from MAKSIMAR_SERVER.RUNTIME.node_topology.topology_contract import (
    build_node_topology_runtime_contract,
)


def _resolve_health_state(
    *,
    connectivity_state: str,
    health_score: int,
    cpu_pressure_percent: int,
    ram_pressure_percent: int,
    vram_pressure_percent: int,
    queue_depth: int,
    degraded_active: bool,
) -> str:
    """Resolve normalized node health state."""
    if connectivity_state == "offline":
        return "critical"

    if (
        health_score < 40
        or cpu_pressure_percent >= 95
        or ram_pressure_percent >= 95
        or vram_pressure_percent >= 95
        or queue_depth >= 16
    ):
        return "critical"

    if (
        degraded_active
        or health_score < 85
        or cpu_pressure_percent >= 75
        or ram_pressure_percent >= 75
        or vram_pressure_percent >= 75
        or queue_depth >= 8
    ):
        return "warning"

    return "healthy"


def build_multi_node_health_registry_contract() -> MultiNodeHealthRegistryContract:
    """Build multi-node health registry from topology and runtime state."""
    topology = build_node_topology_runtime_contract()
    runtime = build_node_runtime_health_contract()
    gpu_profiles = build_multi_gpu_profile_contract()

    topology_by_node = {entry.node_id: entry for entry in topology.nodes}
    gpu_by_node = {entry.node_id: entry for entry in gpu_profiles.nodes}

    registry_entries: list[MultiNodeHealthEntry] = []

    for runtime_entry in runtime.nodes:
        topology_entry = topology_by_node[runtime_entry.node_id]
        gpu_entry = gpu_by_node[runtime_entry.node_id]

        vram_pressure_percent = 0
        if gpu_entry.accelerators:
            vram_pressure_percent = max(
                accelerator.vram_total_gb - accelerator.vram_free_gb
                for accelerator in gpu_entry.accelerators
            )
            # normalize from used-gb to percent only when VRAM total exists
            totals = [accelerator.vram_total_gb for accelerator in gpu_entry.accelerators]
            frees = [accelerator.vram_free_gb for accelerator in gpu_entry.accelerators]
            if totals and max(totals) > 0:
                total_vram = max(totals)
                free_vram = max(frees)
                used_vram = max(total_vram - free_vram, 0)
                vram_pressure_percent = int((used_vram / total_vram) * 100)

        health_state = _resolve_health_state(
            connectivity_state=topology_entry.connectivity_state,
            health_score=runtime_entry.health_score,
            cpu_pressure_percent=runtime_entry.cpu_pressure_percent,
            ram_pressure_percent=runtime_entry.ram_pressure_percent,
            vram_pressure_percent=vram_pressure_percent,
            queue_depth=runtime_entry.queue_depth,
            degraded_active=runtime_entry.degraded_active,
        )

        registry_entries.append(
            MultiNodeHealthEntry(
                node_id=runtime_entry.node_id,
                connectivity_state=topology_entry.connectivity_state,
                health_state=health_state,
                cpu_pressure_percent=runtime_entry.cpu_pressure_percent,
                ram_pressure_percent=runtime_entry.ram_pressure_percent,
                gpu_enabled=gpu_entry.gpu_count > 0,
                vram_pressure_percent=vram_pressure_percent,
                queue_depth=runtime_entry.queue_depth,
                health_score=runtime_entry.health_score,
                degraded_active=runtime_entry.degraded_active,
            )
        )

    healthy_nodes = sum(
        1 for entry in registry_entries if entry.health_state == "healthy"
    )
    warning_nodes = sum(
        1 for entry in registry_entries if entry.health_state == "warning"
    )
    critical_nodes = sum(
        1 for entry in registry_entries if entry.health_state == "critical"
    )

    return MultiNodeHealthRegistryContract(
        total_nodes=len(registry_entries),
        healthy_nodes=healthy_nodes,
        warning_nodes=warning_nodes,
        critical_nodes=critical_nodes,
        nodes=tuple(registry_entries),
    )
