from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    NodeRuntimeHealthContract,
    NodeRuntimeHealthEntry,
)


def test_node_runtime_health_models_build() -> None:
    """Node runtime health models should build successfully."""
    contract = NodeRuntimeHealthContract(
        total_nodes=3,
        nodes=(
            NodeRuntimeHealthEntry(
                node_id="mobile_001",
                cpu_vendor="Qualcomm",
                cpu_model="Snapdragon 8 Gen 2",
                cpu_arch="arm64",
                cpu_cores=8,
                cpu_threads=8,
                cpu_pressure_percent=42,
                ram_total_gb=12,
                ram_free_gb=5,
                ram_pressure_percent=58,
                ram_generation="LPDDR5X",
                ram_frequency_mhz=4200,
                gpu_present=True,
                gpu_vendor="Qualcomm",
                gpu_model="Adreno",
                accelerator_class="mobile_integrated_gpu",
                vram_total_gb=0,
                vram_free_gb=0,
                vram_pressure_percent=0,
                thermal_state="normal",
                queue_depth=1,
                worker_capacity_available=0,
                health_score=88,
                degraded_active=False,
            ),
            NodeRuntimeHealthEntry(
                node_id="dev_001",
                cpu_vendor="Intel",
                cpu_model="Core i7",
                cpu_arch="x86_64",
                cpu_cores=8,
                cpu_threads=16,
                cpu_pressure_percent=37,
                ram_total_gb=32,
                ram_free_gb=18,
                ram_pressure_percent=44,
                ram_generation="DDR4",
                ram_frequency_mhz=3200,
                gpu_present=False,
                gpu_vendor="",
                gpu_model="",
                accelerator_class="cpu_only",
                vram_total_gb=0,
                vram_free_gb=0,
                vram_pressure_percent=0,
                thermal_state="normal",
                queue_depth=2,
                worker_capacity_available=2,
                health_score=91,
                degraded_active=False,
            ),
            NodeRuntimeHealthEntry(
                node_id="home_001",
                cpu_vendor="AMD",
                cpu_model="EPYC",
                cpu_arch="x86_64",
                cpu_cores=16,
                cpu_threads=32,
                cpu_pressure_percent=61,
                ram_total_gb=64,
                ram_free_gb=21,
                ram_pressure_percent=67,
                ram_generation="DDR5",
                ram_frequency_mhz=5600,
                gpu_present=True,
                gpu_vendor="NVIDIA",
                gpu_model="RTX 4070",
                accelerator_class="discrete_gpu",
                vram_total_gb=12,
                vram_free_gb=7,
                vram_pressure_percent=42,
                thermal_state="elevated",
                queue_depth=4,
                worker_capacity_available=3,
                health_score=84,
                degraded_active=False,
            ),
        ),
    )

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.nodes[0].cpu_vendor == "Qualcomm"
    assert contract.nodes[1].cpu_vendor == "Intel"
    assert contract.nodes[-1].cpu_vendor == "AMD"
    assert contract.nodes[-1].accelerator_class == "discrete_gpu"
    assert contract.nodes[-1].ram_generation == "DDR5"
    assert contract.nodes[-1].ram_frequency_mhz == 5600
