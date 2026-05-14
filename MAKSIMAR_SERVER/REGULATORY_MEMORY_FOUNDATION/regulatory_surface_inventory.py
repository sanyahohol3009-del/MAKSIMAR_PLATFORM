from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_track_models import (
    build_regulatory_track_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RegulatorySurfaceKind = Literal[
    "closed_memory_roadmap",
    "regulatory_memory_models",
    "jurisdiction_models",
    "tenant_memory_models",
    "source_version_chain",
    "memory_policy",
    "memory_sync",
    "memory_routing",
    "roadmap_closure",
]


REQUIRED_REGULATORY_SURFACES: Tuple[str, ...] = (
    "docs/architecture/roadmap_index/memory_roadmap_v5_1_final_closure_v1.md",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/regulatory_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/legal_jurisdiction_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py",
    "MAKSIMAR_CORE_LIB/evidence_memory/source_version_chain_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_trust_scope_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_source_priority_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_federation_policy_models.py",
    "MAKSIMAR_SERVER/MEMORY_SYNC/node_memory_scope_models.py",
    "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py",
    "MAKSIMAR_SERVER/ROADMAP_CLOSURE/final_closure_preview_builder.py",
)


@dataclass(frozen=True, slots=True)
class RegulatorySurfaceInventory:
    inventory_id: str
    required_surfaces: Tuple[str, ...]
    missing_surfaces: Tuple[str, ...]
    total_required_surfaces: int
    closed_memory_roadmap_present: bool
    regulatory_models_present: bool
    jurisdiction_models_present: bool
    tenant_models_present: bool
    source_version_chain_present: bool
    memory_policy_present: bool
    routing_surfaces_present: bool
    surface_inventory_ready: bool

    def __post_init__(self) -> None:
        if not self.inventory_id:
            raise ValueError("inventory_id must be non-empty")
        if self.total_required_surfaces != len(self.required_surfaces):
            raise ValueError("total_required_surfaces mismatch")
        if self.missing_surfaces:
            raise ValueError(f"missing required regulatory surfaces: {self.missing_surfaces}")
        if self.closed_memory_roadmap_present is not True:
            raise ValueError("closed_memory_roadmap_present must be True")
        if self.regulatory_models_present is not True:
            raise ValueError("regulatory_models_present must be True")
        if self.jurisdiction_models_present is not True:
            raise ValueError("jurisdiction_models_present must be True")
        if self.tenant_models_present is not True:
            raise ValueError("tenant_models_present must be True")
        if self.source_version_chain_present is not True:
            raise ValueError("source_version_chain_present must be True")
        if self.memory_policy_present is not True:
            raise ValueError("memory_policy_present must be True")
        if self.routing_surfaces_present is not True:
            raise ValueError("routing_surfaces_present must be True")
        if self.surface_inventory_ready is not True:
            raise ValueError("surface_inventory_ready must be True")


def _exists(relative_path: str) -> bool:
    return (PROJECT_ROOT / relative_path).exists()


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not _exists(path))


def build_regulatory_surface_inventory() -> RegulatorySurfaceInventory:
    contract = build_regulatory_track_contract()
    missing = _missing(REQUIRED_REGULATORY_SURFACES)

    closed_memory_roadmap_present = _exists("docs/architecture/roadmap_index/memory_roadmap_v5_1_final_closure_v1.md")
    regulatory_models_present = _exists("MAKSIMAR_CORE_LIB/enterprise_memory_domains/regulatory_memory_models.py")
    jurisdiction_models_present = _exists("MAKSIMAR_CORE_LIB/enterprise_memory_domains/legal_jurisdiction_models.py")
    tenant_models_present = _exists("MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py")
    source_version_chain_present = _exists("MAKSIMAR_CORE_LIB/evidence_memory/source_version_chain_models.py")
    memory_policy_present = (
        _exists("MAKSIMAR_CORE_LIB/memory_policy/memory_trust_scope_models.py")
        and _exists("MAKSIMAR_CORE_LIB/memory_policy/memory_source_priority_models.py")
        and _exists("MAKSIMAR_CORE_LIB/memory_policy/memory_federation_policy_models.py")
    )
    routing_surfaces_present = (
        _exists("MAKSIMAR_SERVER/MEMORY_SYNC/node_memory_scope_models.py")
        and _exists("MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py")
    )

    return RegulatorySurfaceInventory(
        inventory_id="regulatory_surface_inventory_step_1_001",
        required_surfaces=REQUIRED_REGULATORY_SURFACES,
        missing_surfaces=missing,
        total_required_surfaces=len(REQUIRED_REGULATORY_SURFACES),
        closed_memory_roadmap_present=closed_memory_roadmap_present,
        regulatory_models_present=regulatory_models_present,
        jurisdiction_models_present=jurisdiction_models_present,
        tenant_models_present=tenant_models_present,
        source_version_chain_present=source_version_chain_present,
        memory_policy_present=memory_policy_present,
        routing_surfaces_present=routing_surfaces_present,
        surface_inventory_ready=contract.regulatory_track_ready and missing == (),
    )


def build_regulatory_surface_inventory_preview() -> Dict[str, object]:
    inventory = build_regulatory_surface_inventory()

    return {
        "preview_id": "regulatory_surface_inventory_preview_step_1_001",
        "preview_ready": inventory.surface_inventory_ready,
        "inventory_id": inventory.inventory_id,
        "required_surfaces": inventory.required_surfaces,
        "missing_surfaces": inventory.missing_surfaces,
        "total_required_surfaces": inventory.total_required_surfaces,
        "closed_memory_roadmap_present": inventory.closed_memory_roadmap_present,
        "regulatory_models_present": inventory.regulatory_models_present,
        "jurisdiction_models_present": inventory.jurisdiction_models_present,
        "tenant_models_present": inventory.tenant_models_present,
        "source_version_chain_present": inventory.source_version_chain_present,
        "memory_policy_present": inventory.memory_policy_present,
        "routing_surfaces_present": inventory.routing_surfaces_present,
    }
