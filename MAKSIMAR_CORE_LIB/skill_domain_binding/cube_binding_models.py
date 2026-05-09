from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


_CUBE_BINDING_ID_PATTERN = re.compile(r"^cube_binding_[a-z][a-z0-9_]*$")


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


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


def _domain_class_from_cube_slug(cube_slug: str) -> str:
    if cube_slug in {"family_assistant", "mobile_assistant_cube", "desktop_assistant_cube"}:
        return "family_personal_assistant"
    if cube_slug in {"3d_cube", "visual_engineering_cube", "engineering_assistant"}:
        return "engineering_visual"
    if cube_slug in {"industrial_cube", "robotics_cube"}:
        return "industrial_robotics"
    if cube_slug in {"content_cube", "education_cube", "knowledge_assistant"}:
        return "knowledge_content"
    if cube_slug in {"energy_cube", "compute_fleet_cube"}:
        return "infrastructure_compute"
    if cube_slug in {"automation_cube", "module_templates", "vpn_cube"}:
        return "platform_extension"
    return "domain_extension"


@dataclass(frozen=True, slots=True)
class CubeBindingEntry:
    cube_binding_id: str
    cube_slug: str
    cube_path: str
    domain_class: str
    memory_binding_ref: str
    architecture_binding_ref: str
    dashboard_visible: bool
    locator_ready: bool
    cube_source_exists: bool
    skill_binding_present: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        cube_binding_id = _ensure_non_empty_str(
            self.cube_binding_id,
            "cube_binding_id",
        )
        cube_slug = _ensure_non_empty_str(self.cube_slug, "cube_slug")
        cube_path = _ensure_non_empty_str(self.cube_path, "cube_path")
        domain_class = _ensure_non_empty_str(self.domain_class, "domain_class")
        memory_binding_ref = _ensure_non_empty_str(
            self.memory_binding_ref,
            "memory_binding_ref",
        )
        architecture_binding_ref = _ensure_non_empty_str(
            self.architecture_binding_ref,
            "architecture_binding_ref",
        )
        description = _ensure_non_empty_str(self.description, "description")

        if not _CUBE_BINDING_ID_PATTERN.fullmatch(cube_binding_id):
            raise ValueError(f"Invalid cube_binding_id: {cube_binding_id}")
        if cube_slug.startswith("cube_"):
            raise ValueError("cube_slug must preserve canonical domain slug, not cube_* alias")

        for field_name in (
            "dashboard_visible",
            "locator_ready",
            "cube_source_exists",
            "skill_binding_present",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.locator_ready:
            raise ValueError("locator_ready must be True")
        if not self.cube_source_exists:
            raise ValueError("cube_source_exists must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "cube_binding_id", cube_binding_id)
        object.__setattr__(self, "cube_slug", cube_slug)
        object.__setattr__(self, "cube_path", cube_path)
        object.__setattr__(self, "domain_class", domain_class)
        object.__setattr__(self, "memory_binding_ref", memory_binding_ref)
        object.__setattr__(self, "architecture_binding_ref", architecture_binding_ref)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class CubeBindingContract:
    total_cubes: int
    ready_cubes: int
    dashboard_visible_cubes: int
    locator_ready_cubes: int
    source_exists_cubes: int
    skill_binding_present_cubes: int
    entries: tuple[CubeBindingEntry, ...]

    def __post_init__(self) -> None:
        total_cubes = _ensure_non_negative_int(self.total_cubes, "total_cubes")
        if total_cubes != len(self.entries):
            raise ValueError("total_cubes must match entries length")
        if total_cubes <= 0:
            raise ValueError("total_cubes must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_dashboard = sum(1 for entry in self.entries if entry.dashboard_visible)
        computed_locator = sum(1 for entry in self.entries if entry.locator_ready)
        computed_source = sum(1 for entry in self.entries if entry.cube_source_exists)
        computed_skill = sum(1 for entry in self.entries if entry.skill_binding_present)

        expected_counts = {
            "ready_cubes": computed_ready,
            "dashboard_visible_cubes": computed_dashboard,
            "locator_ready_cubes": computed_locator,
            "source_exists_cubes": computed_source,
            "skill_binding_present_cubes": computed_skill,
        }

        for field_name, expected_value in expected_counts.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_cubes != total_cubes:
            raise ValueError("all cube bindings must be ready")
        if self.dashboard_visible_cubes != total_cubes:
            raise ValueError("all cube bindings must be dashboard-visible")
        if self.locator_ready_cubes != total_cubes:
            raise ValueError("all cube bindings must be locator-ready")
        if self.source_exists_cubes != total_cubes:
            raise ValueError("all cube sources must exist")

        cube_slugs = tuple(entry.cube_slug for entry in self.entries)
        if len(set(cube_slugs)) != len(cube_slugs):
            raise ValueError("duplicate cube_slug values detected")

        binding_ids = tuple(entry.cube_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate cube_binding_id values detected")


def build_cube_binding_contract() -> CubeBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )
    from MAKSIMAR_SERVER.architecture_map_runtime import (
        build_domain_cube_memory_locator_contract,
    )

    locators = build_domain_cube_memory_locator_contract()
    skills = build_skill_binding_contract()

    skill_slugs = {entry.module_slug for entry in skills.entries}

    entries = tuple(
        CubeBindingEntry(
            cube_binding_id=f"cube_binding_{safe_id_suffix(locator.cube_slug)}",
            cube_slug=locator.cube_slug,
            cube_path=locator.cube_path,
            domain_class=_domain_class_from_cube_slug(locator.cube_slug),
            memory_binding_ref=locator.memory_binding_ref,
            architecture_binding_ref=locator.architecture_binding_ref,
            dashboard_visible=locator.dashboard_visible,
            locator_ready=locator.locator_ready,
            cube_source_exists=Path(locator.cube_path).exists(),
            skill_binding_present=locator.cube_slug in skill_slugs,
            binding_ready=(
                locator.dashboard_visible
                and locator.locator_ready
                and Path(locator.cube_path).exists()
            ),
            description=f"Domain cube binding for {locator.cube_slug}.",
        )
        for locator in locators.entries
    )

    return CubeBindingContract(
        total_cubes=len(entries),
        ready_cubes=sum(1 for entry in entries if entry.binding_ready),
        dashboard_visible_cubes=sum(1 for entry in entries if entry.dashboard_visible),
        locator_ready_cubes=sum(1 for entry in entries if entry.locator_ready),
        source_exists_cubes=sum(1 for entry in entries if entry.cube_source_exists),
        skill_binding_present_cubes=sum(
            1 for entry in entries if entry.skill_binding_present
        ),
        entries=entries,
    )
