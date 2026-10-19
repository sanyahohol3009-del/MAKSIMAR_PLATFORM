from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUNTIME_LIBRARY_STORE_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_library"
FLUTTER_RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "tools" / "flutter"
_CATEGORY_ORDER = ("agents", "skills_rag", "tools_browser")


def _runtime_library_operator_flags() -> dict[str, Any]:
    return {
        "runtime_library_visible": True,
        "runtime_library_visibility_allowed": True,
        "runtime_library_execution_allowed": True,
        "agent_selection_allowed": True,
        "skill_selection_allowed": True,
        "tool_selection_allowed": True,
        "external_adapter_selection_allowed": True,
        "import_probe_allowed": True,
        "runtime_import_probe_allowed": True,
        "runtime_probe_allowed": True,
        "sandbox_probe_allowed": True,
        "sandbox_execution_allowed": True,
        "approval_required_for_runtime_execution": True,
        "direct_execution_allowed": False,
        "core_write_allowed": False,
        "canonical_write_allowed": False,
        "direct_core_mutation_allowed": False,
        "auto_apply_allowed": False,
        "auto_git_add_allowed": False,
        "auto_git_commit_allowed": False,
        "auto_git_push_allowed": False,
        "auto_install_allowed": False,
        "auto_download_allowed": False,
        "pc_control_without_approval": False,
        "browser_control_without_approval": False,
        "mobile_control_without_approval": False,
    }


def _safe_json_load(
    path: Path, *, store_root: Path | None = None,
    observations: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    status = "READ"
    payload: Any = {}
    try:
        if store_root is not None and not path.resolve().is_relative_to(store_root.resolve()):
            status = "PATH_DENIED"
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                status = "INVALID_OBJECT"
    except FileNotFoundError:
        status = "MISSING"
    except PermissionError:
        status = "PERMISSION_DENIED"
    except (OSError, ValueError):
        status = "UNREADABLE_OR_INVALID"
    if observations is not None:
        observations.append({"path": str(path), "status": status})
    return payload if status == "READ" else {}


def _normalize_category(value: str) -> str:
    category = str(value or "").strip().casefold()
    return category if category in _CATEGORY_ORDER else "unknown"


def _category_label(category: str) -> str:
    return {
        "agents": "agents",
        "skills_rag": "skills/rag",
        "tools_browser": "tools/browser",
    }.get(category, category)


def _manifest_dir(store_root: Path) -> Path:
    return store_root / "manifests"


def _probe_report_dir(store_root: Path) -> Path:
    return store_root / "probe_reports"


def _load_runtime_library_manifests(store_root: Path, observations: list[dict[str, str]] | None = None) -> tuple[dict[str, Any], ...]:
    manifest_dir = _manifest_dir(store_root)
    if not manifest_dir.exists():
        return ()
    manifests: list[dict[str, Any]] = []
    for path in sorted(manifest_dir.glob("*.json")):
        payload = _safe_json_load(path, store_root=store_root, observations=observations)
        manifest_id = str(payload.get("manifest_id", "")).strip()
        if not manifest_id:
            continue
        category = _normalize_category(payload.get("category", ""))
        report_file = str(payload.get("report_file", "")).strip()
        if not report_file:
            report_file = str(_probe_report_dir(store_root) / f"{category}_import_probe.json")
        elif not Path(report_file).is_absolute():
            report_file = str(store_root / report_file)
        # Resolve once: loading, package lookup and provenance share the same path.
        manifests.append(
            {
                "manifest_id": manifest_id,
                "category": category,
                "runtime_only": bool(payload.get("runtime_only", True)),
                "direct_execution_allowed": bool(payload.get("direct_execution_allowed", False)),
                "approval_required_for_write_or_action": bool(
                    payload.get("approval_required_for_write_or_action", True)
                ),
                "report_file": report_file,
                "notes": str(payload.get("notes", "")).strip(),
                "manifest_path": str(path),
            }
        )
    for manifest in manifests:
        manifest["ambiguous_manifest"] = sum(row["manifest_id"] == manifest["manifest_id"] for row in manifests) != 1
    return tuple(manifests)


def _load_probe_payloads(store_root: Path, manifests: tuple[dict[str, Any], ...], observations: list[dict[str, str]] | None = None) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for manifest in manifests:
        report_file = str(manifest.get("report_file", "")).strip()
        if report_file:
            report_path = Path(report_file)
        else:
            report_path = _probe_report_dir(store_root) / f"{manifest['category']}_import_probe.json"
        payloads[str(report_path)] = _safe_json_load(report_path, store_root=store_root, observations=observations)
    return payloads


def _build_package_entry(manifest: dict[str, Any], probe_payload: dict[str, Any], report_file: str) -> dict[str, Any]:
    manifest_id = str(manifest.get("manifest_id", "")).strip()
    category = _normalize_category(manifest.get("category", ""))
    packages = probe_payload.get("packages", ())
    candidates = [
        item for item in packages
        if isinstance(item, dict) and str(item.get("pip_name", "")).strip() == manifest_id
    ] if isinstance(packages, (list, tuple)) else []
    ambiguous = bool(manifest.get("ambiguous_manifest")) or len(candidates) > 1
    package_payload = candidates[0] if len(candidates) == 1 and not ambiguous else {}
    import_ok = package_payload.get("import_ok") is True
    evidence_error = (
        "ambiguous_package_identity" if ambiguous else
        "package_evidence_missing_or_invalid" if not package_payload else
        "invalid_import_status" if not isinstance(package_payload.get("import_ok"), bool) else ""
    )
    package_entry = {
        "package_name": manifest_id,
        "module_name": str(package_payload.get("module_name", "")).strip(),
        "version": str(package_payload.get("version", "")).strip(),
        "import_ok": import_ok,
        "category": category,
        "category_label": _category_label(category),
        "runtime_only": bool(manifest.get("runtime_only", True)),
        "execution_enabled": import_ok,
        "execution_allowed": True,
        "install_allowed": False,
        "download_allowed": False,
        "approval_required_for_write_or_action": bool(manifest.get("approval_required_for_write_or_action", True)),
        "probe_report_file": report_file,
        "venv_name": str(probe_payload.get("venv_name", "")).strip(),
        "runtime_python": str(probe_payload.get("python", "")).strip(),
        "error": evidence_error or str(package_payload.get("error", "")).strip(),
        "probe_observation_only": True,
        "current_execution_verified": False,
        "probe_freshness": "UNASSESSED",
        "probe_observed_at": str(probe_payload.get("observed_at", "")),
        "notes": str(manifest.get("notes", "")).strip(),
    }
    package_entry.update(_runtime_library_operator_flags())
    return package_entry


def build_runtime_library_store_read_model(store_root: Path | None = None) -> dict[str, Any]:
    root = store_root or RUNTIME_LIBRARY_STORE_ROOT
    observations: list[dict[str, str]] = []
    manifests = _load_runtime_library_manifests(root, observations)
    probe_payloads = _load_probe_payloads(root, manifests, observations)

    packages = tuple(
        _build_package_entry(
            manifest,
            probe_payloads.get(str(manifest.get("report_file", "")), {}),
            str(manifest.get("report_file", "")).strip(),
        )
        for manifest in manifests
    )
    available_packages = tuple(package for package in packages if bool(package.get("import_ok", False)))
    unavailable_packages = tuple(package for package in packages if not bool(package.get("import_ok", False)))

    packages_by_category = {
        category: tuple(package for package in packages if package["category"] == category)
        for category in _CATEGORY_ORDER
    }
    available_names = tuple(package["package_name"] for package in available_packages)
    module_names = tuple(package["module_name"] for package in packages if package["module_name"])

    payload = {
        "store_root": str(root),
        "manifest_dir": str(_manifest_dir(root)),
        "probe_report_dir": str(_probe_report_dir(root)),
        "packages": packages,
        "available_packages": available_packages,
        "unavailable_packages": unavailable_packages,
        "package_names": tuple(package["package_name"] for package in packages),
        "available_package_names": available_names,
        "module_names": module_names,
        "agents": packages_by_category["agents"],
        "skills_rag": packages_by_category["skills_rag"],
        "tools_browser": packages_by_category["tools_browser"],
        "categories": _CATEGORY_ORDER,
        "runtime_only": True,
        "read_only": True,
        "install_allowed": False,
        "download_allowed": False,
        "browser_control_allowed": False,
        # Legacy name retains attempted report identities for existing callers.
        "probe_reports_read": tuple(sorted(path for path in probe_payloads if path)),
        "probe_reports_loaded": tuple(sorted({
            row["path"] for row in observations
            if row["status"] == "READ" and row["path"] in probe_payloads
        })),
        "source_observations": tuple(observations),
        "source_errors": tuple(row for row in observations if row["status"] != "READ"),
        "probe_observation_only": True,
        "current_execution_verified": False,
        "probe_freshness": "UNASSESSED",
        "available_count": len(available_packages),
        "unavailable_count": len(unavailable_packages),
        "selection_enabled_package_names": available_names,
    }
    payload.update(_runtime_library_operator_flags())
    return payload


def build_flutter_runtime_status_read_model(
    flutter_root: Path | None = None,
) -> dict[str, Any]:
    root = flutter_root or FLUTTER_RUNTIME_ROOT
    executable = root / "bin" / "flutter"
    version_file = root / "bin" / "cache" / "flutter.version.json"
    return {
        "runtime_root": str(root),
        "installed": root.is_dir(),
        "executable_path": str(executable),
        "executable_present": executable.is_file(),
        "version_file": str(version_file),
        "version": _safe_json_load(version_file),
        "status_probe_only": True,
        "command_executed": False,
        "build_or_deploy_executed": False,
        "read_only": True,
    }
