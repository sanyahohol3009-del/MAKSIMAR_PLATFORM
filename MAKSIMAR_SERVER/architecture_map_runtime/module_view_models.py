from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.architecture_map.module_identity_models import (
    CanonicalModuleId,
)


@dataclass(frozen=True, slots=True)
class ServerModuleViewEntry:
    """Server-side read-only module view entry."""

    module_id: CanonicalModuleId
    layer_name: str
    criticality: str
    dashboard_visible: bool
    source_contract_bound: bool


@dataclass(frozen=True, slots=True)
class ServerModuleViewContract:
    """Unified server-side module view contract."""

    total_modules: int
    modules: tuple[ServerModuleViewEntry, ...]
