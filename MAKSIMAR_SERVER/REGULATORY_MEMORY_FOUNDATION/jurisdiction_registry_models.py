from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


CountryCode = Literal["DE", "EU", "UA", "US", "GLOBAL"]
JurisdictionLevel = Literal["country", "union", "federal", "state", "regional", "municipal", "global"]
ApplicabilityScope = Literal[
    "tenant_policy",
    "regulatory_memory",
    "compliance_memory",
    "enterprise_policy_memory",
    "source_evidence_memory",
]


@dataclass(frozen=True, slots=True)
class JurisdictionRegistryEntry:
    jurisdiction_id: str
    country_code: CountryCode
    jurisdiction_level: JurisdictionLevel
    display_name: str
    applicability_scopes: Tuple[ApplicabilityScope, ...]
    source_bound_required: bool
    version_required: bool
    effective_date_required: bool
    cross_jurisdiction_merge_allowed: bool
    registry_entry_ready: bool

    def __post_init__(self) -> None:
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if not self.display_name:
            raise ValueError("display_name must be non-empty")
        if not self.applicability_scopes:
            raise ValueError("applicability_scopes must be non-empty")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.version_required is not True:
            raise ValueError("version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.registry_entry_ready is not True:
            raise ValueError("registry_entry_ready must be True")


@dataclass(frozen=True, slots=True)
class JurisdictionRegistry:
    registry_id: str
    entries: Tuple[JurisdictionRegistryEntry, ...]
    country_code_required: bool
    jurisdiction_id_required: bool
    applicability_scope_required: bool
    source_bound_required: bool
    cross_jurisdiction_merge_allowed: bool
    registry_ready: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        jurisdiction_ids = {entry.jurisdiction_id for entry in self.entries}
        if len(jurisdiction_ids) != len(self.entries):
            raise ValueError("jurisdiction_id values must be unique")
        if self.country_code_required is not True:
            raise ValueError("country_code_required must be True")
        if self.jurisdiction_id_required is not True:
            raise ValueError("jurisdiction_id_required must be True")
        if self.applicability_scope_required is not True:
            raise ValueError("applicability_scope_required must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if not all(entry.registry_entry_ready for entry in self.entries):
            raise ValueError("all registry entries must be ready")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")


def build_jurisdiction_registry() -> JurisdictionRegistry:
    entries = (
        JurisdictionRegistryEntry(
            jurisdiction_id="jurisdiction_global_reference",
            country_code="GLOBAL",
            jurisdiction_level="global",
            display_name="Global reference scope",
            applicability_scopes=("source_evidence_memory",),
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_jurisdiction_merge_allowed=False,
            registry_entry_ready=True,
        ),
        JurisdictionRegistryEntry(
            jurisdiction_id="jurisdiction_eu_union",
            country_code="EU",
            jurisdiction_level="union",
            display_name="European Union regulatory scope",
            applicability_scopes=("regulatory_memory", "compliance_memory", "source_evidence_memory"),
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_jurisdiction_merge_allowed=False,
            registry_entry_ready=True,
        ),
        JurisdictionRegistryEntry(
            jurisdiction_id="jurisdiction_de_country",
            country_code="DE",
            jurisdiction_level="country",
            display_name="Germany country regulatory scope",
            applicability_scopes=("tenant_policy", "regulatory_memory", "compliance_memory", "enterprise_policy_memory"),
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_jurisdiction_merge_allowed=False,
            registry_entry_ready=True,
        ),
        JurisdictionRegistryEntry(
            jurisdiction_id="jurisdiction_ua_country",
            country_code="UA",
            jurisdiction_level="country",
            display_name="Ukraine country regulatory scope",
            applicability_scopes=("tenant_policy", "regulatory_memory", "compliance_memory"),
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_jurisdiction_merge_allowed=False,
            registry_entry_ready=True,
        ),
        JurisdictionRegistryEntry(
            jurisdiction_id="jurisdiction_us_federal",
            country_code="US",
            jurisdiction_level="federal",
            display_name="United States federal regulatory scope",
            applicability_scopes=("tenant_policy", "regulatory_memory", "compliance_memory"),
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_jurisdiction_merge_allowed=False,
            registry_entry_ready=True,
        ),
    )

    return JurisdictionRegistry(
        registry_id="jurisdiction_registry_step_2_001",
        entries=entries,
        country_code_required=True,
        jurisdiction_id_required=True,
        applicability_scope_required=True,
        source_bound_required=True,
        cross_jurisdiction_merge_allowed=False,
        registry_ready=True,
    )
