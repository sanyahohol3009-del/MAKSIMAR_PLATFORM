from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_ROADMAP_PATH = (
    PROJECT_ROOT
    / "docs/architecture/foundation/batched_foundation_roadmap_v2_1_correction_patch.json"
)

DEFAULT_SCHEMA_PATH = (
    PROJECT_ROOT
    / "docs/architecture/foundation/batched_foundation_roadmap_schema_v1.json"
)


class FoundationRoadmapCIError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class FoundationRoadmapIssue:
    level: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class FoundationRoadmapCIReport:
    report_id: str
    roadmap_path: str
    schema_path: str
    roadmap_id: str
    version: str
    phases_count: int
    batches_count: int
    active_batches: tuple[str, ...]
    closed_batches: tuple[str, ...]
    planned_batches: tuple[str, ...]
    forbidden_paths_present: tuple[str, ...]
    missing_required_files: tuple[str, ...]
    issues: tuple[FoundationRoadmapIssue, ...]
    check_passed: bool

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["issues"] = [asdict(issue) for issue in self.issues]
        return payload


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FoundationRoadmapCIError(f"JSON file does not exist: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise FoundationRoadmapCIError(f"JSON root must be object: {path}")

    return payload


def validate_roadmap_shape(roadmap: Mapping[str, Any]) -> tuple[FoundationRoadmapIssue, ...]:
    issues: list[FoundationRoadmapIssue] = []

    required_top_keys = (
        "roadmap_id",
        "version",
        "title",
        "status",
        "description",
        "global_rules",
        "decision_actions",
        "semantic_families",
        "forbidden_paths",
        "phases",
    )

    for key in required_top_keys:
        if key not in roadmap:
            issues.append(FoundationRoadmapIssue("error", key, "missing required top-level key"))

    if issues:
        return tuple(issues)

    _expect_non_empty_string(issues, roadmap, "roadmap_id")
    _expect_non_empty_string(issues, roadmap, "version")
    _expect_non_empty_string(issues, roadmap, "title")
    _expect_non_empty_string(issues, roadmap, "description")
    _expect_string_in(issues, roadmap, "status", {"draft", "active", "closed"})
    _expect_mapping(issues, roadmap, "global_rules")
    _expect_string_list(issues, roadmap, "decision_actions")
    _expect_string_list(issues, roadmap, "semantic_families")
    _expect_string_list(issues, roadmap, "forbidden_paths", allow_empty=True)

    phases = roadmap.get("phases")
    if not isinstance(phases, list) or not phases:
        issues.append(FoundationRoadmapIssue("error", "phases", "phases must be a non-empty list"))
        return tuple(issues)

    seen_phase_ids: set[str] = set()
    seen_batch_ids: set[str] = set()

    for phase_index, phase in enumerate(phases):
        phase_path = f"phases[{phase_index}]"
        if not isinstance(phase, Mapping):
            issues.append(FoundationRoadmapIssue("error", phase_path, "phase must be object"))
            continue

        phase_id = str(phase.get("phase_id", ""))
        if not phase_id:
            issues.append(FoundationRoadmapIssue("error", f"{phase_path}.phase_id", "phase_id must not be empty"))
        elif phase_id in seen_phase_ids:
            issues.append(FoundationRoadmapIssue("error", f"{phase_path}.phase_id", "duplicate phase_id"))
        else:
            seen_phase_ids.add(phase_id)

        _expect_non_empty_string(issues, phase, "title", prefix=phase_path)
        _expect_non_empty_string(issues, phase, "description", prefix=phase_path)
        _expect_string_in(issues, phase, "status", {"planned", "active", "closed"}, prefix=phase_path)

        batches = phase.get("batches")
        if not isinstance(batches, list) or not batches:
            issues.append(FoundationRoadmapIssue("error", f"{phase_path}.batches", "batches must be a non-empty list"))
            continue

        for batch_index, batch in enumerate(batches):
            batch_path = f"{phase_path}.batches[{batch_index}]"
            if not isinstance(batch, Mapping):
                issues.append(FoundationRoadmapIssue("error", batch_path, "batch must be object"))
                continue

            batch_id = str(batch.get("batch_id", ""))
            if not batch_id:
                issues.append(FoundationRoadmapIssue("error", f"{batch_path}.batch_id", "batch_id must not be empty"))
            elif batch_id in seen_batch_ids:
                issues.append(FoundationRoadmapIssue("error", f"{batch_path}.batch_id", "duplicate batch_id"))
            else:
                seen_batch_ids.add(batch_id)

            _expect_string_in(issues, batch, "status", {"CLOSED", "ACTIVE", "PLANNED"}, prefix=batch_path)
            _expect_non_empty_string(issues, batch, "title", prefix=batch_path)
            _expect_non_empty_string(issues, batch, "description", prefix=batch_path)

            for list_key in (
                "base_files",
                "correction_additions",
                "base_tests",
                "correction_tests",
                "dashboard_read_models",
                "acceptance_gates",
            ):
                allow_empty = list_key not in {"acceptance_gates"}
                _expect_string_list(issues, batch, list_key, prefix=batch_path, allow_empty=allow_empty)

            for bool_key in (
                "semantic_duplicate_scan_required",
                "manifest_required",
                "container_boundary_required",
                "full_auto_pytest_required",
            ):
                if not isinstance(batch.get(bool_key), bool):
                    issues.append(
                        FoundationRoadmapIssue(
                            "error",
                            f"{batch_path}.{bool_key}",
                            f"{bool_key} must be boolean",
                        )
                    )

            if batch.get("full_auto_pytest_required") is not True:
                issues.append(
                    FoundationRoadmapIssue(
                        "error",
                        f"{batch_path}.full_auto_pytest_required",
                        "full auto pytest is mandatory for every batch",
                    )
                )

            if batch.get("status") in {"ACTIVE", "PLANNED"} and batch.get("semantic_duplicate_scan_required") is not True:
                if batch_id != "0.1":
                    issues.append(
                        FoundationRoadmapIssue(
                            "error",
                            f"{batch_path}.semantic_duplicate_scan_required",
                            "semantic duplicate scan is mandatory for active/planned batches",
                        )
                    )

    return tuple(issues)


def build_ci_report(
    *,
    roadmap_path: Path = DEFAULT_ROADMAP_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
    batch_id: str | None = None,
    require_files: bool = False,
) -> FoundationRoadmapCIReport:
    roadmap = load_json_file(roadmap_path)
    schema = load_json_file(schema_path)

    issues = list(validate_roadmap_shape(roadmap))
    issues.extend(_validate_schema_shape(schema))

    phases = tuple(_iter_phases(roadmap))
    batches = tuple(_iter_batches(roadmap))

    filtered_batches = tuple(
        batch for batch in batches if batch_id is None or str(batch.get("batch_id")) == batch_id
    )

    if batch_id is not None and not filtered_batches:
        issues.append(FoundationRoadmapIssue("error", "batch_id", f"batch not found: {batch_id}"))

    forbidden_paths_present = _existing_paths(roadmap.get("forbidden_paths", []))

    if forbidden_paths_present:
        for path in forbidden_paths_present:
            issues.append(FoundationRoadmapIssue("error", "forbidden_paths", f"forbidden path exists: {path}"))

    missing_required_files: tuple[str, ...] = ()
    if require_files:
        required_paths = tuple(_required_paths_for_batches(filtered_batches))
        missing_required_files = _missing_paths(required_paths)
        for path in missing_required_files:
            issues.append(FoundationRoadmapIssue("error", "required_files", f"required path missing: {path}"))

    active_batches = tuple(str(batch["batch_id"]) for batch in batches if batch.get("status") == "ACTIVE")
    closed_batches = tuple(str(batch["batch_id"]) for batch in batches if batch.get("status") == "CLOSED")
    planned_batches = tuple(str(batch["batch_id"]) for batch in batches if batch.get("status") == "PLANNED")

    check_passed = not any(issue.level == "error" for issue in issues)

    return FoundationRoadmapCIReport(
        report_id="foundation_roadmap_ci_report_v1",
        roadmap_path=str(roadmap_path.relative_to(PROJECT_ROOT)),
        schema_path=str(schema_path.relative_to(PROJECT_ROOT)),
        roadmap_id=str(roadmap.get("roadmap_id", "")),
        version=str(roadmap.get("version", "")),
        phases_count=len(phases),
        batches_count=len(batches),
        active_batches=active_batches,
        closed_batches=closed_batches,
        planned_batches=planned_batches,
        forbidden_paths_present=forbidden_paths_present,
        missing_required_files=missing_required_files,
        issues=tuple(issues),
        check_passed=check_passed,
    )


def _validate_schema_shape(schema: Mapping[str, Any]) -> tuple[FoundationRoadmapIssue, ...]:
    issues: list[FoundationRoadmapIssue] = []

    if schema.get("type") != "object":
        issues.append(FoundationRoadmapIssue("error", "schema.type", "schema root type must be object"))

    required = schema.get("required")
    if not isinstance(required, list) or not required:
        issues.append(FoundationRoadmapIssue("error", "schema.required", "schema required must be non-empty list"))

    defs = schema.get("$defs")
    if not isinstance(defs, Mapping):
        issues.append(FoundationRoadmapIssue("error", "schema.$defs", "schema must define $defs"))

    return tuple(issues)


def _iter_phases(roadmap: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    phases = roadmap.get("phases", [])
    if not isinstance(phases, list):
        return ()
    return (phase for phase in phases if isinstance(phase, Mapping))


def _iter_batches(roadmap: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    for phase in _iter_phases(roadmap):
        batches = phase.get("batches", [])
        if not isinstance(batches, list):
            continue
        for batch in batches:
            if isinstance(batch, Mapping):
                yield batch


def _required_paths_for_batches(batches: Iterable[Mapping[str, Any]]) -> Iterable[str]:
    for batch in batches:
        for key in ("base_files", "correction_additions", "base_tests", "correction_tests"):
            values = batch.get(key, [])
            if not isinstance(values, list):
                continue
            for value in values:
                if isinstance(value, str) and value.strip():
                    yield value


def _missing_paths(paths: Iterable[str]) -> tuple[str, ...]:
    missing: list[str] = []
    for raw_path in paths:
        path = PROJECT_ROOT / raw_path
        if not path.exists():
            missing.append(raw_path)
    return tuple(sorted(set(missing)))


def _existing_paths(paths: Iterable[str]) -> tuple[str, ...]:
    existing: list[str] = []
    for raw_path in paths:
        path = PROJECT_ROOT / raw_path
        if path.exists():
            existing.append(raw_path)
    return tuple(sorted(set(existing)))


def _expect_non_empty_string(
    issues: list[FoundationRoadmapIssue],
    mapping: Mapping[str, Any],
    key: str,
    *,
    prefix: str = "",
) -> None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        issues.append(FoundationRoadmapIssue("error", _join_path(prefix, key), f"{key} must be non-empty string"))


def _expect_string_in(
    issues: list[FoundationRoadmapIssue],
    mapping: Mapping[str, Any],
    key: str,
    allowed: set[str],
    *,
    prefix: str = "",
) -> None:
    value = mapping.get(key)
    if not isinstance(value, str) or value not in allowed:
        issues.append(
            FoundationRoadmapIssue(
                "error",
                _join_path(prefix, key),
                f"{key} must be one of {sorted(allowed)}",
            )
        )


def _expect_mapping(
    issues: list[FoundationRoadmapIssue],
    mapping: Mapping[str, Any],
    key: str,
    *,
    prefix: str = "",
) -> None:
    if not isinstance(mapping.get(key), Mapping):
        issues.append(FoundationRoadmapIssue("error", _join_path(prefix, key), f"{key} must be object"))


def _expect_string_list(
    issues: list[FoundationRoadmapIssue],
    mapping: Mapping[str, Any],
    key: str,
    *,
    prefix: str = "",
    allow_empty: bool = False,
) -> None:
    value = mapping.get(key)
    path = _join_path(prefix, key)

    if not isinstance(value, list):
        issues.append(FoundationRoadmapIssue("error", path, f"{key} must be list"))
        return

    if not value and not allow_empty:
        issues.append(FoundationRoadmapIssue("error", path, f"{key} must not be empty"))
        return

    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            issues.append(FoundationRoadmapIssue("error", f"{path}[{index}]", "list item must be non-empty string"))


def _join_path(prefix: str, key: str) -> str:
    if not prefix:
        return key
    return f"{prefix}.{key}"


def main() -> int:
    parser = argparse.ArgumentParser(description="MAKSIMAR foundation roadmap CI check.")
    parser.add_argument("--roadmap", default=str(DEFAULT_ROADMAP_PATH))
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA_PATH))
    parser.add_argument("--batch-id", default=None)
    parser.add_argument("--require-files", action="store_true")
    args = parser.parse_args()

    report = build_ci_report(
        roadmap_path=Path(args.roadmap),
        schema_path=Path(args.schema),
        batch_id=args.batch_id,
        require_files=args.require_files,
    )

    print("===== FOUNDATION ROADMAP CI CHECK =====")
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))

    return 0 if report.check_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
