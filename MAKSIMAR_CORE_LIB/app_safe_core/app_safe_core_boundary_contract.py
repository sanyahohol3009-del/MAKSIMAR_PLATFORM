from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class AppSafeCoreBoundaryContract:
    contract_id: str
    app_safe_core_boundary: bool
    read_only_export_allowed: bool
    intent_only_access: bool
    canonical_core_access_allowed: bool
    canonical_truth_allowed: bool
    canonical_write_allowed: bool
    canonical_memory_write_allowed: bool
    core_action_execution_allowed: bool
    shell_execution_allowed: bool
    pc_control_allowed: bool
    direct_mobile_control_allowed: bool
    server_mutation_allowed: bool
    deployment_allowed: bool
    proposal_only: bool
    app_safe_only: bool
    junior_model_may_read_mirror: bool
    junior_model_may_mutate_mirror: bool
    junior_model_may_execute_core_actions: bool
    owner_approval_required: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        _require_true(self.app_safe_core_boundary, "app_safe_core_boundary")
        _require_true(self.read_only_export_allowed, "read_only_export_allowed")
        _require_true(self.intent_only_access, "intent_only_access")
        _require_false(
            self.canonical_core_access_allowed,
            "canonical_core_access_allowed",
        )
        _require_false(self.canonical_truth_allowed, "canonical_truth_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(
            self.canonical_memory_write_allowed,
            "canonical_memory_write_allowed",
        )
        _require_false(
            self.core_action_execution_allowed,
            "core_action_execution_allowed",
        )
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.server_mutation_allowed, "server_mutation_allowed")
        _require_false(self.deployment_allowed, "deployment_allowed")
        _require_true(self.proposal_only, "proposal_only")
        _require_true(self.app_safe_only, "app_safe_only")
        _require_true(
            self.junior_model_may_read_mirror,
            "junior_model_may_read_mirror",
        )
        _require_false(
            self.junior_model_may_mutate_mirror,
            "junior_model_may_mutate_mirror",
        )
        _require_false(
            self.junior_model_may_execute_core_actions,
            "junior_model_may_execute_core_actions",
        )
        _require_true(self.owner_approval_required, "owner_approval_required")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "app_safe_core_boundary": self.app_safe_core_boundary,
            "read_only_export_allowed": self.read_only_export_allowed,
            "intent_only_access": self.intent_only_access,
            "canonical_core_access_allowed": self.canonical_core_access_allowed,
            "canonical_truth_allowed": self.canonical_truth_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "core_action_execution_allowed": self.core_action_execution_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "server_mutation_allowed": self.server_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "proposal_only": self.proposal_only,
            "app_safe_only": self.app_safe_only,
            "junior_model_may_read_mirror": self.junior_model_may_read_mirror,
            "junior_model_may_mutate_mirror": self.junior_model_may_mutate_mirror,
            "junior_model_may_execute_core_actions": (
                self.junior_model_may_execute_core_actions
            ),
            "owner_approval_required": self.owner_approval_required,
        }


def build_app_safe_core_boundary_contract() -> AppSafeCoreBoundaryContract:
    return AppSafeCoreBoundaryContract(
        contract_id="app_safe_core_boundary_contract_v0_1",
        app_safe_core_boundary=True,
        read_only_export_allowed=True,
        intent_only_access=True,
        canonical_core_access_allowed=False,
        canonical_truth_allowed=False,
        canonical_write_allowed=False,
        canonical_memory_write_allowed=False,
        core_action_execution_allowed=False,
        shell_execution_allowed=False,
        pc_control_allowed=False,
        direct_mobile_control_allowed=False,
        server_mutation_allowed=False,
        deployment_allowed=False,
        proposal_only=True,
        app_safe_only=True,
        junior_model_may_read_mirror=True,
        junior_model_may_mutate_mirror=False,
        junior_model_may_execute_core_actions=False,
        owner_approval_required=True,
    )
