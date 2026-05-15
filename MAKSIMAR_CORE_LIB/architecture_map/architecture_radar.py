from __future__ import annotations

import ast
import fnmatch
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BLUEPRINT_PATH = Path(__file__).resolve().with_name("architecture_blueprint.json")


@dataclass(frozen=True)
class ArchitectureViolation:
    code: str
    message: str
    file_path: str | None = None
    line: int | None = None
    source_layer: str | None = None
    target_layer: str | None = None
    imported_module: str | None = None

    def render(self) -> str:
        location = ""
        if self.file_path:
            location = self.file_path
            if self.line is not None:
                location = f"{location}:{self.line}"
            location = f"{location} | "

        imported = ""
        if self.imported_module:
            imported = f" | import={self.imported_module}"

        layers = ""
        if self.source_layer or self.target_layer:
            layers = f" | {self.source_layer or '?'} -> {self.target_layer or '?'}"

        return f"[{self.code}] {location}{self.message}{layers}{imported}"


@dataclass(frozen=True)
class LayerRadarStatus:
    layer_id: str
    title: str
    declared_status: str
    runtime_status: str
    existing_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    py_file_count: int
    non_init_py_file_count: int
    container_status: str
    container_found_markers: tuple[str, ...]
    container_missing_markers: tuple[str, ...]
    import_guard_enabled: bool


@dataclass
class ArchitectureReport:
    blueprint_id: str
    layer_statuses: list[LayerRadarStatus] = field(default_factory=list)
    violations: list[ArchitectureViolation] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return bool(self.violations)

    def failure_text(self) -> str:
        if not self.violations:
            return "Architecture Drift Guard: OK"

        lines = [
            "",
            "MAKSIMAR ARCHITECTURE DRIFT GUARD FAILED",
            "=" * 72,
        ]
        for violation in self.violations:
            lines.append(violation.render())
        return "\n".join(lines)

    def terminal_text(self) -> str:
        lines: list[str] = []
        lines.append("")
        lines.append("MAKSIMAR ARCHITECTURE RADAR")
        lines.append("=" * 72)
        lines.append(f"Blueprint: {self.blueprint_id}")
        lines.append("")
        lines.append(
            f"{'LAYER':<26} {'STATUS':<20} {'PY':>5} {'CONTAINER':<18} {'DRIFT'}"
        )
        lines.append("-" * 90)

        for status in self.layer_statuses:
            drift = "ON" if status.import_guard_enabled else "OFF"
            lines.append(
                f"{status.layer_id:<26} "
                f"{status.runtime_status:<20} "
                f"{status.py_file_count:>5} "
                f"{status.container_status:<18} "
                f"{drift}"
            )

        lines.append("-" * 90)

        ready_count = sum(1 for s in self.layer_statuses if s.runtime_status == "ГОТОВО")
        skeleton_count = sum(1 for s in self.layer_statuses if s.runtime_status == "КАРКАС")
        planned_count = sum(
            1 for s in self.layer_statuses if s.runtime_status == "ЗАПЛАНИРОВАНО/ПУСТО"
        )
        empty_count = sum(1 for s in self.layer_statuses if s.runtime_status == "ПАПКА_БЕЗ_PY")

        lines.append(
            "Summary: "
            f"ready={ready_count}, "
            f"skeleton={skeleton_count}, "
            f"empty={empty_count}, "
            f"planned={planned_count}, "
            f"violations={len(self.violations)}"
        )

        container_pending = [
            s.layer_id
            for s in self.layer_statuses
            if s.py_file_count > 0 and s.container_status in {"CONTAINER_PENDING", "CONTAINER_PARTIAL"}
        ]
        if container_pending:
            lines.append("")
            lines.append("Containerization readiness:")
            for layer_id in container_pending:
                lines.append(f"  - {layer_id}: container markers incomplete")

        if self.violations:
            lines.append("")
            lines.append("Drift violations:")
            for violation in self.violations[:30]:
                lines.append(f"  - {violation.render()}")
            if len(self.violations) > 30:
                lines.append(f"  ... and {len(self.violations) - 30} more")
        else:
            lines.append("")
            lines.append("Drift Guard: OK")

        return "\n".join(lines)


def load_blueprint(blueprint_path: Path = DEFAULT_BLUEPRINT_PATH) -> dict[str, Any]:
    with blueprint_path.open("r", encoding="utf-8") as handle:
        blueprint = json.load(handle)

    if not isinstance(blueprint, dict):
        raise ValueError("Architecture blueprint must be a JSON object.")

    layers = blueprint.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("Architecture blueprint must contain a non-empty 'layers' list.")

    known_ids: set[str] = set()
    for layer in layers:
        layer_id = layer.get("id")
        if not isinstance(layer_id, str) or not layer_id:
            raise ValueError("Every architecture layer must have a non-empty string id.")
        if layer_id in known_ids:
            raise ValueError(f"Duplicate architecture layer id: {layer_id}")
        known_ids.add(layer_id)

    for layer in layers:
        allowed = layer.get("allowed_import_layer_ids", [])
        forbidden = layer.get("forbidden_import_layer_ids", [])
        for imported_layer_id in [*allowed, *forbidden]:
            if imported_layer_id != "ANY" and imported_layer_id not in known_ids:
                raise ValueError(
                    f"Layer {layer['id']} references unknown layer id: {imported_layer_id}"
                )

    return blueprint


def build_architecture_report(
    project_root: Path = PROJECT_ROOT,
    blueprint_path: Path = DEFAULT_BLUEPRINT_PATH,
) -> ArchitectureReport:
    blueprint = load_blueprint(blueprint_path)
    report = ArchitectureReport(blueprint_id=str(blueprint.get("blueprint_id", "unknown")))

    layers = blueprint["layers"]
    enforcement = blueprint.get("enforcement", {})
    ignored_globs = tuple(blueprint.get("ignored_path_globs", []))
    allowed_unmapped_file_globs = tuple(blueprint.get("allowed_unmapped_file_globs", []))

    layer_statuses = _build_layer_statuses(
        project_root=project_root,
        blueprint=blueprint,
    )
    report.layer_statuses.extend(layer_statuses)

    if enforcement.get("fail_on_missing_mandatory_paths", True):
        report.violations.extend(
            _check_mandatory_paths(
                project_root=project_root,
                layers=layers,
            )
        )

    py_files = list(
        _iter_python_files(
            project_root=project_root,
            ignored_globs=ignored_globs,
        )
    )

    if enforcement.get("fail_on_unregistered_source_file", True):
        report.violations.extend(
            _check_unregistered_source_files(
                project_root=project_root,
                py_files=py_files,
                layers=layers,
                ignored_globs=ignored_globs,
                allowed_unmapped_file_globs=allowed_unmapped_file_globs,
            )
        )

    report.violations.extend(
        _check_import_drift(
            project_root=project_root,
            py_files=py_files,
            layers=layers,
            blueprint=blueprint,
        )
    )

    if enforcement.get("fail_on_container_missing_for_ready_layers", False):
        report.violations.extend(
            _check_container_readiness_enforced(
                report.layer_statuses,
            )
        )

    return report


def assert_architecture_is_clean(
    project_root: Path = PROJECT_ROOT,
    blueprint_path: Path = DEFAULT_BLUEPRINT_PATH,
) -> None:
    report = build_architecture_report(
        project_root=project_root,
        blueprint_path=blueprint_path,
    )
    if report.failed:
        raise AssertionError(report.failure_text())


def _build_layer_statuses(
    project_root: Path,
    blueprint: dict[str, Any],
) -> list[LayerRadarStatus]:
    layers = blueprint["layers"]
    container_config = blueprint.get("containerization", {})
    ready_markers = tuple(container_config.get("ready_markers", []))
    recommended_by_profile = container_config.get("recommended_markers_by_profile", {})

    statuses: list[LayerRadarStatus] = []

    for layer in layers:
        layer_id = layer["id"]
        path_prefixes = tuple(layer.get("path_prefixes", []))
        expected_paths = layer.get("expected_paths", [])
        container_profile = layer.get("container_profile", "server_service")
        recommended_markers = tuple(recommended_by_profile.get(container_profile, ready_markers))

        existing_paths: list[str] = []
        missing_paths: list[str] = []
        layer_py_files: list[Path] = []

        checked_paths = [entry["path"] for entry in expected_paths if "path" in entry]
        if not checked_paths:
            checked_paths = list(path_prefixes)

        for raw_path in checked_paths:
            path = project_root / raw_path
            if path.exists():
                existing_paths.append(raw_path)
                if path.is_dir():
                    layer_py_files.extend(path.rglob("*.py"))
                elif path.suffix == ".py":
                    layer_py_files.append(path)
            else:
                missing_paths.append(raw_path)

        filtered_py_files = [
            path
            for path in layer_py_files
            if "__pycache__" not in path.parts
        ]
        non_init_py_files = [
            path
            for path in filtered_py_files
            if path.name != "__init__.py"
        ]

        if non_init_py_files:
            runtime_status = "ГОТОВО"
        elif filtered_py_files:
            runtime_status = "КАРКАС"
        elif existing_paths:
            runtime_status = "ПАПКА_БЕЗ_PY"
        else:
            runtime_status = "ЗАПЛАНИРОВАНО/ПУСТО"

        found_markers: set[str] = set()
        for raw_path in existing_paths:
            base_path = project_root / raw_path
            if not base_path.is_dir():
                continue
            for marker in recommended_markers:
                if (base_path / marker).exists():
                    found_markers.add(marker)

        missing_markers = tuple(
            marker for marker in recommended_markers if marker not in found_markers
        )

        if not recommended_markers:
            container_status = "N/A"
        elif not filtered_py_files:
            container_status = "CONTAINER_NOT_STARTED"
        elif not found_markers:
            container_status = "CONTAINER_PENDING"
        elif missing_markers:
            container_status = "CONTAINER_PARTIAL"
        else:
            container_status = "CONTAINER_READY"

        statuses.append(
            LayerRadarStatus(
                layer_id=layer_id,
                title=str(layer.get("title", "")),
                declared_status=str(layer.get("status", "")),
                runtime_status=runtime_status,
                existing_paths=tuple(existing_paths),
                missing_paths=tuple(missing_paths),
                py_file_count=len(filtered_py_files),
                non_init_py_file_count=len(non_init_py_files),
                container_status=container_status,
                container_found_markers=tuple(sorted(found_markers)),
                container_missing_markers=missing_markers,
                import_guard_enabled=bool(layer.get("import_guard", True)),
            )
        )

    return statuses


def _check_mandatory_paths(
    project_root: Path,
    layers: list[dict[str, Any]],
) -> list[ArchitectureViolation]:
    violations: list[ArchitectureViolation] = []

    for layer in layers:
        for entry in layer.get("expected_paths", []):
            if not entry.get("mandatory", False):
                continue

            raw_path = entry.get("path")
            if not raw_path:
                continue

            if not (project_root / raw_path).exists():
                violations.append(
                    ArchitectureViolation(
                        code="MISSING_MANDATORY_PATH",
                        message=f"Mandatory architecture path is missing: {raw_path}",
                        source_layer=layer["id"],
                    )
                )

    return violations


def _check_unregistered_source_files(
    project_root: Path,
    py_files: list[Path],
    layers: list[dict[str, Any]],
    ignored_globs: tuple[str, ...],
    allowed_unmapped_file_globs: tuple[str, ...],
) -> list[ArchitectureViolation]:
    violations: list[ArchitectureViolation] = []

    for py_file in py_files:
        rel = _relative_posix(py_file, project_root)

        if _matches_any_glob(rel, ignored_globs):
            continue

        if _matches_any_glob(rel, allowed_unmapped_file_globs):
            continue

        layer = _resolve_file_layer(rel, layers)
        if layer is None:
            violations.append(
                ArchitectureViolation(
                    code="UNREGISTERED_SOURCE_FILE",
                    message="Python file is outside all architecture blueprint path_prefixes.",
                    file_path=rel,
                )
            )

    return violations


def _check_import_drift(
    project_root: Path,
    py_files: list[Path],
    layers: list[dict[str, Any]],
    blueprint: dict[str, Any],
) -> list[ArchitectureViolation]:
    enforcement = blueprint.get("enforcement", {})
    if not enforcement.get("fail_on_forbidden_import", True):
        return []

    ignored_globs = tuple(blueprint.get("ignored_path_globs", []))
    local_roots = _discover_local_python_roots(
        project_root=project_root,
        ignored_globs=ignored_globs,
    )

    violations: list[ArchitectureViolation] = []

    for py_file in py_files:
        rel = _relative_posix(py_file, project_root)

        source_layer = _resolve_file_layer(rel, layers)
        if source_layer is None:
            continue

        if not source_layer.get("import_guard", True):
            continue

        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=rel)
        except SyntaxError as exc:
            violations.append(
                ArchitectureViolation(
                    code="PYTHON_SYNTAX_ERROR",
                    message=f"Cannot parse Python file for architecture drift: {exc}",
                    file_path=rel,
                    line=exc.lineno,
                    source_layer=source_layer["id"],
                )
            )
            continue

        imports = _extract_imports(tree)

        for imported_module, line in imports:
            if not imported_module:
                continue

            target_layer = _resolve_import_layer(imported_module, layers)

            if target_layer is None:
                top_level = imported_module.split(".", 1)[0]
                if (
                    enforcement.get("fail_on_unknown_local_import", True)
                    and top_level in local_roots
                ):
                    violations.append(
                        ArchitectureViolation(
                            code="UNKNOWN_LOCAL_IMPORT",
                            message="Local import does not resolve to any blueprint layer.",
                            file_path=rel,
                            line=line,
                            source_layer=source_layer["id"],
                            imported_module=imported_module,
                        )
                    )
                continue

            source_layer_id = source_layer["id"]
            target_layer_id = target_layer["id"]

            if source_layer_id == target_layer_id:
                continue

            allowed = set(source_layer.get("allowed_import_layer_ids", []))
            forbidden = set(source_layer.get("forbidden_import_layer_ids", []))

            if "ANY" in allowed:
                continue

            if target_layer_id in forbidden:
                violations.append(
                    ArchitectureViolation(
                        code="FORBIDDEN_IMPORT",
                        message="Import explicitly violates forbidden_import_layer_ids.",
                        file_path=rel,
                        line=line,
                        source_layer=source_layer_id,
                        target_layer=target_layer_id,
                        imported_module=imported_module,
                    )
                )
                continue

            if target_layer_id not in allowed:
                violations.append(
                    ArchitectureViolation(
                        code="IMPORT_NOT_ALLOWED",
                        message="Import target layer is not listed in allowed_import_layer_ids.",
                        file_path=rel,
                        line=line,
                        source_layer=source_layer_id,
                        target_layer=target_layer_id,
                        imported_module=imported_module,
                    )
                )

    return violations


def _check_container_readiness_enforced(
    statuses: list[LayerRadarStatus],
) -> list[ArchitectureViolation]:
    violations: list[ArchitectureViolation] = []

    for status in statuses:
        if status.py_file_count <= 0:
            continue

        if status.container_status in {"CONTAINER_PENDING", "CONTAINER_PARTIAL"}:
            violations.append(
                ArchitectureViolation(
                    code="CONTAINER_READINESS_MISSING",
                    message=(
                        "Layer has Python files but containerization markers are incomplete: "
                        f"missing={list(status.container_missing_markers)}"
                    ),
                    source_layer=status.layer_id,
                )
            )

    return violations


def _extract_imports(tree: ast.AST) -> list[tuple[str, int]]:
    imports: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, int(getattr(node, "lineno", 0) or 0)))

        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue

            if node.module:
                imports.append((node.module, int(getattr(node, "lineno", 0) or 0)))

    return imports


def _iter_python_files(
    project_root: Path,
    ignored_globs: tuple[str, ...],
) -> list[Path]:
    result: list[Path] = []

    hard_ignored_dir_names = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        "dist",
        "build",
    }

    for dirpath, dirnames, filenames in os.walk(project_root):
        current = Path(dirpath)
        rel_dir = _relative_posix(current, project_root)

        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in hard_ignored_dir_names
            and not _matches_any_glob(
                f"{rel_dir}/{dirname}/**" if rel_dir != "." else f"{dirname}/**",
                ignored_globs,
            )
        ]

        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            path = current / filename
            rel = _relative_posix(path, project_root)
            if _matches_any_glob(rel, ignored_globs):
                continue

            result.append(path)

    return result


def _discover_local_python_roots(
    project_root: Path,
    ignored_globs: tuple[str, ...],
) -> set[str]:
    roots: set[str] = set()

    for child in project_root.iterdir():
        rel = _relative_posix(child, project_root)
        if _matches_any_glob(rel, ignored_globs) or _matches_any_glob(f"{rel}/**", ignored_globs):
            continue

        if child.is_file() and child.suffix == ".py":
            roots.add(child.stem)

        if child.is_dir():
            try:
                has_python = any(path.suffix == ".py" for path in child.rglob("*.py"))
            except OSError:
                has_python = False

            if has_python:
                roots.add(child.name)

    return roots


def _resolve_file_layer(
    relative_path: str,
    layers: list[dict[str, Any]],
) -> dict[str, Any] | None:
    candidates: list[tuple[int, dict[str, Any]]] = []

    for layer in layers:
        for prefix in layer.get("path_prefixes", []):
            normalized = prefix.strip("/")
            if _path_has_prefix(relative_path, normalized):
                candidates.append((len(normalized), layer))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def _resolve_import_layer(
    module_name: str,
    layers: list[dict[str, Any]],
) -> dict[str, Any] | None:
    candidates: list[tuple[int, dict[str, Any]]] = []

    for layer in layers:
        for prefix in layer.get("module_prefixes", []):
            normalized = prefix.strip(".")
            if _module_has_prefix(module_name, normalized):
                candidates.append((len(normalized), layer))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def _path_has_prefix(relative_path: str, prefix: str) -> bool:
    if not prefix:
        return False
    return relative_path == prefix or relative_path.startswith(f"{prefix}/")


def _module_has_prefix(module_name: str, prefix: str) -> bool:
    if not prefix:
        return False
    return module_name == prefix or module_name.startswith(f"{prefix}.")


def _relative_posix(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _matches_any_glob(path: str, patterns: tuple[str, ...]) -> bool:
    normalized = path.replace("\\", "/")
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in patterns)

if __name__ == "__main__":
    report = build_architecture_report()
    print(report.terminal_text())
    if report.failed:
        raise SystemExit(1)
