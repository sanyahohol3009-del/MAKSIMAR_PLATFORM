from __future__ import annotations

import json
from pathlib import Path

from tools.jarvis_live_runtime import agent_tooling_runtime_probe as probe_module


def test_agent_tooling_runtime_probe_smoke(monkeypatch) -> None:
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
    assert captured["timeout"] == 30
    assert result.installed is True
    assert result.import_probe_passed is True
    assert result.package_name == "openai-agents-python"
    assert result.import_name == "agents"
    assert result.version_if_available == "1.0.0"
    assert result.runtime_python == str(fake_runtime_python)
    assert result.errors == ()


def test_agent_tooling_runtime_probe_reports_missing_runtime_python(monkeypatch) -> None:
    fake_runtime_python = Path("/dev/shm/missing_agent_tooling_runtime_python")
    monkeypatch.setattr(probe_module, "EXTERNAL_RUNTIME_PYTHON", fake_runtime_python)
    monkeypatch.setattr(probe_module.Path, "is_file", lambda self: False)

    result = probe_module._probe_import_in_external_runtime("mcp", "mcp")

    assert result.installed is False
    assert result.import_probe_passed is False
    assert result.errors == ("runtime_python_missing",)
