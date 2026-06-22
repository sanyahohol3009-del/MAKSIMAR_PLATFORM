from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


RUNTIME_LIBRARY_STORE_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_library"
_CATEGORY_ORDER = ("agents", "skills_rag", "tools_browser")
_CATEGORY_ALIASES = {
    "agents": ("agent", "agents", "агент", "агенты", "workflow", "оркестр", "adapter", "mcp"),
    "skills_rag": ("rag", "retrieval", "skill", "skills", "скил", "навык", "langchain", "llama", "duckdb", "pandas"),
    "tools_browser": ("browser", "playwright", "web", "site", "страниц", "браузер"),
}
_TOKEN_RE = re.compile(r"[a-z0-9_.-]+|[а-яё0-9_.-]+", flags=re.IGNORECASE)


def _safe_json_load(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


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


def _load_runtime_library_manifests(store_root: Path) -> tuple[dict[str, Any], ...]:
    manifest_dir = _manifest_dir(store_root)
    if not manifest_dir.exists():
        return ()
    manifests: list[dict[str, Any]] = []
    for path in sorted(manifest_dir.glob("*.json")):
        payload = _safe_json_load(path)
        manifest_id = str(payload.get("manifest_id", "")).strip()
        if not manifest_id:
            continue
        manifests.append(
            {
                "manifest_id": manifest_id,
                "category": _normalize_category(payload.get("category", "")),
                "runtime_only": bool(payload.get("runtime_only", True)),
                "direct_execution_allowed": bool(payload.get("direct_execution_allowed", False)),
                "approval_required_for_write_or_action": bool(
                    payload.get("approval_required_for_write_or_action", True)
                ),
                "report_file": str(payload.get("report_file", "")).strip(),
                "notes": str(payload.get("notes", "")).strip(),
                "manifest_path": str(path),
            }
        )
    return tuple(manifests)


def _load_probe_payloads(store_root: Path, manifests: tuple[dict[str, Any], ...]) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for manifest in manifests:
        report_file = str(manifest.get("report_file", "")).strip()
        if report_file:
            report_path = Path(report_file)
        else:
            report_path = _probe_report_dir(store_root) / f"{manifest['category']}_import_probe.json"
        payloads[str(report_path)] = _safe_json_load(report_path)
    return payloads


def _build_package_entry(manifest: dict[str, Any], probe_payload: dict[str, Any], report_file: str) -> dict[str, Any]:
    manifest_id = str(manifest.get("manifest_id", "")).strip()
    category = _normalize_category(manifest.get("category", ""))
    packages = probe_payload.get("packages", ())
    package_payload = next(
        (
            item
            for item in packages
            if isinstance(item, dict) and str(item.get("pip_name", "")).strip() == manifest_id
        ),
        {},
    )
    import_ok = bool(package_payload.get("import_ok", False))
    return {
        "package_name": manifest_id,
        "module_name": str(package_payload.get("module_name", "")).strip(),
        "version": str(package_payload.get("version", "")).strip(),
        "import_ok": import_ok,
        "category": category,
        "category_label": _category_label(category),
        "runtime_only": bool(manifest.get("runtime_only", True)),
        "execution_enabled": False,
        "execution_allowed": False,
        "direct_execution_allowed": False,
        "install_allowed": False,
        "download_allowed": False,
        "approval_required_for_write_or_action": bool(manifest.get("approval_required_for_write_or_action", True)),
        "probe_report_file": report_file,
        "venv_name": str(probe_payload.get("venv_name", "")).strip(),
        "runtime_python": str(probe_payload.get("python", "")).strip(),
        "error": str(package_payload.get("error", "")).strip(),
        "notes": str(manifest.get("notes", "")).strip(),
    }


def build_runtime_library_store_read_model(store_root: Path | None = None) -> dict[str, Any]:
    root = store_root or RUNTIME_LIBRARY_STORE_ROOT
    manifests = _load_runtime_library_manifests(root)
    probe_payloads = _load_probe_payloads(root, manifests)

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

    return {
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
        "execution_allowed": False,
        "direct_execution_allowed": False,
        "canonical_write_allowed": False,
        "install_allowed": False,
        "download_allowed": False,
        "browser_control_allowed": False,
        "probe_reports_read": tuple(sorted(path for path in probe_payloads if path)),
        "available_count": len(available_packages),
        "unavailable_count": len(unavailable_packages),
        "selection_enabled_package_names": available_names,
    }


def _semantic_tokens(text: str) -> tuple[str, ...]:
    tokens = [token.strip("._- ") for token in _TOKEN_RE.findall(str(text or "").casefold())]
    return tuple(token for token in dict.fromkeys(tokens) if token)


def select_runtime_library_candidates_for_text(
    user_text: str,
    read_model: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ...]:
    runtime_libraries = read_model or build_runtime_library_store_read_model()
    request_tokens = set(_semantic_tokens(user_text))
    lowered = str(user_text or "").casefold()
    candidates: list[dict[str, Any]] = []

    for package in runtime_libraries.get("packages", ()):
        if not isinstance(package, dict):
            continue
        category = str(package.get("category", ""))
        package_name = str(package.get("package_name", ""))
        module_name = str(package.get("module_name", ""))
        package_tokens = set(_semantic_tokens(f"{package_name} {module_name} {category} {_category_label(category)}"))
        overlap = sorted(request_tokens & package_tokens)
        score = 0.0
        reasons: list[str] = []
        if package_name and package_name.casefold() in lowered:
            score += 4.0
            reasons.append(f"package_match={package_name}")
        if module_name and module_name.casefold() in lowered:
            score += 3.5
            reasons.append(f"module_match={module_name}")
        if overlap:
            score += min(3.0, float(len(overlap)))
            reasons.append(f"token_overlap={','.join(overlap[:6])}")
        if any(alias in lowered for alias in _CATEGORY_ALIASES.get(category, ())):
            score += 1.5
            reasons.append(f"category_match={category}")
        if score <= 0:
            continue
        candidates.append(
            {
                "package_name": package_name,
                "module_name": module_name,
                "category": category,
                "version": str(package.get("version", "")),
                "import_ok": bool(package.get("import_ok", False)),
                "runtime_only": True,
                "execution_allowed": False,
                "score": round(score, 3),
                "reason": "; ".join(reasons) if reasons else "semantic_match",
            }
        )

    return tuple(
        sorted(
            candidates,
            key=lambda item: (-float(item["score"]), 0 if bool(item["import_ok"]) else 1, str(item["package_name"])),
        )
    )
