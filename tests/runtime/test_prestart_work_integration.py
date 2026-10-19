"""WORK -> actual prepared preflight with real inherited reservation FD, fake tools."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]


def work_world(tmp_path):
    root=tmp_path/"MAKSIMAR_PLATFORM";state=root/"RUNTIME/state";state.mkdir(parents=True);tools=root/"tools";tools.mkdir()
    shutil.copyfile(ROOT/"tools/work",tools/"work")
    for name in ("CORE_ROOT","SUPERVISOR"):(root/name).symlink_to(ROOT/name,target_is_directory=True)
    roles=[("runtime","process_supervisor","heartbeat_state"),("guard","stop_gate_watcher","guard_heartbeat_state"),("core_guard","core_guard","core_guard_heartbeat_state"),("kernel_guard","kernel_watchdog","kernel_heartbeat_state")]
    originals={}
    for i,(hint,source,receipt) in enumerate(roles):
        pid=910001+i;p=root/"RUNTIME"/(hint+".pid");p.write_text(str(pid)+"\n");originals[p]=p.read_bytes()
        p=state/(receipt+".json");p.write_text(json.dumps({"schema_version":1,"source":source,"pid":pid,"process_start_ticks":str(100+i),"status":"alive","ts":time.time()-100,"monotonic_ts":0.0}));originals[p]=p.read_bytes()
    marker=state/"degraded_mode.flag";marker.write_bytes(b"retained")
    python=root/".venv/bin/python";python.parent.mkdir(parents=True)
    python.write_text("#!"+sys.executable+"\n"+r'''import copy,json,os,sys,time
from pathlib import Path
sys.path.insert(0,str(Path.home()/"MAKSIMAR_PLATFORM"))
from SUPERVISOR import runtime_preflight as pf
from CORE_ROOT import run_context as rc
pf._tmux_snapshot=lambda:{"available":True,"sessions":[],"error":""}
pf._port_snapshot=lambda:{"listening":False,"owned_by_project":False,"owner_pids":[],"owner_identities":[],"error":""}
pf._health_snapshot=lambda:{"ok":False,"status":None}
pf._process_identity=lambda pid,**kwargs:{"pid":pid,"alive":False,"matches":False}
pf.heartbeat_process_alive=lambda *a,**k:False
pf._prestart_owned_processes=lambda:{"canonical":()}
if sys.argv[1].endswith("runtime_preflight.py"):
    with open(os.environ["TEST_CALLS"],"a") as f:f.write("ACTUAL_PREFLIGHT\n")
    if os.environ.get("PAUSE_PREFLIGHT")=="1":
        Path(os.environ["WAIT_MARKER"]).touch()
        limit=time.monotonic()+5
        while not Path(os.environ["RELEASE_MARKER"]).exists():
            if time.monotonic()>limit:raise SystemExit("fixture release timed out")
            time.sleep(0.01)
    def report():
        result=pf.inspect_runtime_state();d=result["decision"]
        return pf.PreflightReport(preflight_id="fixture",checked_at="fixture",ok=d["clean"],stale_tmux_found=False,stale_pid_found=False,stale_heartbeat_found=False,port_conflict_found=False,previous_crash_found=False,already_running_healthy=False,details={"runtime_state":d})
    pf.run_preflight=report
    pf.log=lambda _:None
    sys.argv=sys.argv[1:]
    pf.main()
elif sys.argv[1]=="-":
    exec(compile(sys.stdin.read(),"fixture-stdin","exec"),{"__name__":"__main__"})
else:raise SystemExit("unexpected model/provider/python call")
''')
    python.chmod(0o755)
    for name in ("ctl","rest","guard_ctl","core_guard_ctl","kernel_guard_ctl","oob_dashboard_ctl","ui_open","dashboards_open","dashboard"):
        p=tools/name;p.write_text('#!/bin/bash\necho "${0##*/}:$*" >> "$TEST_CALLS"\nif [[ "${0##*/}" == ctl && "$1" == start ]]; then exit 7; fi\nexit 0\n');p.chmod(0o755)
    binaries=tmp_path/"bin";binaries.mkdir()
    p=binaries/"tmux";p.write_text('#!/bin/bash\nif [[ "$1" == has-session ]]; then exit 1; fi\necho %1\n');p.chmod(0o755)
    env={**os.environ,"HOME":str(tmp_path),"PATH":str(binaries)+":"+os.environ["PATH"],"PYTHONPATH":str(root),"TEST_CALLS":str(tmp_path/"calls"),"WAIT_MARKER":str(tmp_path/"waiting"),"RELEASE_MARKER":str(tmp_path/"release"),"PYTHONDONTWRITEBYTECODE":"1"}
    env.pop("MAKSIMAR_STARTUP_FD",None)
    return root,state,originals,marker,env


def check_prepared_then_aborted(state,originals,marker):
    result=json.loads((state/"preflight_result.json").read_text())
    prep=result["details"]["prestart_reconciliation"]
    assert prep["status"]=="RECONCILED" and result["ok"] is True
    assert result["details"]["runtime_state"]["healthy"] is False
    manifest=json.loads((Path(prep["archive_path"])/"manifest.json").read_text());entries={x["origin"]:x for x in manifest["originals"]}
    assert all((Path(prep["archive_path"])/entries[str(p)]["archive_file"]).read_bytes()==data for p,data in originals.items())
    assert marker.read_bytes()==b"retained" and not (state/"run_metadata.json").exists()


def test_actual_work_preflight_preparation_and_existing_abort_integration(tmp_path):
    root,state,originals,marker,env=work_world(tmp_path)
    result=subprocess.run(["bash",str(root/"tools/work"),"--model-free"],env=env,capture_output=True,text=True,timeout=8)
    assert result.returncode==1,result.stdout+result.stderr
    assert Path(env["TEST_CALLS"]).read_text().splitlines().count("ACTUAL_PREFLIGHT")==1
    assert "rest:" in Path(env["TEST_CALLS"]).read_text()
    check_prepared_then_aborted(state,originals,marker)


def test_second_work_start_refused_before_preflight_or_state_effect(tmp_path):
    root,state,originals,marker,env=work_world(tmp_path);env["PAUSE_PREFLIGHT"]="1"
    first=subprocess.Popen(["bash",str(root/"tools/work"),"--model-free"],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        deadline=time.monotonic()+4
        while not Path(env["WAIT_MARKER"]).exists():
            assert first.poll() is None and time.monotonic()<deadline
            time.sleep(0.01)
        second=subprocess.run(["bash",str(root/"tools/work"),"--model-free"],env=env,capture_output=True,text=True,timeout=2)
        assert second.returncode==1 and "another canonical startup" in second.stdout
        assert all(p.read_bytes()==data for p,data in originals.items())
        assert not (state/"incident_evidence").exists()
    finally:
        Path(env["RELEASE_MARKER"]).touch()
        output,error=first.communicate(timeout=8)
    assert first.returncode==1,output+error
    assert Path(env["TEST_CALLS"]).read_text().splitlines().count("ACTUAL_PREFLIGHT")==1
    check_prepared_then_aborted(state,originals,marker)


def test_service_tmux_creation_does_not_inherit_startup_reservation(tmp_path):
    # Execute the exact inline blocks; fake tmux inspects env and inherited FD.
    import re
    bin_dir=tmp_path/"bin";bin_dir.mkdir();fake=bin_dir/"tmux"
    fake.write_text("#!"+sys.executable+"\nimport os\nassert 'MAKSIMAR_STARTUP_FD' not in os.environ\ntry:os.fstat(int(os.environ['TEST_LOCK_FD']))\nexcept OSError:pass\nelse:raise SystemExit('startup FD leaked')\n")
    fake.chmod(0o755)
    for name in ("ctl","guard_ctl","core_guard_ctl","kernel_guard_ctl"):
        text=(ROOT/"tools"/name).read_text()
        block=next(b for b in re.findall(r"<<'PY'\n(.*?)\nPY",text,re.S) if "tmux" in b and "subprocess.run" in b)
        with (tmp_path/(name+".lock")).open("w") as lock:
            os.set_inheritable(lock.fileno(),True)
            env={**os.environ,"HOME":str(tmp_path),"PATH":str(bin_dir)+":"+os.environ["PATH"],"PYTHONPATH":str(ROOT),"MAKSIMAR_STARTUP_FD":str(lock.fileno()),"TEST_LOCK_FD":str(lock.fileno())}
            result=subprocess.run(["bash","-c",'exec "$TEST_PYTHON" - session "$HOME" command',],input=block,env={**env,"TEST_PYTHON":sys.executable},pass_fds=(lock.fileno(),),capture_output=True,text=True,timeout=5)
            assert result.returncode==0,result.stdout+result.stderr


def test_work_observers_do_not_inherit_startup_descriptor(tmp_path):
    # Source actual observer functions only; no runtime entrypoint is executed.
    import re
    text=(ROOT/"tools/work").read_text()
    functions=[]
    for name in ("start_oob_dashboard","open_dashboard_windows","register_dashboard_ownership","create_runtime_dashboard_session"):
        functions.append(re.search(r"^"+name+r"\(\) \{.*?^\}",text,re.M|re.S).group())
    bin_dir=tmp_path/"bin";bin_dir.mkdir();fake=bin_dir/"tmux"
    fake.write_text('#!'+sys.executable+'\nimport os,sys\nassert "MAKSIMAR_STARTUP_FD" not in os.environ\ntry:os.fstat(8)\nexcept OSError:pass\nelse:raise SystemExit("observer inherited fd8")\nif len(sys.argv)>1 and sys.argv[1]=="has-session":raise SystemExit(1)\nprint("%1")\n');fake.chmod(0o755)
    for name in ("oob_dashboard_ctl","dashboards_open","dashboard"):(bin_dir/name).symlink_to(fake)
    script='\n'.join(functions)+"\nlog(){ :; };session_exists(){ return 1; };ROOT=$HOME;TOOLS_DIR=$TEST_BIN;DASHBOARD_SESSION=synthetic;DASHBOARD_OWNERSHIP_FILE=$HOME/owner;GUARD_LOG_FILE=x;CORE_GUARD_LOG_FILE=y;KERNEL_GUARD_LOG_FILE=z;exec 8>$HOME/reservation;export MAKSIMAR_STARTUP_FD=8;start_oob_dashboard;open_dashboard_windows;create_runtime_dashboard_session"
    env={**os.environ,"HOME":str(tmp_path),"PATH":str(bin_dir)+":"+os.environ["PATH"],"TEST_BIN":str(bin_dir)}
    result=subprocess.run(["bash","-c",script],env=env,capture_output=True,text=True,timeout=5)
    assert result.returncode==0,result.stdout+result.stderr
