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
        "/proc/self/cgroup":"0::/fixture\n", "/sys/fs/cgroup/fixture/memory.max":"max",
        "/sys/fs/cgroup/fixture/memory.current":"0", "/proc/sys/kernel/osrelease":"fixture-native"}
    # Finite budgets belong to /fixture, never to the true hierarchy root.
    files["/proc/self/mountinfo"] = "120 111 0:23 / /sys/fs/cgroup rw - cgroup2 cgroup2 rw\n"
    files["/sys/fs/cgroup/cgroup.controllers"] = "cpu memory pids"
    monkeypatch.setattr(adapter.os, "readlink", lambda path: {"/proc/self/ns/cgroup": "cgroup:[100]",
        "/proc/self/ns/mnt": "mnt:[200]"}[path])
    monkeypatch.setattr(adapter, "_cgroup_interface_state", lambda path: "PRESENT" if path in files else "ABSENT")
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
    files=controlled_hardware_effects;files["/sys/fs/cgroup/fixture/memory.max"]=str(10*1024**3)
    files["/sys/fs/cgroup/fixture/memory.current"]=str(8*1024**3)
    snapshot=adapter.detect_model_resource_observation()
    assert snapshot["scope_complete"] is True
    assert min(v for _,v in snapshot["memory_available_bytes"])==2*1024**3


def test_missing_memory_observation_fail_closed(controlled_hardware_effects):
    controlled_hardware_effects["/proc/meminfo"]=""
    assert adapter.detect_model_resource_observation()["scope_complete"] is False


def test_parent_cgroup_limits_child_even_if_child_is_unlimited(controlled_hardware_effects):
    f=controlled_hardware_effects;f["/proc/self/cgroup"]="0::/fixture/child\n"
    f["/sys/fs/cgroup/fixture/child/memory.max"]="max";f["/sys/fs/cgroup/fixture/child/memory.current"]="0"
    f["/sys/fs/cgroup/fixture/memory.max"]=str(10*1024**3);f["/sys/fs/cgroup/fixture/memory.current"]=str(9*1024**3)
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
    f['/sys/fs/cgroup/fixture/memory.max']=str(10*1024**3); f['/sys/fs/cgroup/fixture/memory.current']=str(9*1024**3)
    monkeypatch.setattr(adapter, '_run_command', lambda argv: '')
    result=adapter.detect_model_resource_observation()
    assert result['scope_complete'] is False and result['host_memory_observation'] is None
    assert min(v for _,v in result['memory_available_bytes']) == 1024**3


def test_r4c_host_success_cannot_hide_missing_ancestor(monkeypatch, controlled_hardware_effects):
    f=controlled_hardware_effects; f['/proc/sys/kernel/osrelease']='fixture-microsoft-WSL2'
    f.pop('/sys/fs/cgroup/fixture/memory.max')
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


# R4-C2: true hierarchy root vs namespace/bind root; no real cgroup mutation.
_R4C2_REAL_INTERFACE_STATE = adapter._cgroup_interface_state


def _r4c2_provenance(snapshot):
    return json.loads(snapshot['source'].split(';cgroup_v2=', 1)[1])


def test_r4c2_true_root_absent_controls_are_not_applicable(controlled_hardware_effects):
    files = controlled_hardware_effects
    files['/proc/self/cgroup'] = '0::/\n'
    result = adapter.detect_model_resource_observation()
    assert result['scope_complete'] is True
    assert result['memory_available_bytes'] == (('execution_environment', 16*1024**3),)
    proof = _r4c2_provenance(result)
    assert proof['status'] == 'TRUE_HIERARCHY_ROOT'
    assert proof['root_controls'] == 'NOT_APPLICABLE' and proof['stable'] is True
    assert proof['mount_root'] == '/' and proof['filesystem'] == 'cgroup2'
    assert proof['cgroup_namespace'] == 'cgroup:[100]' and proof['mount_namespace'] == 'mnt:[200]'
    assert len(proof['mountinfo_sha256']) == 64
    assert set(result) == {'observed_monotonic', 'memory_available_bytes', 'accelerator_available_bytes',
        'physical_identity_verified', 'cpu_threads', 'scope_complete', 'scope_id', 'source', 'host_memory_observation'}


@pytest.mark.parametrize('missing', ['memory.max', 'memory.current'])
def test_r4c2_missing_nonroot_interfaces_stay_unknown(controlled_hardware_effects, missing):
    controlled_hardware_effects.pop('/sys/fs/cgroup/fixture/' + missing)
    result = adapter.detect_model_resource_observation()
    assert result['scope_complete'] is False
    assert _r4c2_provenance(result)['root_controls'] == 'NOT_APPLICABLE'


@pytest.mark.parametrize('root_type', ['domain', 'domain threaded', 'threaded', ''])
def test_r4c2_namespace_slash_not_true_root_even_with_visible_budget(controlled_hardware_effects, root_type):
    f = controlled_hardware_effects
    f['/proc/self/cgroup'] = '0::/\n'
    f['/sys/fs/cgroup/cgroup.type'] = root_type
    f['/sys/fs/cgroup/memory.max'] = str(4*1024**3)
    f['/sys/fs/cgroup/memory.current'] = str(3*1024**3)
    x = adapter.detect_model_resource_observation()
    assert x['scope_complete'] is False
    assert ('cgroup:/sys/fs/cgroup', 1024**3) in x['memory_available_bytes']
    assert _r4c2_provenance(x)['root_controls'] == 'UNKNOWN'


@pytest.mark.parametrize('mountinfo', ['', 'broken',
    '120 111 0:23 /hidden /sys/fs/cgroup rw - cgroup2 cgroup2 rw\n',
    '120 111 0:23 / /sys/fs/cgroup rw - tmpfs tmpfs rw\n',
    '120 111 0:23 / /sys/fs/cgroup rw - cgroup2 cgroup2 rw\n'*2,
    '120 111 0:23 / /sys/fs/cgroup rw - cgroup2 cgroup2 rw\n121 120 0:1 / /sys/fs/cgroup/cgroup.type rw - tmpfs tmpfs rw\n',
    '120 111 0:23 / /sys/fs/cgroup rw cgroup2 cgroup2 rw\n',
    '120 111 0:23 / /sys/fs/cgroup rw - cgroup2\n'])
def test_r4c2_missing_ambiguous_hidden_mounts_fail_closed(controlled_hardware_effects, mountinfo):
    controlled_hardware_effects['/proc/self/mountinfo'] = mountinfo
    controlled_hardware_effects['/proc/self/cgroup'] = '0::/\n'
    x = adapter.detect_model_resource_observation()
    assert not x['scope_complete']
    assert x['memory_available_bytes'] == (('execution_environment', 16*1024**3),)


@pytest.mark.parametrize('membership', ['', '0::relative', '0::/../hidden', '0::/a/../../hidden',
    '0::/./fixture', '0:://fixture', '0::/fixture/', 'bad', 'bad::/fixture', '2::/fixture',
    '0::/fixture\n0::/fixture', '0::/fixture\nmalformed', '0::/null\x00name'])
def test_r4c2_malformed_membership_never_completes(controlled_hardware_effects, membership):
    controlled_hardware_effects['/proc/self/cgroup'] = membership
    assert adapter.detect_model_resource_observation()['scope_complete'] is False


@pytest.mark.parametrize('state', ['UNKNOWN', 'PRESENT'])
def test_r4c2_unreadable_root_discriminator_is_not_absence(monkeypatch, controlled_hardware_effects, state):
    monkeypatch.setattr(adapter, '_cgroup_interface_state', lambda path: state if path.endswith('cgroup.type') else 'ABSENT')
    assert not adapter.detect_model_resource_observation()['scope_complete']


@pytest.mark.parametrize('error, expected', [(FileNotFoundError(), 'ABSENT'),
    (PermissionError(), 'UNKNOWN'), (OSError(), 'UNKNOWN')])
def test_r4c2_real_metadata_reader_distinguishes_enoent(monkeypatch, error, expected):
    def fail(path):
        raise error
    monkeypatch.setattr(adapter.os, 'lstat', fail)
    assert _R4C2_REAL_INTERFACE_STATE('/fixture/cgroup.type') == expected


def test_r4c2_real_metadata_reader_rejects_symlink(tmp_path):
    target = tmp_path/'type'; target.write_text('domain')
    link = tmp_path/'link'; link.symlink_to(target)
    assert _R4C2_REAL_INTERFACE_STATE(str(target)) == 'PRESENT'
    assert _R4C2_REAL_INTERFACE_STATE(str(link)) == 'UNKNOWN'


@pytest.mark.parametrize('namespace', ['cgroup:[0]', 'missing', ''])
def test_r4c2_namespace_unavailable_or_changes_fail_closed(monkeypatch, controlled_hardware_effects, namespace):
    calls = []
    def readlink(path):
        if path.endswith('/mnt'): return 'mnt:[200]'
        calls.append(path)
        if namespace == 'missing': raise PermissionError()
        return 'cgroup:[100]' if len(calls) == 1 else namespace
    monkeypatch.setattr(adapter.os, 'readlink', readlink)
    assert adapter.detect_model_resource_observation()['scope_complete'] is False


def test_r4c2_mount_or_membership_race_is_unknown(monkeypatch, controlled_hardware_effects):
    original = adapter._read_text_file
    calls = []
    def read(path):
        if path == '/proc/self/mountinfo':
            calls.append(path)
            if len(calls) > 1: return ''
        return original(path)
    monkeypatch.setattr(adapter, '_read_text_file', read)
    assert not adapter.detect_model_resource_observation()['scope_complete']


def test_r4c2_v1_finite_ancestors_preserved(controlled_hardware_effects):
    f = controlled_hardware_effects; f['/proc/self/cgroup'] = '5:cpu:/unused\n7:memory:/parent/child\n'
    for path, limit, used in [('', 10, 9), ('/parent', 8, 6), ('/parent/child', 7, 4)]:
        f['/sys/fs/cgroup/memory'+path+'/memory.limit_in_bytes'] = str(limit*1024**3)
        f['/sys/fs/cgroup/memory'+path+'/memory.usage_in_bytes'] = str(used*1024**3)
    x = adapter.detect_model_resource_observation()
    assert x['scope_complete'] is True
    assert min(v for _,v in x['memory_available_bytes']) == 1024**3


def test_r4c2_true_root_does_not_hide_missing_wsl_host(controlled_hardware_effects):
    f = controlled_hardware_effects; f['/proc/self/cgroup'] = '0::/\n'
    f['/proc/sys/kernel/osrelease'] = 'microsoft-WSL2'
    x = adapter.detect_model_resource_observation()
    assert not x['scope_complete'] and _r4c2_provenance(x)['root_controls'] == 'NOT_APPLICABLE'
    assert x['host_memory_observation'] is None


def test_r4c2_missing_memory_controller_not_assumed_unlimited(controlled_hardware_effects):
    controlled_hardware_effects['/sys/fs/cgroup/cgroup.controllers'] = 'cpu pids'
    assert not adapter.detect_model_resource_observation()['scope_complete']


# R4-D provider resource view; client cgroup must not constrain the provider.
@pytest.fixture
def provider_scope_files(controlled_hardware_effects,monkeypatch):
    f=controlled_hardware_effects;pid=881;proc='/proc/881';root=proc+'/root/sys/fs/cgroup'
    f['/sys/fs/cgroup/fixture/memory.max']=str(1024**3)
    f['/sys/fs/cgroup/fixture/memory.current']='0'
    f[proc+'/cgroup']='0::/provider/worker\n'
    f[proc+'/mountinfo']=f['/proc/self/mountinfo']
    f[root+'/cgroup.controllers']='cpu memory pids'
    f[root+'/provider/memory.max']=str(10*1024**3)
    f[root+'/provider/memory.current']=str(6*1024**3)
    f[root+'/provider/worker/memory.max']='max'
    f[root+'/provider/worker/memory.current']='0'
    monkeypatch.setattr(adapter.os,'readlink',lambda path:{'/proc/self/ns/cgroup':'cgroup:[100]',
        '/proc/881/ns/cgroup':'cgroup:[100]','/proc/881/ns/mnt':'mnt:[201]'}[str(path)])
    seen=[]
    def affinity(target):seen.append(target);return {0,1,2}
    monkeypatch.setattr(adapter.os,'sched_getaffinity',affinity)
    return f,proc,root,seen


def test_r4d_provider_not_client_memory_and_affinity(provider_scope_files):
    f,proc,root,seen=provider_scope_files
    x=adapter.detect_model_resource_observation(provider_pid=881)
    assert x['scope_complete'] and x['scope_id']=='provider_process:881'
    assert x['cpu_threads']==3 and seen==[881]
    assert x['memory_available_bytes']==(('execution_environment',16*1024**3),('provider_cgroup:/sys/fs/cgroup/provider',4*1024**3))
    proof=_r4c2_provenance(x)
    assert proof['process_pid']==881 and proof['membership']=='0::/provider/worker'
    assert proof['inspection_root']==root and proof['mount_namespace']=='mnt:[201]'


@pytest.mark.parametrize('case',['namespace_root','missing_proc','missing_mount','missing_limit','missing_usage','malformed_mount','malformed_membership','hidden_mount'])
def test_r4d_inaccessible_or_ambiguous_provider_scope_unknown(provider_scope_files,case):
    f,proc,root,seen=provider_scope_files
    if case=='namespace_root':f[root+'/cgroup.type']='domain'
    elif case=='missing_proc':f.pop(proc+'/cgroup')
    elif case=='missing_mount':f.pop(proc+'/mountinfo')
    elif case=='missing_limit':f.pop(root+'/provider/memory.max')
    elif case=='missing_usage':f.pop(root+'/provider/worker/memory.current')
    elif case=='malformed_mount':f[proc+'/mountinfo']='invalid'
    elif case=='malformed_membership':f[proc+'/cgroup']='0::/../hidden'
    else:f[proc+'/mountinfo']=f[proc+'/mountinfo'].replace('0:23 / /sys','0:23 /hidden /sys')
    x=adapter.detect_model_resource_observation(provider_pid=881)
    assert not x['scope_complete']
    assert all('fixture' not in name for name,value in x['memory_available_bytes'])


def test_r4d_provider_affinity_failure_not_replaced_by_client_capacity(provider_scope_files,monkeypatch):
    def fail(pid):raise ProcessLookupError()
    monkeypatch.setattr(adapter.os,'sched_getaffinity',fail)
    x=adapter.detect_model_resource_observation(provider_pid=881)
    assert not x['scope_complete'] and x['cpu_threads']==0


def test_r4d_provider_namespace_coordinate_mismatch_unknown(provider_scope_files,monkeypatch):
    monkeypatch.setattr(adapter.os,'readlink',lambda path:{'/proc/self/ns/cgroup':'cgroup:[100]',
        '/proc/881/ns/cgroup':'cgroup:[999]','/proc/881/ns/mnt':'mnt:[201]'}[str(path)])
    assert not adapter.detect_model_resource_observation(provider_pid=881)['scope_complete']
