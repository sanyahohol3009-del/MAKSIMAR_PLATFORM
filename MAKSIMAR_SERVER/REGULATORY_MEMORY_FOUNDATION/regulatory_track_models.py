from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


RegulatoryTrackRule = Literal[
    "no_second_memory_world",
    "mempalace_not_source_of_truth",
    "no_cross_tenant_merge",
    "no_cross_jurisdiction_merge",
    "source_version_and_effective_date_required",
]

RegulatoryTrackStage = Literal[
    "surface_inventory",
    "country_jurisdiction_registry",
    "tenant_regulatory_scope",
    "source_version_precedence",
    "conflict_drift_supersession",
    "compliance_evidence_pack",
    "regulatory_update_approval",
    "regulatory_routing_no_leak",
    "final_closure",
]


@dataclass(frozen=True, slots=True)
class RegulatoryTrackRuleStatus:
    rule_id: RegulatoryTrackRule
    enforced: bool
    violation_allowed: bool
    operator_visible: bool

    def __post_init__(self) -> None:
        if self.enforced is not True:
            raise ValueError("enforced must be True")
        if self.violation_allowed:
            raise ValueError("violation_allowed must be False")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryTrackContract:
    contract_id: str
    roadmap_family: str
    track_id: str
    current_step: str
    stages: Tuple[RegulatoryTrackStage, ...]
    rules: Tuple[RegulatoryTrackRuleStatus, ...]
    memory_v5_1_closed_reference: bool
    reopen_memory_v5_1_allowed: bool
    hardening_binding_closure_track: bool
    regulatory_track_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "regulatory_memory_foundation":
            raise ValueError("roadmap_family must be regulatory_memory_foundation")
        if self.track_id != "multi_tenant_multi_country_regulatory_memory_foundation":
            raise ValueError("unexpected track_id")
        if self.current_step != "STEP 1 — Regulatory Track Entry / Surface Inventory":
            raise ValueError("unexpected current_step")
        if len(self.stages) != 9:
            raise ValueError("regulatory track must contain exactly 9 stages")
        if len(self.rules) != 5:
            raise ValueError("step 1 must contain exactly 5 rules/gates")
        if self.memory_v5_1_closed_reference is not True:
            raise ValueError("memory_v5_1_closed_reference must be True")
        if self.reopen_memory_v5_1_allowed:
            raise ValueError("reopen_memory_v5_1_allowed must be False")
        if self.hardening_binding_closure_track is not True:
            raise ValueError("hardening_binding_closure_track must be True")
        if self.regulatory_track_ready is not True:
            raise ValueError("regulatory_track_ready must be True")


def build_regulatory_track_contract() -> RegulatoryTrackContract:
    stages: Tuple[RegulatoryTrackStage, ...] = (
        "surface_inventory",
        "country_jurisdiction_registry",
        "tenant_regulatory_scope",
        "source_version_precedence",
        "conflict_drift_supersession",
        "compliance_evidence_pack",
        "regulatory_update_approval",
        "regulatory_routing_no_leak",
        "final_closure",
    )

    rules = (
        RegulatoryTrackRuleStatus("no_second_memory_world", True, False, True),
        RegulatoryTrackRuleStatus("mempalace_not_source_of_truth", True, False, True),
        RegulatoryTrackRuleStatus("no_cross_tenant_merge", True, False, True),
        RegulatoryTrackRuleStatus("no_cross_jurisdiction_merge", True, False, True),
        RegulatoryTrackRuleStatus("source_version_and_effective_date_required", True, False, True),
    )

    return RegulatoryTrackContract(
        contract_id="regulatory_track_contract_step_1_001",
        roadmap_family="regulatory_memory_foundation",
        track_id="multi_tenant_multi_country_regulatory_memory_foundation",
        current_step="STEP 1 — Regulatory Track Entry / Surface Inventory",
        stages=stages,
        rules=rules,
        memory_v5_1_closed_reference=True,
        reopen_memory_v5_1_allowed=False,
        hardening_binding_closure_track=True,
        regulatory_track_ready=True,
    )
