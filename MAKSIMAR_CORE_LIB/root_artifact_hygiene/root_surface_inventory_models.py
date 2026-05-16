from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping


DEFAULT_ROOT_SURFACE_SCAN_MAX_DEPTH = 2

ROOT_ARTIFACT_HYGIENE_LAYER_ID = "ROOT_ARTIFACT_HYGIENE"
ROOT_ARTIFACT_HYGIENE_BATCH_ID = "PHASE_0_BATCH_0_1"


class RootSurfacePathType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class RootArtifactCandidateKind(str, Enum):
    SOURCE_CANDIDATE = "source_candidate"
    GENERATED_CANDIDATE = "generated_candidate"
    BACKUP_CANDIDATE = "backup_candidate"
    AUDIT_CANDIDATE = "audit_candidate"
    VENDOR_CANDIDATE = "vendor_candidate"
    UNKNOWN_CANDIDATE = "unknown_candidate"


SOURCE_TOP_LEVEL_NAMES: frozenset[str] = frozenset(
    {
        "ACTION_LIBRARY",
        "AI_SERVICES",
        "ANDROID_SHELL",
        "BOOT",
        "CAD_3D_CAM_LAYER",
        "CODEGEN_LAYER",
        "COMPUTE_FLEET_LAYER",
        "CONTENT_MEDIA_LAYER",
        "CONTRACTS",
        "CONTROL_PLANE",
        "CORE_ROOT",
        "DESKTOP_SHELL",
        "DIALOGUE_LAYER",
        "DOMAIN_CUBES",
        "ENERGY_OPERATIONS_LAYER",
        "EVALUATION_LAYER",
        "EVENT_BUS",
        "INDUSTRIAL_LAYER",
        "IOS_SHELL",
        "KNOWLEDGE_SYSTEM",
        "MAKSIMAR_CORE",
        "MAKSIMAR_CORE_LIB",
        "MAKSIMAR_SERVER",
        "MEMORY_SYSTEM",
        "MODULE_SYSTEM",
        "OBSERVABILITY_LAYER",
        "OOB_MONITORING",
        "PACKAGING",
        "PRODUCTS",
        "RESEARCH_LAYER",
        "ROBOTICS_LAYER",
        "RUNTIME",
        "SAFETY_FOUNDATION",
        "SANDBOX",
        "SANDBOX_EXECUTION",
        "SERVER_SHELL",
        "SHARED",
        "SHELL_LAYER",
        "SIMULATION_LAYER",
        "SUPERVISOR",
        "UI_LAYER",
        "VISUAL_ENGINEERING_LAYER",
        "VOICE_LAYER",
        "VPN_LAYER",
        "WORKFLOW_ENGINE",
        "assets",
        "docs",
        "frontend",
        "logs",
        "requirements",
        "runtime_history_store",
        "runtime_imports",
        "scripts",
        "tests",
        "tools",
    }
)

SOURCE_ROOT_FILES: frozenset[str] = frozenset(
    {
        "README.md",
        "Makefile",
        "pytest.ini",
        "start_maksimar.sh",
        "run_context.py",
        "refactor.py",
        "conftest.py",
        "STRUCTURE.md",
        "MAKSIMAR_ENGINE.txt",
        "MAKSIMAR_FULL_SNAPSHOT.txt",
        "MAKSIMAR_INDEX.txt",
        "MAKSIMAR_MAP.txt",
        "FOUNDATION_COMPONENT_CLASSIFICATION_v1.md",
        "FOUNDATION_INTEGRATION_CONTRACT_v1.md",
        "FOUNDATION_STARTUP_CONTRACT_v1.md",
        "DASHBOARD_TRUTH_CONTRACT_v1.md",
        "STATUS_SURFACE_CONTRACT_v1.md",
    }
)

GENERATED_TOP_LEVEL_NAMES: frozenset[str] = frozenset(
    {
        ".pytest_cache",
        "_dashboard_audit_pack",
        "_display_restore_audit",
        "_frontend_graveyard",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "project_audit",
    }
)

PRUNE_DESCENDANT_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "venv",
    }
)

BACKUP_MARKERS: tuple[str, ...] = (
    ".bak",
    ".bak_",
    ".backup",
    "_backup",
    "~",
)

AUDIT_REPORT_MARKERS: tuple[str, ...] = (
    "audit_",
    "_audit",
    "_coverage",
    "coverage_",
    "_pytest",
    "pytest_",
    "_report",
    "report_",
    "history_track_",
    "phase1_",
    "phase2_",
    "visual_",
    "dashboard_audit_",
    "display_restore_",
)


@dataclass(frozen=True, slots=True)
class RootSurfaceInventoryEntry:
    relative_path: str
    path_type: RootSurfacePathType
    candidate_kind: RootArtifactCandidateKind
    reason_codes: tuple[str, ...] = field(default_factory=tuple)
    size_bytes: int | None = None
    exists: bool = True

    def __post_init__(self) -> None:
        if not self.relative_path:
            raise ValueError("relative_path must not be empty")

        if self.relative_path.startswith("/"):
            raise ValueError("relative_path must be project-relative, not absolute")

        if "\\" in self.relative_path:
            raise ValueError("relative_path must use POSIX-style '/' separators")

        if ".." in Path(self.relative_path).parts:
            raise ValueError("relative_path must not contain '..'")

        if not isinstance(self.path_type, RootSurfacePathType):
            raise TypeError("path_type must be RootSurfacePathType")

        if not isinstance(self.candidate_kind, RootArtifactCandidateKind):
            raise TypeError("candidate_kind must be RootArtifactCandidateKind")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative when provided")

    @property
    def dashboard_safe(self) -> bool:
        return True

    @property
    def delete_allowed(self) -> bool:
        return False

    @property
    def move_allowed(self) -> bool:
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "path_type": self.path_type.value,
            "candidate_kind": self.candidate_kind.value,
            "reason_codes": list(self.reason_codes),
            "size_bytes": self.size_bytes,
            "exists": self.exists,
            "dashboard_safe": self.dashboard_safe,
            "delete_allowed": self.delete_allowed,
            "move_allowed": self.move_allowed,
        }


@dataclass(frozen=True, slots=True)
class RootSurfaceInventoryReadModel:
    scanned_root: str
    entries: tuple[RootSurfaceInventoryEntry, ...]
    layer_id: str = ROOT_ARTIFACT_HYGIENE_LAYER_ID
    batch_id: str = ROOT_ARTIFACT_HYGIENE_BATCH_ID
    status: str = "ready"
    readiness: float = 1.0
    scan_readonly: bool = True
    delete_allowed: bool = False
    move_allowed: bool = False
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)
    next_action: str = "proceed_to_artifact_classification"

    def __post_init__(self) -> None:
        if not self.scanned_root:
            raise ValueError("scanned_root must not be empty")

        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be a tuple")

        for entry in self.entries:
            if not isinstance(entry, RootSurfaceInventoryEntry):
                raise TypeError("entries must contain RootSurfaceInventoryEntry instances")

        if not 0.0 <= self.readiness <= 1.0:
            raise ValueError("readiness must be between 0.0 and 1.0")

        if self.layer_id != ROOT_ARTIFACT_HYGIENE_LAYER_ID:
            raise ValueError(f"layer_id must be {ROOT_ARTIFACT_HYGIENE_LAYER_ID}")

        if self.batch_id != ROOT_ARTIFACT_HYGIENE_BATCH_ID:
            raise ValueError(f"batch_id must be {ROOT_ARTIFACT_HYGIENE_BATCH_ID}")

        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")

        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false in BATCH 0.1")

        if self.move_allowed:
            raise ValueError("move_allowed must remain false in BATCH 0.1")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    @property
    def total_root_files(self) -> int:
        return sum(1 for entry in self.entries if entry.path_type is RootSurfacePathType.FILE)

    @property
    def total_root_dirs(self) -> int:
        return sum(1 for entry in self.entries if entry.path_type is RootSurfacePathType.DIRECTORY)

    @property
    def source_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.SOURCE_CANDIDATE)

    @property
    def generated_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.GENERATED_CANDIDATE)

    @property
    def backup_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.BACKUP_CANDIDATE)

    @property
    def audit_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.AUDIT_CANDIDATE)

    @property
    def vendor_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.VENDOR_CANDIDATE)

    @property
    def unknown_candidates(self) -> int:
        return self.count_by_kind(RootArtifactCandidateKind.UNKNOWN_CANDIDATE)

    @property
    def total_entries(self) -> int:
        return len(self.entries)

    def count_by_kind(self, candidate_kind: RootArtifactCandidateKind) -> int:
        return sum(1 for entry in self.entries if entry.candidate_kind is candidate_kind)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "readiness": self.readiness,
            "scanned_root": self.scanned_root,
            "total_entries": self.total_entries,
            "total_root_files": self.total_root_files,
            "total_root_dirs": self.total_root_dirs,
            "source_candidates": self.source_candidates,
            "generated_candidates": self.generated_candidates,
            "backup_candidates": self.backup_candidates,
            "audit_candidates": self.audit_candidates,
            "vendor_candidates": self.vendor_candidates,
            "unknown_candidates": self.unknown_candidates,
            "scan_readonly": self.scan_readonly,
            "delete_allowed": self.delete_allowed,
            "move_allowed": self.move_allowed,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "warnings": list(self.warnings),
            "next_action": self.next_action,
            "entries": [entry.to_dict() for entry in self.entries],
        }

    @classmethod
    def from_entries(
        cls,
        *,
        scanned_root: str,
        entries: Iterable[RootSurfaceInventoryEntry],
    ) -> RootSurfaceInventoryReadModel:
        entry_tuple = tuple(entries)

        warnings: list[str] = []
        unknown_count = sum(
            1
            for entry in entry_tuple
            if entry.candidate_kind is RootArtifactCandidateKind.UNKNOWN_CANDIDATE
        )
        backup_count = sum(
            1
            for entry in entry_tuple
            if entry.candidate_kind is RootArtifactCandidateKind.BACKUP_CANDIDATE
        )
        audit_count = sum(
            1
            for entry in entry_tuple
            if entry.candidate_kind is RootArtifactCandidateKind.AUDIT_CANDIDATE
        )

        if unknown_count:
            warnings.append("unknown_candidates_present")
        if backup_count:
            warnings.append("backup_candidates_present")
        if audit_count:
            warnings.append("audit_candidates_present")

        next_action = (
            "review_unknown_candidates_before_classification"
            if unknown_count
            else "proceed_to_artifact_classification"
        )

        return cls(
            scanned_root=scanned_root,
            entries=entry_tuple,
            warnings=tuple(warnings),
            next_action=next_action,
        )


def classify_root_surface_path(
    relative_path: str | Path,
    *,
    is_dir: bool,
    size_bytes: int | None = None,
) -> RootSurfaceInventoryEntry:
    normalized = _normalize_relative_path(relative_path)
    path = Path(normalized)
    parts = path.parts

    if not parts:
        raise ValueError("relative_path must not resolve to project root itself")

    top_level = parts[0]
    lower_name = path.name.lower()
    lower_path = normalized.lower()

    path_type = RootSurfacePathType.DIRECTORY if is_dir else RootSurfacePathType.FILE

    candidate_kind: RootArtifactCandidateKind
    reason_codes: list[str] = []

    if top_level == "EXTERNAL_BACKENDS":
        candidate_kind = RootArtifactCandidateKind.VENDOR_CANDIDATE
        reason_codes.append("under_external_backends")
    elif top_level in GENERATED_TOP_LEVEL_NAMES:
        candidate_kind = RootArtifactCandidateKind.GENERATED_CANDIDATE
        reason_codes.append("generated_or_runtime_artifact_root")
    elif _contains_pruned_or_cache_part(parts):
        candidate_kind = RootArtifactCandidateKind.GENERATED_CANDIDATE
        reason_codes.append("cache_or_generated_path")
    elif _looks_like_backup(lower_path):
        candidate_kind = RootArtifactCandidateKind.BACKUP_CANDIDATE
        reason_codes.append("backup_filename_marker")
    elif _looks_like_audit_or_report(lower_path):
        candidate_kind = RootArtifactCandidateKind.AUDIT_CANDIDATE
        reason_codes.append("audit_report_or_coverage_marker")
    elif top_level in SOURCE_TOP_LEVEL_NAMES:
        candidate_kind = RootArtifactCandidateKind.SOURCE_CANDIDATE
        reason_codes.append("known_source_root")
    elif normalized in SOURCE_ROOT_FILES or lower_name in {item.lower() for item in SOURCE_ROOT_FILES}:
        candidate_kind = RootArtifactCandidateKind.SOURCE_CANDIDATE
        reason_codes.append("known_source_root_file")
    else:
        candidate_kind = RootArtifactCandidateKind.UNKNOWN_CANDIDATE
        reason_codes.append("unknown_root_surface_path")

    return RootSurfaceInventoryEntry(
        relative_path=normalized,
        path_type=path_type,
        candidate_kind=candidate_kind,
        reason_codes=tuple(reason_codes),
        size_bytes=size_bytes,
    )


def build_root_surface_inventory(
    project_root: str | Path,
    *,
    max_depth: int = DEFAULT_ROOT_SURFACE_SCAN_MAX_DEPTH,
) -> RootSurfaceInventoryReadModel:
    root = Path(project_root).resolve()

    if not root.exists():
        raise FileNotFoundError(f"project_root does not exist: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"project_root must be a directory: {root}")

    if max_depth < 1:
        raise ValueError("max_depth must be >= 1")

    entries: list[RootSurfaceInventoryEntry] = []

    for path in _iter_surface_paths(root=root, max_depth=max_depth):
        relative_path = path.relative_to(root).as_posix()
        size_bytes = _safe_file_size(path)

        entries.append(
            classify_root_surface_path(
                relative_path,
                is_dir=path.is_dir(),
                size_bytes=size_bytes,
            )
        )

    return RootSurfaceInventoryReadModel.from_entries(
        scanned_root=str(root),
        entries=entries,
    )


def _iter_surface_paths(*, root: Path, max_depth: int) -> Iterable[Path]:
    def walk(current: Path, depth: int) -> Iterable[Path]:
        if depth > max_depth:
            return

        try:
            children = sorted(current.iterdir(), key=lambda item: item.name)
        except PermissionError:
            return

        for child in children:
            yield child

            if not child.is_dir():
                continue

            if child.name in PRUNE_DESCENDANT_NAMES:
                continue

            if depth < max_depth:
                yield from walk(child, depth + 1)

    yield from walk(root, 1)


def _safe_file_size(path: Path) -> int | None:
    if path.is_dir():
        return None

    try:
        return path.stat().st_size
    except OSError:
        return None


def _normalize_relative_path(relative_path: str | Path) -> str:
    path = Path(relative_path)

    if path.is_absolute():
        raise ValueError("relative_path must not be absolute")

    normalized = path.as_posix().strip()

    if not normalized or normalized == ".":
        raise ValueError("relative_path must not be empty")

    normalized_parts = Path(normalized).parts

    if ".." in normalized_parts:
        raise ValueError("relative_path must not contain '..'")

    return normalized


def _contains_pruned_or_cache_part(parts: tuple[str, ...]) -> bool:
    return any(part in PRUNE_DESCENDANT_NAMES for part in parts)


def _looks_like_backup(lower_path: str) -> bool:
    return any(marker in lower_path for marker in BACKUP_MARKERS)


def _looks_like_audit_or_report(lower_path: str) -> bool:
    name = Path(lower_path).name

    return (
        any(marker in lower_path for marker in AUDIT_REPORT_MARKERS)
        or name.endswith("_report.txt")
        or name.endswith("_coverage.txt")
        or name.endswith("_pytest_run.txt")
        or name.endswith(".tar.gz")
    )


def read_model_from_mapping(payload: Mapping[str, Any]) -> RootSurfaceInventoryReadModel:
    entries_payload = payload.get("entries", [])

    if not isinstance(entries_payload, list):
        raise TypeError("payload['entries'] must be a list")

    entries: list[RootSurfaceInventoryEntry] = []

    for entry_payload in entries_payload:
        if not isinstance(entry_payload, Mapping):
            raise TypeError("entry payload must be a mapping")

        entries.append(
            RootSurfaceInventoryEntry(
                relative_path=str(entry_payload["relative_path"]),
                path_type=RootSurfacePathType(str(entry_payload["path_type"])),
                candidate_kind=RootArtifactCandidateKind(str(entry_payload["candidate_kind"])),
                reason_codes=tuple(str(item) for item in entry_payload.get("reason_codes", [])),
                size_bytes=entry_payload.get("size_bytes"),
                exists=bool(entry_payload.get("exists", True)),
            )
        )

    return RootSurfaceInventoryReadModel(
        scanned_root=str(payload["scanned_root"]),
        entries=tuple(entries),
        status=str(payload.get("status", "ready")),
        readiness=float(payload.get("readiness", 1.0)),
        scan_readonly=bool(payload.get("scan_readonly", True)),
        delete_allowed=bool(payload.get("delete_allowed", False)),
        move_allowed=bool(payload.get("move_allowed", False)),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
        runtime_mutation_allowed=bool(payload.get("runtime_mutation_allowed", False)),
        canonical_write_allowed=bool(payload.get("canonical_write_allowed", False)),
        warnings=tuple(str(item) for item in payload.get("warnings", [])),
        next_action=str(payload.get("next_action", "proceed_to_artifact_classification")),
    )
