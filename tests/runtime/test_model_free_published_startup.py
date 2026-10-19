"""Published launcher contract, exercised only in isolated fake toolchains."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def launcher(tmp_path):
    root = tmp_path / "MAKSIMAR_PLATFORM"
    state = root / "RUNTIME/state"
    state.mkdir(parents=True)
    tools = root / "tools"
    tools.mkdir()
    for name in ("tools/work", "start_maksimar.sh"):
        target = root / name
        shutil.copyfile(ROOT / name, target)
        target.chmod(0o755)
    markers = {name: ("retained:" + name).encode() for name in
               ("degraded_mode.flag", "stop_gate_trigger.txt", "last_degraded_reason.txt", "incident_history.jsonl")}
    for name, payload in markers.items():
        (state / name).write_bytes(payload)
    calls = tmp_path / "calls"
    fake_python = root / ".venv/bin/python"
    fake_python.parent.mkdir(parents=True)
    fake_python.write_text(r'''#!/bin/bash
case "$1" in
 *system_bootstrap.py) echo BOOT >> "$TEST_CALLS"; exit "${BOOT_STATUS:-0}";;
 *runtime_preflight.py)
   echo PREFLIGHT >> "$TEST_CALLS"
   printf '{"ok":%s,"already_running_healthy":false}\n' "${PREFLIGHT_OK:-true}" > "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/preflight_result.json"
   exit "${PREFLIGHT_STATUS:-0}";;
 -c)
   case "$2" in
    *recover_previous_run_degradation*) echo STOPGATE >> "$TEST_CALLS"; exit 0;;
    *inspect_runtime_state*) echo CHAIN >> "$TEST_CALLS"; exit 0;;
   esac;;
 -) exec "$TEST_PYTHON" -B "$@";;
esac
echo FORBIDDEN_MODEL_OR_PROVIDER_PROBE >> "$TEST_CALLS"
exit 95
''')
    fake_python.chmod(0o755)
    for tool in ("ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl", "rest", "oob_dashboard_ctl", "ui_open", "dashboards_open", "dashboard"):
        target = tools / tool
        target.write_text(r'''#!/bin/bash
name="${0##*/}"
echo "$name:$*" >> "$TEST_CALLS"
if [[ "$name" == ctl && "$1" == start ]]; then echo "STARTUP_CONTEXT:${MAKSIMAR_MODEL_FREE_STARTUP:-unset}" >> "$TEST_CALLS"; fi
if [[ "$1" == start && "$name" == "${FAIL_START:-none}" ]]; then exit 7; fi
if [[ "$1" == start ]]; then
 for name in heartbeat_state guard_heartbeat_state core_guard_heartbeat_state kernel_heartbeat_state; do
  touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/$name.json"
 done
fi
exit 0
''')
        target.chmod(0o755)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "python3").symlink_to(fake_python)
    for name, body in (("tmux", 'if [[ "$1" == has-session ]]; then exit 1; fi\necho %1\n'), ("curl", 'exit 0\n')):
        target = bin_dir / name
        target.write_text('#!/bin/bash\n' + body)
        target.chmod(0o755)
    env = {**os.environ, "HOME": str(tmp_path), "PATH": str(bin_dir) + ":" + os.environ["PATH"],
           "TEST_CALLS": str(calls), "TEST_PYTHON": sys.executable, "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("PYTHONPATH", None)
    def run(args=(), *, root_entry=False, **extra):
        result = subprocess.run(["bash", str(root / ("start_maksimar.sh" if root_entry else "tools/work")), *args],
                                env={**env, **extra}, capture_output=True, text=True, timeout=8)
        observed = calls.read_text().splitlines() if calls.exists() else []
        assert "FORBIDDEN_MODEL_OR_PROVIDER_PROBE" not in observed
        assert all((state / name).read_bytes() == data for name, data in markers.items())
        assert not (state / "run_metadata.json").exists()
        return result, observed
    return run


@pytest.mark.parametrize("args", [(), ("--model-free",)])
@pytest.mark.parametrize("model_flags", [{}, {"JARVIS_LIVE_WARMUP_INCLUDE_HEAVY": "1", "JARVIS_LIVE_WARMUP_INCLUDE_DAILY": "1", "JARVIS_LIVE_WARMUP_ENABLED": "1"}])
def test_published_default_and_model_free_keep_canonical_startup_without_probes(launcher, args, model_flags):
    result, calls = launcher(args, **model_flags)
    assert result.returncode == 0, result.stdout + result.stderr
    assert calls.count("PREFLIGHT") == 1 and calls.count("ctl:start") == 2
    assert calls.index("PREFLIGHT") < calls.index("ctl:start") < calls.index("guard_ctl:start")
    assert calls.index("guard_ctl:start") < calls.index("core_guard_ctl:start") < calls.index("kernel_guard_ctl:start")
    assert calls.index("kernel_guard_ctl:start") < calls.index("CHAIN") < calls.index("STOPGATE")
    assert not any(c.startswith("rest:") for c in calls)
    assert ("launcher warmup disabled" in result.stdout) is bool(args)


@pytest.mark.parametrize("bootstrap_status", ["0", "2"])
def test_root_passes_option_only_after_secure_bootstrap(launcher, bootstrap_status):
    result, calls = launcher(("--model-free",), root_entry=True, BOOT_STATUS=bootstrap_status)
    assert result.returncode == int(bootstrap_status)
    assert calls[0] == "BOOT"
    if bootstrap_status == "0":
        assert "launcher warmup disabled" in result.stdout and "STOPGATE" in calls
    else:
        assert calls == ["BOOT"]


@pytest.mark.parametrize("args", [(), ("--model-free",)])
def test_preflight_failure_has_no_start_cleanup_or_rest(launcher, args):
    result, calls = launcher(args, PREFLIGHT_OK="false", PREFLIGHT_STATUS="1")
    assert result.returncode == 1 and calls == ["PREFLIGHT"]


@pytest.mark.parametrize("owner", ["ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl"])
def test_published_start_error_reaches_existing_abort(launcher, owner):
    result, calls = launcher(("--model-free",), FAIL_START=owner)
    assert result.returncode == 1
    assert "rest:" in calls and "CHAIN" not in calls and "STOPGATE" not in calls


@pytest.mark.parametrize("args", [("--unknown",), ("--model-free", "--unknown")])
def test_unknown_or_extra_options_refused_before_effects(launcher, args):
    result, calls = launcher(args)
    assert result.returncode == 2 and calls == []


@pytest.mark.parametrize("args,expected", [((), "0"), (("--model-free",), "1")])
def test_work_pins_context_and_normal_launch_clears_inherited_suppression(launcher,args,expected):
    result,calls=launcher(args,MAKSIMAR_MODEL_FREE_STARTUP="1")
    assert result.returncode==0
    assert calls.count("STARTUP_CONTEXT:"+expected)==2
