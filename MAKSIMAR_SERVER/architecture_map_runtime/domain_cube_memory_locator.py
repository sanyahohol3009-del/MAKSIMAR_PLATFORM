from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


_CUBE_LOCATOR_ID_PATTERN = re.compile(r"^domain_cube_memory_locator_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class DomainCubeMemoryLocatorEntry:
    locator_id: str
    cube_slug: str
    cube_path: str
    memory_binding_ref: str
    architecture_binding_ref: str
    dashboard_visible: bool
    locator_ready: bool

    def __post_init__(self) -> None:
        locator_id = _ensure_non_empty_str(self.locator_id, "locator_id")
        cube_slug = _ensure_non_empty_str(self.cube_slug, "cube_slug")
        cube_path = _ensure_non_empty_str(self.cube_path, "cube_path")
        memory_binding_ref = _ensure_non_empty_str(
            self.memory_binding_ref,
            "memory_binding_ref",
        )
        architecture_binding_ref = _ensure_non_empty_str(
            self.architecture_binding_ref,
            "architecture_binding_ref",
        )

        if not _CUBE_LOCATOR_ID_PATTERN.fullmatch(locator_id):
            raise ValueError(f"Invalid locator_id: {locator_id}")

        _ensure_bool(self.dashboard_visible, "dashboard_visible")
        _ensure_bool(self.locator_ready, "locator_ready")

        if not self.dashboard_visible:
            raise ValueError("domain cube locator must be dashboard-visible")
        if not self.locator_ready:
            raise ValueError("domain cube locator must be ready")

        object.__setattr__(self, "locator_id", locator_id)
        object.__setattr__(self, "cube_slug", cube_slug)
        object.__setattr__(self, "cube_path", cube_path)
        object.__setattr__(self, "memory_binding_ref", memory_binding_ref)
        object.__setattr__(self, "architecture_binding_ref", architecture_binding_ref)


@dataclass(frozen=True, slots=True)
class DomainCubeMemoryLocatorContract:
    total_cubes: int
    ready_cubes: int
    dashboard_visible_cubes: int
    entries: tuple[DomainCubeMemoryLocatorEntry, ...]

    def __post_init__(self) -> None:
        if self.total_cubes != len(self.entries):
            raise ValueError("total_cubes must match entries length")
        if self.total_cubes <= 0:
            raise ValueError("total_cubes must be >= 1")
        if self.ready_cubes != sum(1 for entry in self.entries if entry.locator_ready):
            raise ValueError("ready_cubes must match computed count")
        if self.dashboard_visible_cubes != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_cubes must match computed count")

        if self.ready_cubes != self.total_cubes:
            raise ValueError("all domain cube locators must be ready")
        if self.dashboard_visible_cubes != self.total_cubes:
            raise ValueError("all domain cube locators must be dashboard-visible")

        locator_ids = tuple(entry.locator_id for entry in self.entries)
        if len(set(locator_ids)) != len(locator_ids):
            raise ValueError("duplicate locator_id values detected")


def _discover_domain_cube_slugs() -> tuple[str, ...]:
    root = Path("DOMAIN_CUBES")
    if not root.exists():
        return ("knowledge_assistant",)

    slugs = tuple(
        path.name
        for path in sorted(root.iterdir())
        if path.is_dir() and not path.name.startswith(".")
    )

    if not slugs:
        return ("knowledge_assistant",)

    return slugs


def _locator_suffix_from_slug(slug: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", slug.strip().lower()).strip("_")
    if not normalized:
        raise ValueError("cube slug must produce a non-empty locator suffix")
    if not normalized[0].isalpha():
        normalized = f"cube_{normalized}"
    return normalized


def build_domain_cube_memory_locator_contract() -> DomainCubeMemoryLocatorContract:
    entries = tuple(
        DomainCubeMemoryLocatorEntry(
            locator_id=f"domain_cube_memory_locator_{_locator_suffix_from_slug(slug)}",
            cube_slug=slug,
            cube_path=f"DOMAIN_CUBES/{slug}",
            memory_binding_ref="arch_memory_binding_memory_registry",
            architecture_binding_ref="MAKSIMAR_SERVER/architecture_map_runtime",
            dashboard_visible=True,
            locator_ready=True,
        )
        for slug in _discover_domain_cube_slugs()
    )

    return DomainCubeMemoryLocatorContract(
        total_cubes=len(entries),
        ready_cubes=sum(1 for entry in entries if entry.locator_ready),
        dashboard_visible_cubes=sum(1 for entry in entries if entry.dashboard_visible),
        entries=entries,
    )
