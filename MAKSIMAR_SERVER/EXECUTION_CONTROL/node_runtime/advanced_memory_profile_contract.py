from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.advanced_memory_profile_models import (
    AdvancedMemoryProfile,
    AdvancedMemoryProfileContract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter import (
    detect_node_hardware,
)


def build_advanced_memory_profile_contract() -> AdvancedMemoryProfileContract:
    """Build advanced memory profile contract from detected hardware."""
    node_ids = ("mobile_001", "dev_001", "home_001")

    nodes = []
    for node_id in node_ids:
        detected = detect_node_hardware(node_id=node_id)
        memory = detected.memory

        nodes.append(
            AdvancedMemoryProfile(
                node_id=node_id,
                ram_total_gb=memory.ram_total_gb,
                ram_generation=memory.ram_generation,
                ram_frequency_mhz=memory.ram_frequency_mhz,
                ram_module_count=memory.ram_module_count,
                ram_channels=memory.ram_channels,
                ram_layout=memory.ram_layout,
                ecc_present=memory.ecc_present,
                registered_or_buffered=memory.registered_or_buffered,
                slot_population=memory.slot_population,
            )
        )

    return AdvancedMemoryProfileContract(
        total_nodes=len(nodes),
        nodes=tuple(nodes),
    )
