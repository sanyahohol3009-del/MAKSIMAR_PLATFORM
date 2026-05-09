from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


DomainLayerKind = Literal[
    "skill_adapter_registry",
    "domain_cubes",
    "memory_registry",
    "retrieval_orchestration",
    "dashboard_read_only_views",
    "architecture_map_runtime",
]

_DOMAIN_LAYER_BINDING_ID_PATTERN = re.compile(r"^domain_layer_binding_[a-z][a-z0-9_]*$")


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


@dataclass(frozen=True, slots=True)
class DomainLayerBindingEntry:
    domain_layer_binding_id: str
    layer_kind: DomainLayerKind
    layer_name: str
    source_path: str
    visible_units: int
    source_exists: bool
    registry_backed: bool
    dashboard_visible: bool
    read_only: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        domain_layer_binding_id = _ensure_non_empty_str(
            self.domain_layer_binding_id,
            "domain_layer_binding_id",
        )
        layer_name = _ensure_non_empty_str(self.layer_name, "layer_name")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        description = _ensure_non_empty_str(self.description, "description")

        if not _DOMAIN_LAYER_BINDING_ID_PATTERN.fullmatch(domain_layer_binding_id):
            raise ValueError(
                f"Invalid domain_layer_binding_id: {domain_layer_binding_id}"
            )

        _ensure_non_negative_int(self.visible_units, "visible_units")

        for field_name in (
            "source_exists",
            "registry_backed",
            "dashboard_visible",
            "read_only",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.visible_units <= 0:
            raise ValueError("visible_units must be >= 1")
        if not self.source_exists:
            raise ValueError("source_exists must be True")
        if not self.registry_backed:
            raise ValueError("registry_backed must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "domain_layer_binding_id", domain_layer_binding_id)
        object.__setattr__(self, "layer_name", layer_name)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class DomainLayerBindingContract:
    total_layers: int
    ready_layers: int
    source_exists_layers: int
    registry_backed_layers: int
    dashboard_visible_layers: int
    read_only_layers: int
    entries: tuple[DomainLayerBindingEntry, ...]

    def __post_init__(self) -> None:
        total_layers = _ensure_non_negative_int(self.total_layers, "total_layers")
        if total_layers != len(self.entries):
            raise ValueError("total_layers must match entries length")
        if total_layers <= 0:
            raise ValueError("total_layers must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_source = sum(1 for entry in self.entries if entry.source_exists)
        computed_registry = sum(1 for entry in self.entries if entry.registry_backed)
        computed_dashboard = sum(1 for entry in self.entries if entry.dashboard_visible)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)

        expected_counts = {
            "ready_layers": computed_ready,
            "source_exists_layers": computed_source,
            "registry_backed_layers": computed_registry,
            "dashboard_visible_layers": computed_dashboard,
            "read_only_layers": computed_read_only,
        }

        for field_name, expected_value in expected_counts.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_layers != total_layers:
            raise ValueError("all domain layers must be ready")
        if self.source_exists_layers != total_layers:
            raise ValueError("all domain layer sources must exist")
        if self.registry_backed_layers != total_layers:
            raise ValueError("all domain layers must be registry-backed")
        if self.dashboard_visible_layers != total_layers:
            raise ValueError("all domain layers must be dashboard-visible")
        if self.read_only_layers != total_layers:
            raise ValueError("all domain layers must be read-only")

        binding_ids = tuple(entry.domain_layer_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate domain_layer_binding_id values detected")


def _entry(
    *,
    layer_kind: DomainLayerKind,
    layer_name: str,
    source_path: str,
    visible_units: int,
) -> DomainLayerBindingEntry:
    source_exists = Path(source_path).exists()

    return DomainLayerBindingEntry(
        domain_layer_binding_id=f"domain_layer_binding_{safe_id_suffix(layer_kind)}",
        layer_kind=layer_kind,
        layer_name=layer_name,
        source_path=source_path,
        visible_units=visible_units,
        source_exists=source_exists,
        registry_backed=True,
        dashboard_visible=True,
        read_only=True,
        binding_ready=source_exists and visible_units > 0,
        description=f"Read-only domain layer binding for {layer_name}.",
    )


def build_domain_layer_binding_contract() -> DomainLayerBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.cube_binding_models import (
        build_cube_binding_contract,
    )
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )
    from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
        build_retrieval_phase_readiness,
    )
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
        build_dashboard_read_only_views_contract,
    )
    from MAKSIMAR_SERVER.MEMORY_REGISTRY import build_memory_registry_contract
    from MAKSIMAR_SERVER.architecture_map_runtime import build_memory_dependency_summary

    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()
    memory_registry = build_memory_registry_contract()
    retrieval = build_retrieval_phase_readiness()
    dashboard = build_dashboard_read_only_views_contract()
    architecture = build_memory_dependency_summary()

    entries = (
        _entry(
            layer_kind="skill_adapter_registry",
            layer_name="Skill Adapter Registry",
            source_path="MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY",
            visible_units=skills.ready_bindings,
        ),
        _entry(
            layer_kind="domain_cubes",
            layer_name="Domain Cubes",
            source_path="DOMAIN_CUBES",
            visible_units=cubes.ready_cubes,
        ),
        _entry(
            layer_kind="memory_registry",
            layer_name="Memory Registry",
            source_path="MAKSIMAR_SERVER/MEMORY_REGISTRY",
            visible_units=memory_registry.active_entries,
        ),
        _entry(
            layer_kind="retrieval_orchestration",
            layer_name="Retrieval Orchestration",
            source_path="MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",
            visible_units=retrieval.selected_source_count,
        ),
        _entry(
            layer_kind="dashboard_read_only_views",
            layer_name="Dashboard Read-Only Views",
            source_path="MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS",
            visible_units=dashboard.active_entries,
        ),
        _entry(
            layer_kind="architecture_map_runtime",
            layer_name="Architecture Map Runtime",
            source_path="MAKSIMAR_SERVER/architecture_map_runtime",
            visible_units=int(architecture["architecture_module_views"]),
        ),
    )

    return DomainLayerBindingContract(
        total_layers=len(entries),
        ready_layers=sum(1 for entry in entries if entry.binding_ready),
        source_exists_layers=sum(1 for entry in entries if entry.source_exists),
        registry_backed_layers=sum(1 for entry in entries if entry.registry_backed),
        dashboard_visible_layers=sum(1 for entry in entries if entry.dashboard_visible),
        read_only_layers=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
