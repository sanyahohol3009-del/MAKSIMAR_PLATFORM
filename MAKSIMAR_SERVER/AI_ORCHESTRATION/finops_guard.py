from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    FinOpsBudgetContract,
    build_default_finops_budget_contract,
)


@dataclass(frozen=True, slots=True)
class FinOpsGuardReadModel:
    service_id: str
    budget_contract: FinOpsBudgetContract
    budget_guard_ready: bool
    spend_execution_allowed: bool
    runtime_billing_mutation_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("service_id", self.service_id)
        if not isinstance(self.budget_contract, FinOpsBudgetContract):
            raise TypeError("budget_contract must be FinOpsBudgetContract")
        _validate_true("budget_guard_ready", self.budget_guard_ready)
        _validate_false("spend_execution_allowed", self.spend_execution_allowed)
        _validate_false("runtime_billing_mutation_allowed", self.runtime_billing_mutation_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "budget_contract": self.budget_contract.to_dict(),
            "budget_guard_ready": self.budget_guard_ready,
            "spend_execution_allowed": self.spend_execution_allowed,
            "runtime_billing_mutation_allowed": self.runtime_billing_mutation_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_finops_guard_read_model() -> FinOpsGuardReadModel:
    contract = build_default_finops_budget_contract()
    return FinOpsGuardReadModel(
        service_id="finops_guard_v1",
        budget_contract=contract,
        budget_guard_ready=contract.budget_guard_ready,
        spend_execution_allowed=False,
        runtime_billing_mutation_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "finops_guard_read_model_only",
            "spend_execution_blocked",
            "runtime_billing_mutation_blocked",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
