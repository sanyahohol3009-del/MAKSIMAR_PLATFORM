from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.multi_gpu_profile_models import (
    AcceleratorProfileEntry,
    MultiGpuProfile,
    MultiGpuProfileContract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter import (
    detect_node_hardware,
)


def build_multi_gpu_profile_contract() -> MultiGpuProfileContract:
    """Build unified multi-GPU / accelerator profile contract."""
    node_ids = ("mobile_001", "dev_001", "home_001")

    nodes = []
    for node_id in node_ids:
        detected = detect_node_hardware(node_id=node_id)

        accelerators = tuple(
            AcceleratorProfileEntry(
                gpu_index=gpu.gpu_index,
                gpu_vendor=gpu.gpu_vendor,
                gpu_model=gpu.gpu_model,
                accelerator_class=gpu.accelerator_class,
                vram_total_gb=gpu.vram_total_gb,
                vram_free_gb=gpu.vram_free_gb,
                shared_memory_mode=gpu.shared_memory_mode,
                gpu_capabilities=gpu.gpu_capabilities,
            )
            for gpu in detected.gpus
        )

        nodes.append(
            MultiGpuProfile(
                node_id=node_id,
                gpu_count=detected.gpu_count,
                accelerators=accelerators,
            )
        )

    return MultiGpuProfileContract(
        total_nodes=len(nodes),
        nodes=tuple(nodes),
    )
