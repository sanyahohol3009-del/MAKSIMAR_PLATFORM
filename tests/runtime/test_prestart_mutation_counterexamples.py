"""Historical counterexamples reconciled to current safety; original bytes remain in audit.

Existing replacements: test_prestart_mutation_coordination.py. These retain the
legacy shell environment/bridge boundaries and evidence retention checks.
"""
from pathlib import Path
import os
import ast
import json
import threading
import subprocess
import pytest
from CORE_ROOT import heartbeat_io as hb, stop_gate as gate, run_context as rc

ROOT = Path(__file__).resolve().parents[2]


def shell_function(name, path):
    source = path.read_text()
    return name + "() {\n" + source.split(name + "() {\n", 1)[1].split("\n}", 1)[0] + "\n}\n"


def invoke(tmp_path, function, variables):
    script = tmp_path / "fixture_mutator.sh"
    script.write_text('log() { :; }\n' + function)
    return subprocess.run(["bash", str(script)], env={**os.environ, "HOME": str(tmp_path), **variables},
                          capture_output=True, text=True, timeout=5, cwd=tmp_path)


def test_current_rest_cleanup_races_an_inflight_atomic_writer(tmp_path, monkeypatch):
    # Unique boundary: original legacy aliases, unrelated history/pending file,
    # and idempotent cleanup again AFTER the atomic publication.
    state = tmp_path / "state"; state.mkdir()
    receipt = state / "heartbeat.json"; receipt.write_bytes(b"old receipt")
    history = state / "historical_receipt.json"; history.write_bytes(b"historical evidence")
    pending = state / ".tmp_other_writer.json"; pending.write_bytes(b"other writer pending")
    monkeypatch.setattr(hb, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(rc, "RUNTIME_STATE_DIR", state)
    real_replace = hb.os.replace
    variables = {"RUNTIME_STATE_DIR": str(state)}
    for key in ("RUNTIME_HEARTBEAT_FILE", "GUARD_HEARTBEAT_FILE", "CORE_GUARD_HEARTBEAT_FILE", "KERNEL_HEARTBEAT_FILE", "PREFLIGHT_RESULT_FILE"):
        variables[key] = str(receipt)
    function = shell_function("remove_stale_state_files", ROOT / "tools/rest") + "remove_stale_state_files\n"
    protected = []
    payload = {"source": "synthetic atomic writer", "status": "alive"}
    def racing_replace(source, target):
        assert Path(source).exists() and Path(target) == receipt
        temporary_bytes = Path(source).read_bytes()
        assert json.loads(temporary_bytes) == payload
        result = invoke(tmp_path, function, variables)
        assert result.returncode == 0
        protected.append(Path(source).read_bytes() == temporary_bytes and receipt.read_bytes() == b"old receipt")
        assert history.read_bytes() == b"historical evidence"
        assert pending.read_bytes() == b"other writer pending"
        return real_replace(source, target)
    monkeypatch.setattr(hb.os, "replace", racing_replace)
    hb.atomic_write_json(receipt, payload)
    assert protected == [True] and hb.safe_read_json(receipt) == payload
    published = receipt.read_bytes(); inode = receipt.stat().st_ino
    result = invoke(tmp_path, function, variables)
    assert result.returncode == 0 and receipt.read_bytes() == published and receipt.stat().st_ino == inode
    assert history.read_bytes() == b"historical evidence" and pending.read_bytes() == b"other writer pending"


def test_current_work_cleanup_ignores_stopgate_transition_lock(tmp_path, monkeypatch):
    # Unique boundary: all legacy heartbeat variables alias one fresh receipt;
    # repeat cleanup and preserve the entire state evidence cohort under transition.
    state = tmp_path / "state"; state.mkdir()
    monkeypatch.setattr(gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(gate, "RUNTIME_STATE_DIR", state)
    monkeypatch.setattr(rc, "RUNTIME_STATE_DIR", state)
    receipt = state / "heartbeat.json"; receipt.write_bytes(b"new writer receipt")
    (state / "historical_receipt.json").write_bytes(b"historical evidence")
    (state / ".tmp_other_writer.json").write_bytes(b"pending evidence")
    variables = {"RUNTIME_STATE_DIR": str(state), "LOGS_DIR": str(tmp_path / "logs")}
    for key in ("RUNTIME_HEARTBEAT_FILE", "GUARD_HEARTBEAT_FILE", "CORE_GUARD_HEARTBEAT_FILE", "KERNEL_HEARTBEAT_FILE"):
        variables[key] = str(receipt)
    function = shell_function("remove_disposable_runtime_artifacts", ROOT / "tools/work") + "remove_disposable_runtime_artifacts\n"
    with gate._transition_lock():
        inode = (state / "stop_gate_transition.lock").stat().st_ino
        before = {p.name: (p.read_bytes(), p.stat().st_ino) for p in state.iterdir()}
        for _ in range(2):
            result = invoke(tmp_path, function, variables)
            assert result.returncode == 0
            assert {p.name: (p.read_bytes(), p.stat().st_ino) for p in state.iterdir()} == before
        assert receipt.read_bytes() == b"new writer receipt"
        assert (state / "stop_gate_transition.lock").stat().st_ino == inode


def test_current_guard_pid_write_ignores_stopgate_lock(tmp_path, monkeypatch):
    # Unique boundary: actual extracted shell forwards PID/module to the canonical
    # writer; ambiguous identity is not even queried until the transition releases.
    state = tmp_path / "state"; state.mkdir()
    monkeypatch.setattr(gate, "ensure_runtime_layout", lambda: None)
    monkeypatch.setattr(gate, "RUNTIME_STATE_DIR", state)
    monkeypatch.setattr(rc, "RUNTIME_STATE_DIR", state)
    hint = tmp_path / "guard.pid"; hint.write_text("1111\n")
    shell_bridge = ('find_guard_pid() { echo 4242; }\n'
        'python3() { printf "ARG:%s\\n" "$@"; printf "CODE:\\n"; cat; }\n')
    function = shell_bridge + shell_function("write_pid_file", ROOT / "tools/guard_ctl") + "write_pid_file\n"
    started = threading.Event(); looked_up = threading.Event(); done = threading.Event(); errors = []
    def identity(module):
        assert module == "CORE_ROOT.stop_gate_watcher"
        looked_up.set()
        return (101, 102)  # Explicit synthetic ambiguity; neither is claimed as a real owner.
    monkeypatch.setattr(hb, "find_owned_module_process_pids", identity)
    def writer(path, module):
        started.set()
        try:
            hb.write_owned_pid_hint(path, module)
        except RuntimeError as exc:
            errors.append(str(exc))
        finally:
            done.set()
    with gate._transition_lock():
        inode = (state / "stop_gate_transition.lock").stat().st_ino
        result = invoke(tmp_path, function, {"ROOT": str(tmp_path), "PID_FILE": str(hint), "RUNTIME_STATE_DIR": str(state)})
        assert result.returncode == 0 and hint.read_text() == "1111\n"
        arguments, program = result.stdout.split("CODE:\n", 1)
        assert arguments.splitlines() == ["ARG:-", "ARG:" + str(hint), "ARG:CORE_ROOT.stop_gate_watcher"]
        tree = ast.parse(program)
        call = tree.body[-1].value
        assert ast.dump(call) == ast.dump(ast.parse("write_owned_pid_hint(sys.argv[1], sys.argv[2])").body[0].value)
        assert any(isinstance(node, ast.ImportFrom) and node.module == "CORE_ROOT.heartbeat_io" for node in tree.body)
        thread = threading.Thread(target=writer, args=(hint, "CORE_ROOT.stop_gate_watcher"))
        thread.start(); assert started.wait(2)
        assert not looked_up.wait(0.1) and not done.is_set()
        assert hint.read_text() == "1111\n" and (state / "stop_gate_transition.lock").stat().st_ino == inode
    thread.join(3)
    assert done.is_set() and looked_up.is_set() and errors == ["PID hint identity unknown or ambiguous"]
    assert hint.read_text() == "1111\n"
