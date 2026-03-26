from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    CpuHardwareProfile,
    GpuHardwareProfile,
    MemoryHardwareProfile,
    NodeHardwareProfile,
    NodeHardwareProfileContract,
)


def test_node_hardware_profile_models_build() -> None:
    """Node hardware profile models should build successfully."""
    contract = NodeHardwareProfileContract(
        total_nodes=3,
        nodes=(
            NodeHardwareProfile(
                node_id="mobile_001",
                cpu_profile=CpuHardwareProfile(
                    cpu_vendor="Qualcomm",
                    cpu_model="Snapdragon 8 Gen 2",
                    cpu_arch="arm64",
                    cpu_cores=8,
                    cpu_threads=8,
                    cpu_features=("neon", "fp16"),
                ),
                gpu_profile=GpuHardwareProfile(
                    gpu_present=True,
                    gpu_vendor="Qualcomm",
                    gpu_model="Adreno",
                    accelerator_class="mobile_integrated_gpu",
                    vram_total_gb=0,
                    gpu_capabilities=("mobile_graphics",),
                ),
                memory_profile=MemoryHardwareProfile(
                    ram_total_gb=12,
                    ram_generation="LPDDR5X",
                    ram_frequency_mhz=4200,
                ),
            ),
            NodeHardwareProfile(
                node_id="dev_001",
                cpu_profile=CpuHardwareProfile(
                    cpu_vendor="Intel",
                    cpu_model="Core i7",
                    cpu_arch="x86_64",
                    cpu_cores=8,
                    cpu_threads=16,
                    cpu_features=("avx2", "aes"),
                ),
                gpu_profile=GpuHardwareProfile(
                    gpu_present=False,
                    gpu_vendor="",
                    gpu_model="",
                    accelerator_class="cpu_only",
                    vram_total_gb=0,
                    gpu_capabilities=(),
                ),
                memory_profile=MemoryHardwareProfile(
                    ram_total_gb=32,
                    ram_generation="DDR4",
                    ram_frequency_mhz=3200,
                ),
            ),
            NodeHardwareProfile(
                node_id="home_001",
                cpu_profile=CpuHardwareProfile(
                    cpu_vendor="AMD",
                    cpu_model="EPYC",
                    cpu_arch="x86_64",
                    cpu_cores=16,
                    cpu_threads=32,
                    cpu_features=("avx2", "aes"),
                ),
                gpu_profile=GpuHardwareProfile(
                    gpu_present=True,
                    gpu_vendor="NVIDIA",
                    gpu_model="RTX 4070",
                    accelerator_class="discrete_gpu",
                    vram_total_gb=12,
                    gpu_capabilities=("cuda", "tensor"),
                ),
                memory_profile=MemoryHardwareProfile(
                    ram_total_gb=64,
                    ram_generation="DDR5",
                    ram_frequency_mhz=5600,
                ),
            ),
        ),
    )

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3
    assert contract.nodes[0].cpu_profile.cpu_vendor == "Qualcomm"
    assert contract.nodes[1].cpu_profile.cpu_vendor == "Intel"
    assert contract.nodes[-1].cpu_profile.cpu_vendor == "AMD"
    assert contract.nodes[-1].gpu_profile.accelerator_class == "discrete_gpu"
    assert contract.nodes[-1].memory_profile.ram_generation == "DDR5"
