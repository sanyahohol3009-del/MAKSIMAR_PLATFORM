from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    detect_node_hardware,
)


def test_hardware_detection_adapter_builds() -> None:
    """Hardware detection adapter should build successfully."""
    contract = detect_node_hardware(node_id="dev_001")

    assert contract.node_id == "dev_001"
    assert contract.cpu.cpu_arch != ""
    assert contract.cpu.cpu_cores >= 1
    assert contract.cpu.cpu_threads >= 1
    assert contract.memory.ram_total_gb >= 1
    assert contract.memory.ram_pressure_percent >= 0
    assert contract.gpu_count >= 0


def test_hardware_detection_adapter_returns_detection_sources() -> None:
    """Hardware detection adapter should expose at least one detection source."""
    contract = detect_node_hardware(node_id="dev_001")

    assert len(contract.detection_sources) >= 1


import pytest
from dataclasses import replace
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import hardware_detection_adapter as adapter
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter_models import DetectedGpuSnapshot

@pytest.fixture(autouse=True)
def controlled_hardware_effects(monkeypatch):
    files={"/proc/meminfo":"MemTotal: 33554432 kB\nMemAvailable: 16777216 kB\n",
        "/proc/cpuinfo":"vendor_id: Fixture\nmodel name: Fixture CPU\n",
        "/proc/self/cgroup":"0::/\n", "/sys/fs/cgroup/memory.max":"max",
        "/sys/fs/cgroup/memory.current":"0", "/proc/sys/kernel/osrelease":"fixture-native"}
    monkeypatch.setattr(adapter,"_run_command",lambda command:"")
    monkeypatch.setattr(adapter,"_read_text_file",lambda path:files.get(path,""))
    return files


def gpu(index,uuid,pci):
    return DetectedGpuSnapshot(index,"Fixture","same-model","discrete_gpu",80,70,False,("compute",),uuid,pci)


def test_distinct_identical_gpus_preserved_and_verified_alias_merged():
    first=gpu(0,"gpu-a","0000:01:00.0");second=gpu(1,"gpu-b","0000:02:00.0")
    alias=replace(first,gpu_uuid="",pci_bus_id="01:00.0",gpu_model="alternate description")
    result=adapter._merge_gpu_snapshots((first,second),(alias,))
    assert len(result)==2 and {g.gpu_uuid for g in result}=={"gpu-a","gpu-b"}


def test_conflicting_physical_identifiers_rejected():
    with pytest.raises(ValueError):
        adapter._merge_gpu_snapshots((gpu(0,"gpu-a","0000:01:00.0"),),(gpu(1,"gpu-b","0000:01:00.0"),))


def test_guest_memory_never_claimed_independent_host_budget(controlled_hardware_effects):
    files=controlled_hardware_effects;files["/proc/sys/kernel/osrelease"]="fixture-microsoft-WSL2"
    snapshot=adapter.detect_model_resource_observation()
    assert snapshot["scope_complete"] is False
    assert snapshot["memory_available_bytes"]==(("execution_environment",16*1024**3),)


def test_cgroup_available_budget_is_separate_constraint(controlled_hardware_effects):
    files=controlled_hardware_effects;files["/sys/fs/cgroup/memory.max"]=str(10*1024**3)
    files["/sys/fs/cgroup/memory.current"]=str(8*1024**3)
    snapshot=adapter.detect_model_resource_observation()
    assert snapshot["scope_complete"] is True
    assert min(v for _,v in snapshot["memory_available_bytes"])==2*1024**3


def test_missing_memory_observation_fail_closed(controlled_hardware_effects):
    controlled_hardware_effects["/proc/meminfo"]=""
    assert adapter.detect_model_resource_observation()["scope_complete"] is False


def test_parent_cgroup_limits_child_even_if_child_is_unlimited(controlled_hardware_effects):
    f=controlled_hardware_effects;f["/proc/self/cgroup"]="0::/child\n"
    f["/sys/fs/cgroup/child/memory.max"]="max";f["/sys/fs/cgroup/child/memory.current"]="0"
    f["/sys/fs/cgroup/memory.max"]=str(10*1024**3);f["/sys/fs/cgroup/memory.current"]=str(9*1024**3)
    snapshot=adapter.detect_model_resource_observation()
    assert snapshot["scope_complete"]
    assert min(v for _,v in snapshot["memory_available_bytes"])==1024**3


def test_real_nvidia_adapter_keeps_device_uuid_and_pci_aliases(monkeypatch):
    def command(args):
        if args[0]=="nvidia-smi":
            return "0, GPU-00000000-0000-0000-0000-000000000001, 00000000:01:00.0, identical, 81920, 71680\n1, GPU-00000000-0000-0000-0000-000000000002, 00000000:02:00.0, identical, 81920, 71680"
        if args[0]=="lspci":return "01:00.0 VGA compatible controller: NVIDIA identical"
        return ""
    monkeypatch.setattr(adapter,"_run_command",command)
    snapshot=adapter.detect_model_resource_observation()
    assert len(snapshot["accelerator_available_bytes"])==2 and snapshot["physical_identity_verified"]
    assert all(size==70*1024**3 for _,size in snapshot["accelerator_available_bytes"])
