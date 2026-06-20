from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import load_external_tool_manifests


EXTERNAL_RUNTIME_PYTHON = Path.home() / "MAKSIMAR_RUNTIME/venvs/agent_tooling/bin/python"


@dataclass(frozen=True, slots=True)
class AgentToolingRuntimeProbeResult:
    installed: bool
    import_probe_passed: bool
    package_name: str
    import_name: str
    version_if_available: str
    runtime_python: str
    errors: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "installed": self.installed,
            "import_probe_passed": self.import_probe_passed,
            "package_name": self.package_name,
            "import_name": self.import_name,
            "version_if_available": self.version_if_available,
            "runtime_python": self.runtime_python,
            "errors": self.errors,
        }


def _probe_import_in_external_runtime(package_name: str, import_name: str) -> AgentToolingRuntimeProbeResult:
    runtime_python = str(EXTERNAL_RUNTIME_PYTHON)
    if not EXTERNAL_RUNTIME_PYTHON.is_file():
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=("runtime_python_missing",),
        )

    probe_script = """
import importlib
import importlib.metadata
import json
import sys

package_name = sys.argv[1]
import_name = sys.argv[2]
result = {
    "installed": False,
    "import_probe_passed": False,
    "package_name": package_name,
    "import_name": import_name,
    "version_if_available": "",
    "runtime_python": sys.executable,
    "errors": [],
}
try:
    importlib.import_module(import_name)
    result["installed"] = True
    result["import_probe_passed"] = True
    try:
        result["version_if_available"] = importlib.metadata.version(package_name)
    except Exception:
        try:
            result["version_if_available"] = importlib.metadata.version(import_name)
        except Exception:
            result["version_if_available"] = ""
except Exception as exc:
    result["errors"] = [f"{type(exc).__name__}:{exc}"]
print(json.dumps(result, ensure_ascii=False))
"""
    completed = subprocess.run(
        [runtime_python, "-c", probe_script, package_name, import_name],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0 and not completed.stdout.strip():
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=(completed.stderr.strip() or f"returncode:{completed.returncode}",),
        )
    try:
        payload = json.loads(completed.stdout.strip() or "{}")
    except json.JSONDecodeError as exc:
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=(f"invalid_probe_json:{exc}",),
        )
    errors = payload.get("errors", [])
    if isinstance(errors, str):
        errors = [errors]
    return AgentToolingRuntimeProbeResult(
        installed=bool(payload.get("installed")),
        import_probe_passed=bool(payload.get("import_probe_passed")),
        package_name=str(payload.get("package_name", package_name)),
        import_name=str(payload.get("import_name", import_name)),
        version_if_available=str(payload.get("version_if_available", "")),
        runtime_python=str(payload.get("runtime_python", runtime_python)),
        errors=tuple(str(error) for error in errors if str(error).strip()),
    )


def probe_agent_tooling_runtime() -> tuple[AgentToolingRuntimeProbeResult, ...]:
    return tuple(
        _probe_import_in_external_runtime(manifest.package_name or manifest.module_import_name, manifest.module_import_name or manifest.package_name)
        for manifest in load_external_tool_manifests()
    )


def build_agent_tooling_runtime_probe_read_model() -> dict[str, Any]:
    results = probe_agent_tooling_runtime()
    return {
        "runtime_python": str(EXTERNAL_RUNTIME_PYTHON),
        "probe_results": tuple(result.to_read_model() for result in results),
        "installed": tuple(result.package_name for result in results if result.installed),
        "import_probe_passed": tuple(result.package_name for result in results if result.import_probe_passed),
        "errors": tuple(result.errors for result in results if result.errors),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe external agent/tooling runtime packages in the isolated venv.")
    parser.parse_args()
    print(json.dumps(build_agent_tooling_runtime_probe_read_model(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
