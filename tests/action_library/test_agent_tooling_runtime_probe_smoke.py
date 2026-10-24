from __future__ import annotations

import json
from pathlib import Path

from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models as probe_module


def test_agent_tooling_runtime_probe_smoke(monkeypatch) -> None:
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "0")
    fake_runtime_python = Path("/dev/shm/agent_tooling_runtime_python")
    monkeypatch.setattr(probe_module, "EXTERNAL_RUNTIME_PYTHON", fake_runtime_python)
    monkeypatch.setattr(probe_module.Path, "is_file", lambda self: self == fake_runtime_python)

    captured: dict[str, object] = {}

    def fake_run(command, check, capture_output, text, timeout):
        captured["command"] = command
        captured["timeout"] = timeout
        payload = {
            "installed": True,
            "import_probe_passed": True,
            "import_attempted": True,
            "package_name": "openai-agents-python",
            "import_name": "agents",
            "version_if_available": "1.0.0",
            "runtime_python": str(fake_runtime_python),
            "errors": [],
        }
        return type(
            "CompletedProcess",
            (),
            {
                "returncode": 0,
                "stdout": json.dumps(payload),
                "stderr": "",
            },
        )()

    monkeypatch.setattr(probe_module.subprocess, "run", fake_run)

    result = probe_module._probe_import_in_external_runtime("openai-agents-python", "agents")

    assert captured["command"][0] == str(fake_runtime_python)
    assert captured["timeout"] == 60
    assert result.installed is True
    assert result.import_probe_passed is True
    assert result.import_attempted is True
    assert result.runtime_capability_verified is False
    assert result.package_name == "openai-agents-python"
    assert result.import_name == "agents"
    assert result.version_if_available == "1.0.0"
    assert result.runtime_python == str(fake_runtime_python)
    assert result.errors == ()


def test_agent_tooling_runtime_probe_reports_missing_runtime_python(monkeypatch) -> None:
    monkeypatch.setenv("MAKSIMAR_MODEL_FREE_STARTUP", "0")
    fake_runtime_python = Path("/dev/shm/missing_agent_tooling_runtime_python")
    monkeypatch.setattr(probe_module, "EXTERNAL_RUNTIME_PYTHON", fake_runtime_python)
    monkeypatch.setattr(probe_module.Path, "is_file", lambda self: False)

    result = probe_module._probe_import_in_external_runtime("mcp", "mcp")

    assert result.installed is False
    assert result.import_probe_passed is False
    assert result.errors == ("runtime_python_missing",)


def test_core_contract_without_server_observation_never_proves_import():
    from MAKSIMAR_CORE_LIB.action_library_adapters import agent_tooling_runtime_probe as contract
    result = contract.build_agent_tooling_runtime_probe_read_model()
    imports = [row for row in result["probe_results"] if row["probe_kind"] == "IMPORT"]
    assert imports
    assert all(row["installed"] is False and row["import_probe_passed"] is False
               and row["import_attempted"] is False and row["runtime_capability_verified"] is False
               and row["errors"] == ("probe_observation_required",) for row in imports)
