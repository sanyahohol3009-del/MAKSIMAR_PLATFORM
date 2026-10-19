"""Fail-closed results of the existing WORK start helpers; synthetic tools only."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("function,tool", [
    ("start_runtime", "ctl"),
    ("start_guard", "guard_ctl"),
    ("start_core_guard", "core_guard_ctl"),
    ("start_kernel_watchdog", "kernel_guard_ctl"),
])
@pytest.mark.parametrize("start_code", [0, 7])
def test_work_helper_does_not_replace_failed_start_with_successful_status(tmp_path, function, tool, start_code):
    source = (ROOT / "tools/work").read_text()
    # Extract the actual existing helper; no service, tmux or model is run.
    body = source.split(function + "() {\n", 1)[1].split("\n}", 1)[0]
    tools = tmp_path / "tools"
    tools.mkdir()
    calls = tmp_path / "calls"
    target = tools / tool
    target.write_text('#!/bin/bash\necho "$1" >> "$TEST_CALLS"\n'
                      'if [[ "$1" == start ]]; then exit "$TEST_START_CODE"; fi\nexit 0\n')
    target.chmod(0o755)
    script = tmp_path / "helper.sh"
    script.write_text('set -euo pipefail\nlog() { :; }\n' + function + '() {\n' + body + '\n}\n'
                      + function + ' || { result=$?; printf "ABORT:%s\\n" "$result"; exit "$result"; }\n'
                      + 'printf "CONTINUE\\n"\n')
    result = subprocess.run(["bash", str(script)], env={**os.environ, "HOME": str(tmp_path),
        "TOOLS_DIR": str(tools), "TEST_CALLS": str(calls), "TEST_START_CODE": str(start_code)},
        capture_output=True, text=True, timeout=5)
    assert result.returncode == start_code
    assert calls.read_text().splitlines() == (["start", "status"] if start_code == 0 else ["start"])
    assert ("CONTINUE" in result.stdout) is (start_code == 0)
    assert ("ABORT:7" in result.stdout) is (start_code == 7)
