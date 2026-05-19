from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DataPlaneSemanticDuplicateBinding:
    binding_id: str
    batch_id: str
    target_family: str
    duplicate_relation: str
    action: str
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    auto_move_allowed: bool = False
    auto_delete_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("binding_id", self.binding_id),
            ("batch_id", self.batch_id),
            ("target_family", self.target_family),
            ("duplicate_relation", self.duplicate_relation),
            ("action", self.action),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.auto_move_allowed:
            raise ValueError("auto_move_allowed must remain false")
        if self.auto_delete_allowed:
            raise ValueError("auto_delete_allowed must remain false")


BATCH_2_2_SEMANTIC_DUPLICATE_BINDING = DataPlaneSemanticDuplicateBinding(
    binding_id="data_plane_batch_2_2_semantic_duplicate_binding",
    batch_id="PHASE_2_BATCH_2_2",
    target_family="append_only_log_and_immutable_ledger",
    duplicate_relation="create_new_after_clean_semantic_scan",
    action="create_only_no_move_no_delete_no_migration",
    reason_codes=(
        "true_duplicate_risk_count_zero",
        "high_risk_count_zero",
        "existing_data_plane_sources_reference_only",
    ),
)
