from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.jurisdiction_registry_models import (
    build_jurisdiction_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_track_preview_builder import (
    build_regulatory_track_entry_preview,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_JURISDICTION_BINDING_SURFACES: Tuple[str, ...] = (
    "docs/architecture/foundation/regulatory_track_entry_surface_inventory_v1.md",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/legal_jurisdiction_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/regulatory_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_trust_scope_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_source_priority_models.py",
    "MAKSIMAR_CORE_LIB/evidence_memory/source_version_chain_models.py",
)


@dataclass(frozen=True, slots=True)
class CountryJurisdictionBinding:
    binding_id: str
    country_codes: Tuple[str, ...]
    jurisdiction_ids: Tuple[str, ...]
    required_surfaces: Tuple[str, ...]
    missing_surfaces: Tuple[str, ...]
    step_1_ready: bool
    registry_ready: bool
    country_jurisdiction_binding_ready: bool
    no_cross_jurisdiction_merge: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.binding_id:
            raise ValueError("binding_id must be non-empty")
        if not self.country_codes:
            raise ValueError("country_codes must be non-empty")
        if not self.jurisdiction_ids:
            raise ValueError("jurisdiction_ids must be non-empty")
        if self.missing_surfaces:
            raise ValueError(f"missing required jurisdiction binding surfaces: {self.missing_surfaces}")
        if self.step_1_ready is not True:
            raise ValueError("step_1_ready must be True")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")
        if self.country_jurisdiction_binding_ready is not True:
            raise ValueError("country_jurisdiction_binding_ready must be True")
        if self.no_cross_jurisdiction_merge is not True:
            raise ValueError("no_cross_jurisdiction_merge must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_country_jurisdiction_binding() -> CountryJurisdictionBinding:
    step_1 = build_regulatory_track_entry_preview()
    registry = build_jurisdiction_registry()
    missing = _missing(REQUIRED_JURISDICTION_BINDING_SURFACES)

    return CountryJurisdictionBinding(
        binding_id="country_jurisdiction_binding_step_2_001",
        country_codes=tuple(sorted({entry.country_code for entry in registry.entries})),
        jurisdiction_ids=tuple(entry.jurisdiction_id for entry in registry.entries),
        required_surfaces=REQUIRED_JURISDICTION_BINDING_SURFACES,
        missing_surfaces=missing,
        step_1_ready=step_1["preview_ready"],
        registry_ready=registry.registry_ready,
        country_jurisdiction_binding_ready=step_1["preview_ready"] is True and registry.registry_ready and missing == (),
        no_cross_jurisdiction_merge=registry.cross_jurisdiction_merge_allowed is False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
    )


def build_country_jurisdiction_binding_preview() -> Dict[str, object]:
    binding = build_country_jurisdiction_binding()

    return {
        "preview_id": "country_jurisdiction_binding_preview_step_2_001",
        "preview_ready": binding.country_jurisdiction_binding_ready,
        "binding_id": binding.binding_id,
        "country_codes": binding.country_codes,
        "jurisdiction_ids": binding.jurisdiction_ids,
        "required_surfaces": binding.required_surfaces,
        "missing_surfaces": binding.missing_surfaces,
        "step_1_ready": binding.step_1_ready,
        "registry_ready": binding.registry_ready,
        "no_cross_jurisdiction_merge": binding.no_cross_jurisdiction_merge,
        "runtime_mutation_allowed": binding.runtime_mutation_allowed,
        "direct_core_write_allowed": binding.direct_core_write_allowed,
        "deployment_allowed_now": binding.deployment_allowed_now,
    }
