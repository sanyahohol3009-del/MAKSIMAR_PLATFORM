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


# R4-C: real host parser/constraint composition with fixed external observations.
import json
_R4C_REAL_RUN_COMMAND = adapter._run_command


def _r4c_host_payload(**changes):
    values = {'schema_version': 1, 'source': 'windows_parent_cim_v1', 'platform': 'Win32NT',
              'total_physical_bytes': 32 * 1024**3, 'available_physical_bytes': 12 * 1024**3,
              'commit_limit_bytes': 64 * 1024**3, 'committed_bytes': 24 * 1024**3}
    values.update(changes)
    return json.dumps(values)


def test_r4c_local_host_snapshot_keeps_separate_constraints_and_provenance(monkeypatch, controlled_hardware_effects):
    controlled_hardware_effects['/proc/sys/kernel/osrelease'] = 'fixture-microsoft-WSL2'
    calls = []
    def command(argv):
        calls.append(argv)
        return _r4c_host_payload()
    monkeypatch.setattr(adapter, '_run_command', command)
    # Keep GPU probe doubles from generating unrelated command entries.
    monkeypatch.setattr(adapter, '_detect_nvidia_gpus', lambda: ((), ()))
    monkeypatch.setattr(adapter, '_detect_generic_gpus', lambda: ((), ()))
    result = adapter.detect_model_resource_observation()
    assert result['scope_complete'] is True
    assert dict(result['memory_available_bytes']) == {'execution_environment': 16*1024**3,
        'windows_parent_physical': 12*1024**3, 'windows_parent_commit': 40*1024**3}
    assert len(calls) == 1 and calls[0][:4] == ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command']
    assert calls[0][4] == adapter._WINDOWS_PARENT_MEMORY_COMMAND
    assert result['host_memory_observation']['association'] == 'local_windows_interop'
    assert result['host_memory_observation']['observed_monotonic'] <= result['host_memory_observation']['completed_monotonic']
    assert 'windows_parent_cim_v1' in result['source']


@pytest.mark.parametrize('changes', [
    {'schema_version': True}, {'schema_version': 2}, {'source': 'foreign'}, {'platform': 'Unix'},
    {'available_physical_bytes': True}, {'available_physical_bytes': 2.5},
    {'available_physical_bytes': -1}, {'total_physical_bytes': 0},
    {'available_physical_bytes': 33*1024**3}, {'commit_limit_bytes': 0},
    {'committed_bytes': 65*1024**3}, {'committed_bytes': None},
])
def test_r4c_invalid_host_fields_never_become_capacity(changes):
    assert adapter._parse_windows_parent_memory(_r4c_host_payload(**changes), started=10., finished=11.) is None


@pytest.mark.parametrize('raw', ['', 'not-json', '[]', 'null', '{}'])
def test_r4c_missing_or_partial_host_snapshot_unknown(raw):
    assert adapter._parse_windows_parent_memory(raw, started=10., finished=11.) is None


@pytest.mark.parametrize('started,finished', [(10.,9.), (10.,16.), (float('nan'),11.), (10.,float('inf')), (True,2.)])
def test_r4c_bad_acquisition_timing_is_unknown(started, finished):
    assert adapter._parse_windows_parent_memory(_r4c_host_payload(), started=started, finished=finished) is None


def test_r4c_known_zero_capacity_not_invented_unknown_or_positive():
    host = adapter._parse_windows_parent_memory(_r4c_host_payload(available_physical_bytes=0,
        committed_bytes=64*1024**3), started=10., finished=11.)
    assert host is not None and host['constraint_domains'] == (('windows_parent_physical',0),('windows_parent_commit',0))


def test_r4c_missing_host_preserves_guest_and_parent_constraints(monkeypatch, controlled_hardware_effects):
    f=controlled_hardware_effects; f['/proc/sys/kernel/osrelease']='fixture-microsoft-WSL2'
    f['/sys/fs/cgroup/memory.max']=str(10*1024**3); f['/sys/fs/cgroup/memory.current']=str(9*1024**3)
    monkeypatch.setattr(adapter, '_run_command', lambda argv: '')
    result=adapter.detect_model_resource_observation()
    assert result['scope_complete'] is False and result['host_memory_observation'] is None
    assert min(v for _,v in result['memory_available_bytes']) == 1024**3


def test_r4c_host_success_cannot_hide_missing_ancestor(monkeypatch, controlled_hardware_effects):
    f=controlled_hardware_effects; f['/proc/sys/kernel/osrelease']='fixture-microsoft-WSL2'
    f.pop('/sys/fs/cgroup/memory.max')
    monkeypatch.setattr(adapter, '_run_command', lambda argv: _r4c_host_payload())
    result=adapter.detect_model_resource_observation()
    assert result['host_memory_observation'] is not None and result['scope_complete'] is False


def test_r4c_native_linux_never_queries_windows(monkeypatch):
    calls=[]
    monkeypatch.setattr(adapter, '_run_command', lambda argv: calls.append(argv) or '')
    assert adapter._detect_windows_parent_memory() is None and not calls


def test_r4c_existing_command_timeout_remains_five_seconds(monkeypatch):
    import subprocess
    monkeypatch.setattr(adapter.shutil,'which',lambda name:'/fixture/'+name)
    calls=[]
    def timeout(argv,**kwargs):
        calls.append(kwargs['timeout'])
        raise subprocess.TimeoutExpired(argv,kwargs['timeout'])
    monkeypatch.setattr(adapter.subprocess,'run',timeout)
    assert _R4C_REAL_RUN_COMMAND(['powershell.exe','-NoProfile']) == ''
    assert calls == [5]
