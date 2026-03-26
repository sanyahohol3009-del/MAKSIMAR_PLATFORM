from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.architecture_map.module_identity_models import (
    CanonicalModuleId,
)


@dataclass(frozen=True, slots=True)
class ServerDependencyViewEntry:
    """Server-side read-only dependency view entry."""

    upstream_module_id: CanonicalModuleId
    downstream_module_id: CanonicalModuleId
    critical_path: bool
    source_contract_bound: bool


@dataclass(frozen=True, slots=True)
class ServerDependencyViewContract:
    """Unified server-side dependency view contract."""

    total_edges: int
    edges: tuple[ServerDependencyViewEntry, ...]
