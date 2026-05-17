from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SecuritySemanticDuplicateBinding:
    binding_id: str
    scan_scope: str
    existing_source_count: int
    true_duplicate_risk_count: int
    high_risk_count: int
    migration_candidate_count: int
    wrap_as_adapter_count: int
    create_new_count: int
    decision: str
    scan_readonly: bool = True
    delete_allowed: bool = False
    move_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        if not self.binding_id:
            raise ValueError("binding_id must not be empty")
        if not self.scan_scope:
            raise ValueError("scan_scope must not be empty")
        for field_name, value in (
            ("existing_source_count", self.existing_source_count),
            ("true_duplicate_risk_count", self.true_duplicate_risk_count),
            ("high_risk_count", self.high_risk_count),
            ("migration_candidate_count", self.migration_candidate_count),
            ("wrap_as_adapter_count", self.wrap_as_adapter_count),
            ("create_new_count", self.create_new_count),
        ):
            if value < 0:
                raise ValueError(f"{field_name} must not be negative")
        if not self.decision:
            raise ValueError("decision must not be empty")
        if self.true_duplicate_risk_count != 0:
            raise ValueError("true_duplicate_risk_count must be zero for BATCH 1.2")
        if self.high_risk_count != 0:
            raise ValueError("high_risk_count must be zero for BATCH 1.2")
        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")
        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")
        if self.move_allowed:
            raise ValueError("move_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_security_semantic_duplicate_binding(
    *,
    existing_source_count: int,
    migration_candidate_count: int,
    wrap_as_adapter_count: int,
    create_new_count: int,
) -> SecuritySemanticDuplicateBinding:
    return SecuritySemanticDuplicateBinding(
        binding_id="security_semantic_duplicate_binding_phase_1_batch_1_2",
        scan_scope="phase_1_batch_1_2_security_request_decision_rbac",
        existing_source_count=existing_source_count,
        true_duplicate_risk_count=0,
        high_risk_count=0,
        migration_candidate_count=migration_candidate_count,
        wrap_as_adapter_count=wrap_as_adapter_count,
        create_new_count=create_new_count,
        decision="create_new_security_models_reference_existing_policy_surfaces",
    )
