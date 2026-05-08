from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


ExistingDomainKind = Literal[
    "domain_cube",
    "platform_layer",
    "workflow_engine",
    "action_library",
    "shell_adapter",
    "server_registry",
]

_DOMAIN_SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_STORAGE_NODE_ID_PATTERN = re.compile(r"^storage_node_[a-z][a-z0-9_]*$")
_RETRIEVAL_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")
_OBSERVABILITY_ID_PATTERN = re.compile(r"^observability_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _normalize_slug(raw: str) -> str:
    normalized = re.sub(r"[^a-z0-9_]+", "_", raw.lower()).strip("_")
    if not normalized:
        normalized = "domain"
    if not normalized[0].isalpha():
        normalized = f"domain_{normalized}"
    return normalized


@dataclass(frozen=True, slots=True)
class ExistingDomainInventoryEntry:
    """Read-only inventory entry for an existing project domain."""

    domain_slug: str
    source_path: str
    domain_kind: ExistingDomainKind
    storage_node_id: str
    retrieval_source_id: str
    dashboard_exposure_id: str
    observability_binding_id: str
    discovered: bool

    def __post_init__(self) -> None:
        domain_slug = _ensure_non_empty_str(self.domain_slug, "domain_slug")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        storage_node_id = _ensure_non_empty_str(self.storage_node_id, "storage_node_id")
        retrieval_source_id = _ensure_non_empty_str(
            self.retrieval_source_id,
            "retrieval_source_id",
        )
        dashboard_exposure_id = _ensure_non_empty_str(
            self.dashboard_exposure_id,
            "dashboard_exposure_id",
        )
        observability_binding_id = _ensure_non_empty_str(
            self.observability_binding_id,
            "observability_binding_id",
        )

        if not _DOMAIN_SLUG_PATTERN.fullmatch(domain_slug):
            raise ValueError(f"Invalid domain_slug: {domain_slug}")
        if not _STORAGE_NODE_ID_PATTERN.fullmatch(storage_node_id):
            raise ValueError(f"Invalid storage_node_id: {storage_node_id}")
        if not _RETRIEVAL_SOURCE_ID_PATTERN.fullmatch(retrieval_source_id):
            raise ValueError(f"Invalid retrieval_source_id: {retrieval_source_id}")
        if not _PANEL_ID_PATTERN.fullmatch(dashboard_exposure_id):
            raise ValueError(f"Invalid dashboard_exposure_id: {dashboard_exposure_id}")
        if not _OBSERVABILITY_ID_PATTERN.fullmatch(observability_binding_id):
            raise ValueError(
                f"Invalid observability_binding_id: {observability_binding_id}"
            )
        if not isinstance(self.discovered, bool):
            raise ValueError("discovered must be bool")

        object.__setattr__(self, "domain_slug", domain_slug)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "storage_node_id", storage_node_id)
        object.__setattr__(self, "retrieval_source_id", retrieval_source_id)
        object.__setattr__(self, "dashboard_exposure_id", dashboard_exposure_id)
        object.__setattr__(self, "observability_binding_id", observability_binding_id)


@dataclass(frozen=True, slots=True)
class ExistingDomainInventoryContract:
    """Read-only inventory contract for existing project domains."""

    total_entries: int
    domain_cube_entries: int
    platform_layer_entries: int
    shell_adapter_entries: int
    server_registry_entries: int
    entries: tuple[ExistingDomainInventoryEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        domain_cube_entries = _ensure_non_negative_int(
            self.domain_cube_entries,
            "domain_cube_entries",
        )
        platform_layer_entries = _ensure_non_negative_int(
            self.platform_layer_entries,
            "platform_layer_entries",
        )
        shell_adapter_entries = _ensure_non_negative_int(
            self.shell_adapter_entries,
            "shell_adapter_entries",
        )
        server_registry_entries = _ensure_non_negative_int(
            self.server_registry_entries,
            "server_registry_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        if domain_cube_entries != sum(
            1 for entry in self.entries if entry.domain_kind == "domain_cube"
        ):
            raise ValueError("domain_cube_entries must match computed count")

        if platform_layer_entries != sum(
            1 for entry in self.entries if entry.domain_kind == "platform_layer"
        ):
            raise ValueError("platform_layer_entries must match computed count")

        if shell_adapter_entries != sum(
            1 for entry in self.entries if entry.domain_kind == "shell_adapter"
        ):
            raise ValueError("shell_adapter_entries must match computed count")

        if server_registry_entries != sum(
            1 for entry in self.entries if entry.domain_kind == "server_registry"
        ):
            raise ValueError("server_registry_entries must match computed count")

        source_paths = tuple(entry.source_path for entry in self.entries)
        domain_slugs = tuple(entry.domain_slug for entry in self.entries)

        if len(set(source_paths)) != len(source_paths):
            raise ValueError("Duplicate source_path values detected")
        if len(set(domain_slugs)) != len(domain_slugs):
            raise ValueError("Duplicate domain_slug values detected")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "domain_cube_entries", domain_cube_entries)
        object.__setattr__(self, "platform_layer_entries", platform_layer_entries)
        object.__setattr__(self, "shell_adapter_entries", shell_adapter_entries)
        object.__setattr__(self, "server_registry_entries", server_registry_entries)


def _candidate_paths(project_root: Path) -> tuple[tuple[Path, ExistingDomainKind], ...]:
    candidates: list[tuple[Path, ExistingDomainKind]] = []

    domain_cubes = project_root / "DOMAIN_CUBES"
    if domain_cubes.is_dir():
        for child in sorted(domain_cubes.iterdir()):
            if child.is_dir():
                candidates.append((child, "domain_cube"))

    for child in sorted(project_root.iterdir()):
        if child.is_dir() and child.name.endswith("_LAYER"):
            candidates.append((child, "platform_layer"))

    for name, kind in (
        ("WORKFLOW_ENGINE", "workflow_engine"),
        ("ACTION_LIBRARY", "action_library"),
    ):
        path = project_root / name
        if path.is_dir():
            candidates.append((path, kind))  # type: ignore[arg-type]

    for relative in (
        "ANDROID_SHELL/memory_adapter",
        "ANDROID_SHELL/knowledge_adapter",
        "IOS_SHELL/memory_adapter",
        "IOS_SHELL/knowledge_adapter",
    ):
        path = project_root / relative
        if path.is_dir():
            candidates.append((path, "shell_adapter"))

    for relative in (
        "MAKSIMAR_SERVER/MEMORY_REGISTRY",
        "MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY",
        "MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT",
        "MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics",
    ):
        path = project_root / relative
        if path.is_dir():
            candidates.append((path, "server_registry"))

    return tuple(candidates)


def build_existing_domain_inventory(
    project_root: Path | None = None,
) -> ExistingDomainInventoryContract:
    """Build read-only inventory for existing project domains.

    This function does not write manifests and does not mutate registry state.
    """
    root = project_root or Path.cwd()
    entries: list[ExistingDomainInventoryEntry] = []
    seen_paths: set[str] = set()

    for path, domain_kind in _candidate_paths(root):
        relative_path = path.relative_to(root).as_posix()
        if relative_path in seen_paths:
            continue
        seen_paths.add(relative_path)

        slug = _normalize_slug(relative_path.replace("/", "_"))
        entries.append(
            ExistingDomainInventoryEntry(
                domain_slug=slug,
                source_path=relative_path,
                domain_kind=domain_kind,
                storage_node_id=f"storage_node_{slug}",
                retrieval_source_id=f"retrieval_source_{slug}",
                dashboard_exposure_id=f"panel_{slug}",
                observability_binding_id=f"observability_{slug}",
                discovered=True,
            )
        )

    ordered_entries = tuple(sorted(entries, key=lambda entry: entry.source_path))

    return ExistingDomainInventoryContract(
        total_entries=len(ordered_entries),
        domain_cube_entries=sum(
            1 for entry in ordered_entries if entry.domain_kind == "domain_cube"
        ),
        platform_layer_entries=sum(
            1 for entry in ordered_entries if entry.domain_kind == "platform_layer"
        ),
        shell_adapter_entries=sum(
            1 for entry in ordered_entries if entry.domain_kind == "shell_adapter"
        ),
        server_registry_entries=sum(
            1 for entry in ordered_entries if entry.domain_kind == "server_registry"
        ),
        entries=ordered_entries,
    )
