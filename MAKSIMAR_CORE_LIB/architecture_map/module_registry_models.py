from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.architecture_map.module_identity_models import (
    CanonicalModuleId,
)


@dataclass(frozen=True, slots=True)
class ModuleRegistryEntry:
    """Canonical module registry entry for project architecture map."""

    module_id: CanonicalModuleId
    layer_name: str
    criticality: str
    read_only_view_available: bool


@dataclass(frozen=True, slots=True)
class ModuleRegistryContract:
    """Unified module registry contract."""

    total_modules: int
    modules: tuple[ModuleRegistryEntry, ...]
