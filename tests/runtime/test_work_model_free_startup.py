"""Existing WORK/root shell path with isolated synthetic toolchains only."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from SUPERVISOR.runtime_preflight import classify_runtime_observation

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def shell_world(tmp_path):
    root = tmp_path / "MAKSIMAR_PLATFORM"
    tools = root / "tools"
    tools.mkdir(parents=True)
    state = root / "RUNTIME/state"
    state.mkdir(parents=True)
    calls = tmp_path / "calls"
    for name in ("tools/work", "start_maksimar.sh"):
        target = root / name
        shutil.copyfile(ROOT / name, target)
        target.chmod(0o755)
    for name in ("degraded_mode.flag", "stop_gate_trigger.txt", "last_degraded_reason.txt", "incident_history.jsonl"):
        (state / name).write_text("preserve " + name)
    original_markers = {p.name: p.read_bytes() for p in state.iterdir()}
    fake_python = root / ".venv/bin/python"
    fake_python.parent.mkdir(parents=True)
    fake_python.write_text(r'''#!/bin/bash
case "$1" in
  *system_bootstrap.py) echo BOOT >> "$TEST_CALLS"; exit "${BOOT_STATUS:-0}";;
  *runtime_preflight.py)
    echo PREFLIGHT >> "$TEST_CALLS"
    printf '{"ok":%s,"already_running_healthy":%s}\n' "${PREFLIGHT_OK:-true}" "${ALREADY_HEALTHY:-false}" > "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/preflight_result.json"
    exit "${PREFLIGHT_STATUS:-0}";;
  *model_warmup_probe.py)
    echo "WARMUP:$*" >> "$TEST_CALLS"
    [[ "${FORBID_WARMUP:-0}" == 1 ]] && exit 99
    printf '{"model_ready":%s}\n' "${WARMUP_MODEL_READY:-true}"
    if [[ "${LOST_CHAIN_DURING_WARMUP:-0}" == 1 ]]; then
      touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/test_chain_failed"
    fi
    exit "${WARMUP_STATUS:-0}";;
  -c)
    case "$2" in
      *recover_previous_run_degradation*) echo RECOVERY >> "$TEST_CALLS"; exit 0;;
      *inspect_runtime_state*) echo CHAIN_PREFLIGHT >> "$TEST_CALLS"; [[ -f "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/test_chain_failed" ]] && exit 1; exit 0;;
      *) echo UNAPPROVED_PYTHON_CALL >> "$TEST_CALLS"; exit 97;;
    esac;;
esac
exec "$TEST_REAL_PYTHON" -B "$@"
''')
    fake_python.chmod(0o755)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "python3").symlink_to(fake_python)
    for name in ("ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl", "rest", "ui_open", "oob_dashboard_ctl", "dashboards_open", "dashboard"):
        target = tools / name
        target.write_text(r'''#!/bin/bash
name="${0##*/}"
echo "$name:$*" >> "$TEST_CALLS"
if [[ "$name" == ctl && "$1" == start ]]; then
  touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/heartbeat_state.json"
fi
if [[ "$1" == start && "$name" == "${FAIL_START:-none}" ]]; then exit 7; fi
if [[ "$1" == start ]]; then
  case "$name" in
    guard_ctl) touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/guard_heartbeat_state.json";;
    core_guard_ctl) touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/core_guard_heartbeat_state.json";;
    kernel_guard_ctl) touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/kernel_heartbeat_state.json";;
  esac
fi
exit 0
''')
        target.chmod(0o755)
    for name in ("tmux", "curl"):
        target = bin_dir / name
        target.write_text('#!/bin/bash\n' + ('if [[ "$1" == has-session ]]; then exit 1; fi\nprintf "%s\\n" %1\n' if name == "tmux" else 'exit 0\n'))
        target.chmod(0o755)
    date = bin_dir / "date"
    date.write_text(r'''#!/bin/bash
if [[ "${FAST_TIMEOUT:-0}" == 1 && "$1" == +%s ]]; then
  counter="$HOME/test_monotonic_clock"
  n=0; [[ -f "$counter" ]] && read -r n < "$counter"
  printf '%s\n' "$((n+30))" > "$counter"
  printf '%s\n' "$n"
else
  exec /bin/date "$@"
fi
''')
    date.chmod(0o755)
    env = dict(os.environ, HOME=str(tmp_path), PATH=str(bin_dir) + ":" + os.environ["PATH"],
               TEST_CALLS=str(calls), TEST_REAL_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE="1")
    # Shell JSON readers use stdlib only; they must not import the original tree.
    env.pop("PYTHONPATH", None)
    def run(*args, root_entry=False, clean_model_start=False, **changes):
        expected_markers = dict(original_markers)
        if clean_model_start:
            (state / "degraded_mode.flag").unlink()
            expected_markers.pop("degraded_mode.flag")
        if changes.get("ALREADY_HEALTHY") == "true":
            for name in ("heartbeat_state", "guard_heartbeat_state", "core_guard_heartbeat_state", "kernel_heartbeat_state"):
                (state / (name + ".json")).write_text("synthetic existing healthy receipt")
        result = subprocess.run(["bash", str(root / ("start_maksimar.sh" if root_entry else "tools/work")), *args],
                                env={**env, **changes}, text=True, capture_output=True, timeout=8)
        observed = calls.read_text().splitlines() if calls.exists() else []
        assert not any("UNAPPROVED" in item for item in observed)
        assert all((state / name).read_bytes() == value for name, value in expected_markers.items())
        assert not (state / "run_metadata.json").exists()
        return result, observed
    return run


def test_default_work_preserves_warmup_and_full_chain(shell_world):
    result, calls = shell_world(clean_model_start=True)
    assert result.returncode == 0, result.stdout + result.stderr
    warmups = [c for c in calls if c.startswith("WARMUP:")]
    assert len(warmups) == 1 and "--warm --primary-only" in warmups[0]
    assert calls.index("PREFLIGHT") < calls.index("ctl:start") < calls.index(warmups[0])
    assert calls.index("guard_ctl:start") < calls.index("core_guard_ctl:start") < calls.index("kernel_guard_ctl:start") < calls.index("CHAIN_PREFLIGHT") < calls.index("RECOVERY") < calls.index(warmups[0])
    assert calls.count("CHAIN_PREFLIGHT") == 2
    assert calls.index(warmups[0]) < max(i for i, call in enumerate(calls) if call == "CHAIN_PREFLIGHT")
    assert not any(c.startswith("rest:") for c in calls)


@pytest.mark.parametrize("flags", [{}, {"JARVIS_LIVE_WARMUP_INCLUDE_HEAVY": "1"}, {"JARVIS_LIVE_WARMUP_INCLUDE_DAILY": "1", "JARVIS_LIVE_WARMUP_ENABLED": "1"}])
def test_model_free_skips_entire_probe_even_when_environment_requests_models(shell_world, flags):
    result, calls = shell_world("--model-free", FORBID_WARMUP="1", **flags)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not any(c.startswith("WARMUP:") for c in calls)
    for required in ("PREFLIGHT", "ctl:start", "guard_ctl:start", "core_guard_ctl:start", "kernel_guard_ctl:start", "CHAIN_PREFLIGHT", "RECOVERY"):
        assert required in calls
    assert calls.index("PREFLIGHT") < calls.index("ctl:start") < calls.index("CHAIN_PREFLIGHT") < calls.index("RECOVERY")
    assert "skipping model warmup probe" in result.stdout


@pytest.mark.parametrize("args", [(), ("--model-free",)])
def test_preflight_rejection_preserves_evidence_without_start_or_rest(shell_world, args):
    result, calls = shell_world(*args, PREFLIGHT_OK="false", PREFLIGHT_STATUS="1")
    assert result.returncode == 1
    assert calls == ["PREFLIGHT"]


def test_healthy_model_free_repeat_still_delegates_recovery_without_duplicate_start(shell_world):
    result, calls = shell_world("--model-free", ALREADY_HEALTHY="true", FORBID_WARMUP="1")
    assert result.returncode == 0
    assert calls == ["PREFLIGHT", "RECOVERY"]


@pytest.mark.parametrize("failed_owner", ["ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl"])
def test_abort_keeps_existing_rest_delegation_and_markers(shell_world, failed_owner):
    result, calls = shell_world("--model-free", FAIL_START=failed_owner, FORBID_WARMUP="1")
    assert result.returncode == 1
    assert "rest:" in calls
    assert "CHAIN_PREFLIGHT" not in calls
    assert not any(c.startswith("WARMUP:") for c in calls)


@pytest.mark.parametrize("bootstrap_status", ["0", "2"])
def test_root_forwards_model_free_only_through_secure_bootstrap(shell_world, bootstrap_status):
    result, calls = shell_world("--model-free", root_entry=True, BOOT_STATUS=bootstrap_status, FORBID_WARMUP="1")
    assert result.returncode == int(bootstrap_status)
    assert calls[0] == "BOOT"
    if bootstrap_status == "0":
        assert "PREFLIGHT" in calls and "guard_ctl:start" in calls
        assert not any(c.startswith("WARMUP:") for c in calls)
    else:
        assert calls == ["BOOT"]


@pytest.mark.parametrize("args", [("--unknown",), ("--model-free", "--unknown")])
def test_invalid_arguments_fail_before_preflight_or_start(shell_world, args):
    result, calls = shell_world(*args)
    assert result.returncode == 2
    assert calls == []


def clean_observation():
    return {"tmux": {"available": True, "sessions": []}, "pid_file_exists": False,
            "runtime_pid": None, "runtime_pid_identity": {"alive": False, "matches": False},
            "heartbeats": {scope: {"exists": False, "fresh": False} for scope in ("runtime", "guard", "core_guard", "kernel_guard")},
            "port": {"listening": False, "owner_pids": [], "owned_by_project": False},
            "health": {"ok": False}, "run_metadata": None}


def test_actual_preflight_clean_start_needs_no_previous_metadata():
    observation = clean_observation()
    before = copy.deepcopy(observation)
    verdict = classify_runtime_observation(observation)
    assert verdict["clean"] is True and verdict["healthy"] is False
    assert observation == before


@pytest.mark.parametrize("state", ["stale_pid", "stale_alive", "foreign_port", "unknown_process"])
def test_actual_preflight_never_promotes_stale_or_unknown_state(state):
    observation = clean_observation()
    if state in {"stale_pid", "unknown_process"}:
        observation.update(pid_file_exists=True, runtime_pid=778899,
                           runtime_pid_identity={"alive": False if state == "stale_pid" else None, "matches": False})
    elif state == "stale_alive":
        observation["heartbeats"]["runtime"] = {"exists": True, "status": "alive", "fresh": False, "source": "process_supervisor"}
    else:
        observation["port"]["listening"] = True
    before = copy.deepcopy(observation)
    verdict = classify_runtime_observation(observation)
    assert verdict["clean"] is False and verdict["healthy"] is False
    assert observation == before


@pytest.mark.parametrize("failed_owner", ["ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl"])
def test_normal_work_never_loads_before_guard_start_success(shell_world, failed_owner):
    result, calls = shell_world(clean_model_start=True, FAIL_START=failed_owner)
    assert result.returncode == 1
    assert "rest:" in calls
    assert not any(c.startswith("WARMUP:") for c in calls)


def test_normal_work_withholds_warmup_while_stopgate_remains_active(shell_world):
    result, calls = shell_world(FORBID_WARMUP="1")
    assert result.returncode == 0
    assert "canonical StopGate degradation remains active" in result.stdout
    assert not any(c.startswith("WARMUP:") for c in calls)
    assert calls.count("CHAIN_PREFLIGHT") == 2
    assert "readiness=ready" not in result.stdout


@pytest.mark.parametrize("warmup_status", ["1", "7", "124"])
def test_recoverable_warmup_failure_preserves_guarded_runtime_and_truth(shell_world, warmup_status):
    result, calls = shell_world(clean_model_start=True, WARMUP_STATUS=warmup_status, WARMUP_MODEL_READY="false")
    assert result.returncode == 0
    assert "readiness=not_ready" in result.stdout and "readiness=ready" not in result.stdout
    assert calls.count("CHAIN_PREFLIGHT") == 2
    warmup = next(c for c in calls if c.startswith("WARMUP:"))
    assert calls.index("kernel_guard_ctl:start") < calls.index(warmup)
    assert not any(c.startswith("rest:") for c in calls)


def test_post_warmup_chain_loss_aborts_through_existing_rest(shell_world):
    result, calls = shell_world(clean_model_start=True, LOST_CHAIN_DURING_WARMUP="1", FAST_TIMEOUT="1")
    assert result.returncode == 1
    assert "guard chain lost during model warmup" in result.stdout
    assert "rest:" in calls
    assert not any(c.startswith("dashboards_open:") for c in calls)
