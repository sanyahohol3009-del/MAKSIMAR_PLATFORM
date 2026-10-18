from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import load_external_tool_manifests


# The project-local isolated runtime is the authoritative P2 provider runtime.
# Keep this explicit and repository-relative so probes cannot silently drift to
# an older machine-wide venv with different framework versions.
EXTERNAL_RUNTIME_PYTHON = (
    Path(__file__).resolve().parents[2]
    / "EXTERNAL_BACKENDS/agent_tooling/venv/bin/python"
)
EXTERNAL_IMPORT_PROBE_TIMEOUT_SECONDS = 60


@dataclass(frozen=True, slots=True)
class AgentToolingRuntimeProbeResult:
    installed: bool
    import_probe_passed: bool
    package_name: str
    import_name: str
    version_if_available: str
    runtime_python: str
    errors: tuple[str, ...]
    probe_kind: str = "IMPORT"
    path_exists: bool | None = None
    package_metadata_exists: bool | None = None
    import_attempted: bool | None = None
    runtime_capability_verified: bool = False

    def __post_init__(self) -> None:
        if type(self.installed) is not bool or type(self.import_probe_passed) is not bool:
            raise ValueError("probe_truth_requires_boolean")
        for value in (self.path_exists, self.package_metadata_exists, self.import_attempted):
            if value is not None and type(value) is not bool:
                raise ValueError("probe_observation_requires_boolean_or_unknown")
        if self.probe_kind not in {"IMPORT", "PATH_EXISTS"}:
            raise ValueError("unknown_probe_kind")
        if self.probe_kind == "PATH_EXISTS" and (self.import_attempted or self.import_probe_passed):
            raise ValueError("path_presence_is_not_import_proof")
        if self.import_probe_passed and self.import_attempted is False:
            raise ValueError("import_pass_requires_attempt")
        if self.runtime_capability_verified is not False:
            raise ValueError("import_or_path_probe_is_not_runtime_capability_verification")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "installed": self.installed,
            "import_probe_passed": self.import_probe_passed,
            "package_name": self.package_name,
            "import_name": self.import_name,
            "version_if_available": self.version_if_available,
            "runtime_python": self.runtime_python,
            "errors": self.errors,
            "probe_kind": self.probe_kind,
            "path_exists": self.path_exists,
            "package_metadata_exists": self.package_metadata_exists,
            "import_attempted": self.import_attempted,
            "runtime_capability_verified": self.runtime_capability_verified,
        }


def _probe_import_in_external_runtime(package_name: str, import_name: str) -> AgentToolingRuntimeProbeResult:
    return _probe_import_with_runtime_python(str(EXTERNAL_RUNTIME_PYTHON), package_name, import_name)


def _probe_path_only_manifest(path_value: str, capability_name: str) -> AgentToolingRuntimeProbeResult:
    target_path = Path(path_value).expanduser()
    path_exists = target_path.exists()
    return AgentToolingRuntimeProbeResult(
        installed=path_exists,
        import_probe_passed=False,
        package_name=capability_name,
        import_name=capability_name,
        version_if_available="",
        runtime_python=str(target_path),
        errors=() if path_exists else ("external_path_missing",),
        probe_kind="PATH_EXISTS",
        path_exists=path_exists,
        package_metadata_exists=None,
        import_attempted=False,
    )


def _probe_import_with_runtime_python(runtime_python: str, package_name: str, import_name: str) -> AgentToolingRuntimeProbeResult:
    runtime_python_path = Path(runtime_python)
    if not runtime_python_path.is_file():
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=("runtime_python_missing",),
            import_attempted=False,
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
    "import_attempted": False,
    "package_name": package_name,
    "import_name": import_name,
    "version_if_available": "",
    "runtime_python": sys.executable,
    "errors": [],
}
try:
    result["import_attempted"] = True
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
    try:
        completed = subprocess.run(
            [runtime_python, "-c", probe_script, package_name, import_name],
            check=False,
            capture_output=True,
            text=True,
            timeout=EXTERNAL_IMPORT_PROBE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return AgentToolingRuntimeProbeResult(
            installed=False, import_probe_passed=False, package_name=package_name,
            import_name=import_name, version_if_available="", runtime_python=runtime_python,
            errors=(type(exc).__name__,), import_attempted=None if isinstance(exc, subprocess.TimeoutExpired) else False,
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
            import_attempted=None,
        )
    try:
        payload = json.loads(completed.stdout.strip() or "{}")
    except (json.JSONDecodeError, TypeError) as exc:
        return AgentToolingRuntimeProbeResult(
            installed=False,
            import_probe_passed=False,
            package_name=package_name,
            import_name=import_name,
            version_if_available="",
            runtime_python=runtime_python,
            errors=(f"invalid_probe_json:{type(exc).__name__}",),
            import_attempted=None,
        )
    if not isinstance(payload, dict):
        return AgentToolingRuntimeProbeResult(
            installed=False, import_probe_passed=False, package_name=package_name,
            import_name=import_name, version_if_available="", runtime_python=runtime_python,
            errors=("invalid_probe_object",), import_attempted=None,
        )
    identity_matches = payload.get("package_name", package_name) == package_name and payload.get("import_name", import_name) == import_name
    errors = payload.get("errors", [])
    if isinstance(errors, str):
        errors = [errors]
    if not isinstance(errors, (list, tuple)):
        errors = ["invalid_probe_errors"]
    if not identity_matches:
        errors = [*errors, "probe_identity_mismatch"]
    if completed.returncode != 0:
        errors = [*errors, f"returncode:{completed.returncode}"]
    attempted = payload.get("import_attempted", True if payload.get("import_probe_passed") is True else None)
    attempted = attempted if type(attempted) is bool else None
    valid_import = identity_matches and completed.returncode == 0 and not errors and attempted is True
    return AgentToolingRuntimeProbeResult(
        installed=payload.get("installed") is True and identity_matches,
        import_probe_passed=payload.get("import_probe_passed") is True and valid_import,
        package_name=package_name,
        import_name=import_name,
        version_if_available=str(payload.get("version_if_available", "")) if identity_matches else "",
        runtime_python=str(payload.get("runtime_python", runtime_python)),
        errors=tuple(str(error) for error in errors if str(error).strip()),
        import_attempted=attempted,
        package_metadata_exists=bool(str(payload.get("version_if_available", "")).strip()) if valid_import and payload.get("import_probe_passed") is True else None,
    )


def probe_agent_tooling_runtime() -> tuple[AgentToolingRuntimeProbeResult, ...]:
    results: list[AgentToolingRuntimeProbeResult] = []
    for manifest in load_external_tool_manifests():
        metadata = manifest.metadata if isinstance(manifest.metadata, dict) else {}
        external_path = str(metadata.get("external_path", "")).strip()
        if external_path:
            results.append(_probe_path_only_manifest(external_path, manifest.tool_id))
            continue
        runtime_selector = str(metadata.get("probe_runtime", "")).strip()
        package_name = manifest.package_name or manifest.module_import_name or manifest.tool_id
        import_name = manifest.module_import_name or manifest.package_name or manifest.tool_id
        if runtime_selector == "current_python":
            results.append(_probe_import_with_runtime_python(sys.executable, package_name, import_name))
            continue
        results.append(_probe_import_in_external_runtime(package_name, import_name))
    return tuple(results)


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
