from __future__ import annotations

import importlib
import json
import subprocess
from types import SimpleNamespace

import pytest

from MAKSIMAR_CORE_LIB.action_library_adapters import agent_tooling_runtime_probe as probe
from MAKSIMAR_CORE_LIB.action_library_adapters import external_tool_library_adapter as consumer


def test_legacy_import_is_same_existing_owner():
    legacy = importlib.import_module("tools.jarvis_live_runtime.agent_tooling_runtime_probe")
    assert legacy is probe
    assert legacy.build_agent_tooling_runtime_probe_read_model is probe.build_agent_tooling_runtime_probe_read_model


@pytest.mark.parametrize("exists", [True, False])
def test_path_does_not_claim_import_or_runtime(tmp_path, exists):
    path = tmp_path if exists else tmp_path / "missing"
    result = probe._probe_path_only_manifest(str(path), "external_adapter:fixture")
    assert result.probe_kind == "PATH_EXISTS"
    assert result.path_exists is exists
    assert result.installed is exists
    assert result.import_probe_passed is False
    assert result.import_attempted is False
    assert result.package_metadata_exists is None
    assert result.runtime_capability_verified is False


def test_existing_consumer_cannot_select_path_as_import(tmp_path, monkeypatch):
    tool_id = "external_adapter:fixture"
    manifest = SimpleNamespace(tool_id=tool_id, package_name=tool_id, module_import_name=tool_id,
        source_library="fixture", capability_id=tool_id, adapter_mode="read_only", provider_kind="tool_provider",
        requires_verified_owner=True, safe_direct_allowed=False, risk_class="risk_gate", not_canonical_truth=True)
    monkeypatch.setattr(consumer, "load_external_tool_manifests", lambda: (manifest,))
    record = probe._probe_path_only_manifest(str(tmp_path), tool_id).to_read_model()
    status = consumer.probe_external_tool_adapters({"probe_results": (record,)})[0]
    assert status.installed is True
    assert status.import_probe_worked is False
    assert status.selection_enabled is False
    assert status.availability_status == "unavailable"


def fixture_runtime(tmp_path, monkeypatch):
    runtime = tmp_path / "python"
    runtime.write_text("synthetic fixture; never executed")
    monkeypatch.setattr(probe, "EXTERNAL_RUNTIME_PYTHON", runtime)
    return str(runtime)


@pytest.mark.parametrize("passed", [True, False, "false", "true", 1, None])
def test_import_status_is_typed_and_not_runtime_execution(tmp_path, monkeypatch, passed):
    runtime = fixture_runtime(tmp_path, monkeypatch)
    payload = {"installed": True, "import_probe_passed": passed, "import_attempted": True,
               "package_name": "package_a", "import_name": "module_a", "version_if_available": "1.2", "errors": []}
    calls = []
    def fake_run(*args, **kwargs):
        calls.append(args)
        return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr="")
    monkeypatch.setattr(probe.subprocess, "run", fake_run)
    result = probe._probe_import_in_external_runtime("package_a", "module_a")
    assert len(calls) == 1
    assert result.import_attempted is True
    assert result.import_probe_passed is (passed is True)
    assert result.runtime_capability_verified is False


@pytest.mark.parametrize("kind", ["malformed", "nonobject", "nonzero", "foreign_identity", "not_attempted", "timeout", "spawn_failure"])
def test_bad_wire_or_failed_process_never_proves_import(tmp_path, monkeypatch, kind):
    fixture_runtime(tmp_path, monkeypatch)
    payload = {"installed": True, "import_probe_passed": True, "import_attempted": True,
               "package_name": "package_a", "import_name": "module_a", "errors": []}
    if kind == "foreign_identity":
        payload["package_name"] = "other"
    if kind == "not_attempted":
        payload["import_attempted"] = False
    def fake_run(*args, **kwargs):
        if kind == "timeout":
            raise subprocess.TimeoutExpired("fixture", 60)
        if kind == "spawn_failure":
            raise OSError("synthetic spawn failure")
        text = "not-json" if kind == "malformed" else "[]" if kind == "nonobject" else json.dumps(payload)
        return SimpleNamespace(returncode=7 if kind == "nonzero" else 0, stdout=text, stderr="")
    monkeypatch.setattr(probe.subprocess, "run", fake_run)
    result = probe._probe_import_in_external_runtime("package_a", "module_a")
    assert result.import_probe_passed is False
    assert result.runtime_capability_verified is False
    if kind == "timeout":
        assert result.import_attempted is None
    elif kind in {"spawn_failure", "not_attempted"}:
        assert result.import_attempted is False


def test_missing_runtime_does_not_spawn(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, "EXTERNAL_RUNTIME_PYTHON", tmp_path / "missing")
    monkeypatch.setattr(probe.subprocess, "run", lambda *a, **k: pytest.fail("must not spawn"))
    result = probe._probe_import_in_external_runtime("package_a", "module_a")
    assert result.import_attempted is False
    assert result.import_probe_passed is False


@pytest.mark.parametrize("extra", [{"probe_kind": "PATH_EXISTS", "import_attempted": True},
    {"runtime_capability_verified": True}, {"import_attempted": "false"}])
def test_result_contract_rejects_unsupported_proof(extra):
    with pytest.raises(ValueError):
        probe.AgentToolingRuntimeProbeResult(False, False, "package_a", "module_a", "", "fixture", (), **extra)


def test_legacy_cli_forwards_to_same_owner_without_probe(monkeypatch):
    import runpy
    from pathlib import Path
    called = []
    monkeypatch.setattr(probe, "main", lambda: called.append("canonical") or 0)
    root = Path(probe.__file__).resolve().parents[2]
    with pytest.raises(SystemExit) as exc:
        runpy.run_path(str(root / "tools/jarvis_live_runtime/agent_tooling_runtime_probe.py"), run_name="__main__")
    assert exc.value.code == 0
    assert called == ["canonical"]


def test_empty_wire_preserves_unknown_import_attempt(tmp_path, monkeypatch):
    fixture_runtime(tmp_path, monkeypatch)
    monkeypatch.setattr(probe.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stdout="{}", stderr=""))
    result = probe._probe_import_in_external_runtime("package_a", "module_a")
    assert result.import_probe_passed is False
    assert result.import_attempted is None
    assert result.package_metadata_exists is None
