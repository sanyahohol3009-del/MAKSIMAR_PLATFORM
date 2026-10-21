from __future__ import annotations
import os
import pathlib
import subprocess
import pytest


@pytest.mark.parametrize("bootstrap_status", [0, 2])
def test_root_start_uses_existing_work_only_after_bootstrap_pass(tmp_path, bootstrap_status):
    root = tmp_path / "MAKSIMAR_PLATFORM"
    (root / "tools").mkdir(parents=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "calls"
    python = bin_dir / "python3"
    python.write_text(f'#!/bin/bash\necho BOOT >> "$TEST_CALLS"\nexit {bootstrap_status}\n')
    python.chmod(0o755)
    for name, marker in (("work", "WORK"), ("dashboard.sh", "OLD_DASHBOARD_ONLY")):
        p = root / "tools" / name
        p.write_text(f'#!/bin/bash\necho {marker} >> "$TEST_CALLS"\n')
        p.chmod(0o755)
    env = dict(os.environ, HOME=str(tmp_path), PATH=str(bin_dir) + ":" + os.environ["PATH"], TEST_CALLS=str(calls))
    result = subprocess.run(["bash", str(pathlib.Path("start_maksimar.sh").resolve())], env=env, text=True, capture_output=True)
    assert result.returncode == bootstrap_status
    assert calls.read_text().splitlines() == (["BOOT", "WORK"] if bootstrap_status == 0 else ["BOOT"])


def test_real_work_launcher_has_no_recursive_startup_in_isolated_toolchain(tmp_path):
    """Exercise actual root/work shell control flow; all process/device tools are fakes."""
    import sys
    import shutil
    root = tmp_path / "MAKSIMAR_PLATFORM"
    tools = root / "tools"
    tools.mkdir(parents=True)
    state = root / "RUNTIME" / "state"
    state.mkdir(parents=True)
    calls = tmp_path / "calls"
    for name in ("start_maksimar.sh", "tools/work"):
        target = root / name
        shutil.copyfile(pathlib.Path(name), target)
        target.chmod(0o755)
    # Disposable heartbeat existence is supplied by fake ctl start, never production.
    script = '#!/bin/bash\necho "${0##*/}:$*" >> "$TEST_CALLS"\n'
    script += 'mkdir -p "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state"\n'
    script += 'for n in heartbeat_state guard_heartbeat_state core_guard_heartbeat_state kernel_heartbeat_state; do touch "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/$n.json"; done\n'
    for name in ("rest", "ctl", "guard_ctl", "core_guard_ctl", "kernel_guard_ctl", "oob_dashboard_ctl", "ui_open", "dashboards_open", "dashboard"):
        target = tools / name
        target.write_text(script)
        target.chmod(0o755)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_python = root / ".venv/bin/python"
    fake_python.parent.mkdir(parents=True)
    fake_python.write_text(
        '#!/bin/bash\n'
        'case "$1" in\n'
        '*system_bootstrap.py) echo BOOT >> "$TEST_CALLS"; exit 0;;\n'
        '*runtime_preflight.py) echo PREFLIGHT >> "$TEST_CALLS"; '
        'echo \'{"ok":true,"already_running_healthy":false}\' > "$HOME/MAKSIMAR_PLATFORM/RUNTIME/state/preflight_result.json"; exit 0;;\n'
        '*model_warmup_probe.py) echo WARMUP >> "$TEST_CALLS"; echo \'{"ready":true}\'; exit 0;;\n'
        '-c) echo RECOVERY >> "$TEST_CALLS"; exit 0;;\n'
        'esac\n'
        'exec "$TEST_REAL_PYTHON" "$@"\n'
    )
    fake_python.chmod(0o755)
    (bin_dir / "python3").symlink_to(fake_python)
    for name in ("tmux", "curl"):
        target = bin_dir / name
        target.write_text('#!/bin/bash\n' + ('if [[ "$1" == has-session ]]; then exit 1; fi\necho %1\n' if name == "tmux" else 'exit 0\n'))
        target.chmod(0o755)
    env = dict(os.environ, HOME=str(tmp_path), PATH=str(bin_dir) + ":" + os.environ["PATH"], TEST_CALLS=str(calls), TEST_REAL_PYTHON=sys.executable)
    result = subprocess.run(["bash", str(root / "start_maksimar.sh")], env=env, text=True, capture_output=True, timeout=10)
    assert result.returncode == 0, result.stdout + result.stderr
    observed = calls.read_text().splitlines()
    assert observed.count("BOOT") == 1
    assert observed.count("PREFLIGHT") == 1
    assert observed.count("WARMUP") == 1
    assert observed.count("ctl:start") == 2  # existing readiness identity reconciliation
    assert observed.count("guard_ctl:start") == 1
    assert observed.count("core_guard_ctl:start") == 1
    assert observed.count("kernel_guard_ctl:start") == 1
    assert observed.index("guard_ctl:start") < observed.index("core_guard_ctl:start") < observed.index("kernel_guard_ctl:start") < observed.index("WARMUP")
    assert not any(x.startswith("rest:") for x in observed)
