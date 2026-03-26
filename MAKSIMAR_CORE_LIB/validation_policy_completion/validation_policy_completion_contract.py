from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.validation_policy import (
    build_validation_error_contract,
    build_validation_payload_class_contract,
    build_validation_policy_contract,
    build_validation_task_class_contract,
    build_validation_tier_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.validation_gate import (
    build_server_validation_gate_contract,
)


ValidationTier = Literal[
    "L1_HEADER",
    "L2_SCHEMA",
    "L3_DEEP",
]

ValidationRiskLevel = Literal[
    "low",
    "medium",
    "high",
    "critical",
]

ValidationCompletionStatus = Literal[
    "completed",
]


_COMPLETION_ENTRY_ID_PATTERN = re.compile(
    r"^validationcompletion_[a-z][a-z0-9_]*$"
)
_TASK_CLASS_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_PAYLOAD_CLASS_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
_POLICY_RULE_ID_PATTERN = re.compile(r"^policy_[a-z][a-z0-9_]*$")
_ERROR_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ValidationPolicyCompletionEntry:
    """Canonical validation policy completion entry."""

    completion_entry_id: str
    task_class: str
    payload_class: str
    required_validation_tier: ValidationTier
    effective_risk_level: ValidationRiskLevel
    policy_rule_id: str
    deep_validation_required: bool
    payload_reference_required: bool
    error_code_on_failure: str
    completion_valid: bool
    completion_status: ValidationCompletionStatus
    description: str

    def __post_init__(self) -> None:
        """Validate validation policy completion invariants."""
        if not _COMPLETION_ENTRY_ID_PATTERN.fullmatch(self.completion_entry_id):
            raise ValueError(
                f"Invalid completion_entry_id: {self.completion_entry_id}"
            )

        if not _TASK_CLASS_PATTERN.fullmatch(self.task_class):
            raise ValueError(f"Invalid task_class: {self.task_class}")

        if not _PAYLOAD_CLASS_PATTERN.fullmatch(self.payload_class):
            raise ValueError(f"Invalid payload_class: {self.payload_class}")

        if not _POLICY_RULE_ID_PATTERN.fullmatch(self.policy_rule_id):
            raise ValueError(f"Invalid policy_rule_id: {self.policy_rule_id}")

        if not _ERROR_CODE_PATTERN.fullmatch(self.error_code_on_failure):
            raise ValueError(
                f"Invalid error_code_on_failure: {self.error_code_on_failure}"
            )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.completion_entry_id}"
            )

        if not self.completion_valid:
            raise ValueError(
                f"validation completion entry must be valid: {self.completion_entry_id}"
            )

        if self.completion_status != "completed":
            raise ValueError(
                f"validation completion entry must be completed: {self.completion_entry_id}"
            )

        if self.task_class == "chat_request" and self.payload_class == "small_control":
            if self.required_validation_tier != "L1_HEADER":
                raise ValueError(
                    f"chat_request + small_control must map to L1_HEADER: {self.completion_entry_id}"
                )
            if self.effective_risk_level != "low":
                raise ValueError(
                    f"chat_request + small_control must map to low risk: {self.completion_entry_id}"
                )
            if self.deep_validation_required:
                raise ValueError(
                    f"chat_request + small_control must not require deep validation: {self.completion_entry_id}"
                )
            if self.payload_reference_required:
                raise ValueError(
                    f"chat_request + small_control must not require payload reference: {self.completion_entry_id}"
                )
            if self.error_code_on_failure != "invalid_header":
                raise ValueError(
                    f"chat_request + small_control must fail with invalid_header: {self.completion_entry_id}"
                )

        if (
            self.task_class == "simulation_request"
            and self.payload_class == "medium_contract"
        ):
            if self.required_validation_tier != "L2_SCHEMA":
                raise ValueError(
                    f"simulation_request + medium_contract must map to L2_SCHEMA: {self.completion_entry_id}"
                )
            if self.effective_risk_level != "medium":
                raise ValueError(
                    f"simulation_request + medium_contract must map to medium risk: {self.completion_entry_id}"
                )
            if self.deep_validation_required:
                raise ValueError(
                    f"simulation_request + medium_contract must not require deep validation by default: {self.completion_entry_id}"
                )
            if self.payload_reference_required:
                raise ValueError(
                    f"simulation_request + medium_contract must not require payload reference: {self.completion_entry_id}"
                )
            if self.error_code_on_failure != "invalid_schema":
                raise ValueError(
                    f"simulation_request + medium_contract must fail with invalid_schema: {self.completion_entry_id}"
                )

        if (
            self.task_class == "robotics_action"
            and self.payload_class == "heavy_artifact"
        ):
            if self.required_validation_tier != "L3_DEEP":
                raise ValueError(
                    f"robotics_action + heavy_artifact must map to L3_DEEP: {self.completion_entry_id}"
                )
            if self.effective_risk_level != "critical":
                raise ValueError(
                    f"robotics_action + heavy_artifact must map to critical risk: {self.completion_entry_id}"
                )
            if not self.deep_validation_required:
                raise ValueError(
                    f"robotics_action + heavy_artifact must require deep validation: {self.completion_entry_id}"
                )
            if not self.payload_reference_required:
                raise ValueError(
                    f"robotics_action + heavy_artifact must require payload reference: {self.completion_entry_id}"
                )
            if self.error_code_on_failure != "deep_validation_failed":
                raise ValueError(
                    f"robotics_action + heavy_artifact must fail with deep_validation_failed: {self.completion_entry_id}"
                )


@dataclass(frozen=True, slots=True)
class ValidationPolicyCompletionContract:
    """Unified validation policy completion contract."""

    total_entries: int
    deep_validation_entries: int
    payload_reference_entries: int
    completed_entries: int
    entries: tuple[ValidationPolicyCompletionEntry, ...]

    def __post_init__(self) -> None:
        """Validate validation policy completion contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        deep_validation_entries = sum(
            1 for entry in self.entries if entry.deep_validation_required
        )
        payload_reference_entries = sum(
            1 for entry in self.entries if entry.payload_reference_required
        )
        completed_entries = sum(
            1 for entry in self.entries if entry.completion_status == "completed"
        )

        if self.deep_validation_entries != deep_validation_entries:
            raise ValueError("deep_validation_entries must match computed count")

        if self.payload_reference_entries != payload_reference_entries:
            raise ValueError("payload_reference_entries must match computed count")

        if self.completed_entries != completed_entries:
            raise ValueError("completed_entries must match computed count")

        entry_ids = tuple(entry.completion_entry_id for entry in self.entries)
        policy_rule_ids = tuple(entry.policy_rule_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate completion_entry_id values detected")

        if len(set(policy_rule_ids)) != len(policy_rule_ids):
            raise ValueError("Duplicate policy_rule_id values detected")


def build_validation_policy_completion_contract() -> ValidationPolicyCompletionContract:
    """Build canonical validation policy completion contract."""
    tier_contract = build_validation_tier_contract()
    task_contract = build_validation_task_class_contract()
    payload_contract = build_validation_payload_class_contract()
    policy_contract = build_validation_policy_contract()
    error_contract = build_validation_error_contract()
    validation_gate = build_server_validation_gate_contract()

    if tier_contract.total_tiers != 3:
        raise ValueError("Expected canonical validation tier count = 3")

    if task_contract.total_task_classes <= 0:
        raise ValueError("Task class contract must expose task classes")

    if payload_contract.total_payload_classes <= 0:
        raise ValueError("Payload class contract must expose payload classes")

    if policy_contract.total_rules <= 0:
        raise ValueError("Policy contract must expose rules")

    if error_contract.total_errors <= 0:
        raise ValueError("Error contract must expose errors")

    if validation_gate.total_entries <= 0:
        raise ValueError("Validation gate contract must expose entries")

    task_by_name = {
        entry.task_class: entry for entry in task_contract.task_classes
    }
    payload_by_name = {
        entry.payload_class: entry for entry in payload_contract.payload_classes
    }
    policy_by_rule_id = {
        entry.rule_id: entry for entry in policy_contract.rules
    }
    error_codes = {entry.error_code for entry in error_contract.errors}

    required_tasks = {
        "chat_request",
        "simulation_request",
        "robotics_action",
    }
    required_payloads = {
        "small_control",
        "medium_contract",
        "heavy_artifact",
    }
    required_rules = {
        "policy_chat_request_small_control",
        "policy_simulation_request_medium_contract",
        "policy_robotics_action_heavy_artifact",
    }
    required_errors = {
        "invalid_header",
        "invalid_schema",
        "deep_validation_failed",
    }

    missing_tasks = required_tasks - set(task_by_name)
    if missing_tasks:
        raise ValueError(f"Missing task classes: {sorted(missing_tasks)}")

    missing_payloads = required_payloads - set(payload_by_name)
    if missing_payloads:
        raise ValueError(f"Missing payload classes: {sorted(missing_payloads)}")

    missing_rules = required_rules - set(policy_by_rule_id)
    if missing_rules:
        raise ValueError(f"Missing policy rules: {sorted(missing_rules)}")

    missing_errors = required_errors - error_codes
    if missing_errors:
        raise ValueError(f"Missing validation errors: {sorted(missing_errors)}")

    entries = (
        ValidationPolicyCompletionEntry(
            completion_entry_id="validationcompletion_chat_small_001",
            task_class="chat_request",
            payload_class="small_control",
            required_validation_tier="L1_HEADER",
            effective_risk_level="low",
            policy_rule_id="policy_chat_request_small_control",
            deep_validation_required=False,
            payload_reference_required=False,
            error_code_on_failure="invalid_header",
            completion_valid=True,
            completion_status="completed",
            description="Completed validation policy mapping for chat_request + small_control.",
        ),
        ValidationPolicyCompletionEntry(
            completion_entry_id="validationcompletion_simulation_medium_001",
            task_class="simulation_request",
            payload_class="medium_contract",
            required_validation_tier="L2_SCHEMA",
            effective_risk_level="medium",
            policy_rule_id="policy_simulation_request_medium_contract",
            deep_validation_required=False,
            payload_reference_required=False,
            error_code_on_failure="invalid_schema",
            completion_valid=True,
            completion_status="completed",
            description="Completed validation policy mapping for simulation_request + medium_contract.",
        ),
        ValidationPolicyCompletionEntry(
            completion_entry_id="validationcompletion_robotics_heavy_001",
            task_class="robotics_action",
            payload_class="heavy_artifact",
            required_validation_tier="L3_DEEP",
            effective_risk_level="critical",
            policy_rule_id="policy_robotics_action_heavy_artifact",
            deep_validation_required=True,
            payload_reference_required=True,
            error_code_on_failure="deep_validation_failed",
            completion_valid=True,
            completion_status="completed",
            description="Completed validation policy mapping for robotics_action + heavy_artifact.",
        ),
    )

    deep_validation_entries = sum(
        1 for entry in entries if entry.deep_validation_required
    )
    payload_reference_entries = sum(
        1 for entry in entries if entry.payload_reference_required
    )
    completed_entries = sum(
        1 for entry in entries if entry.completion_status == "completed"
    )

    return ValidationPolicyCompletionContract(
        total_entries=len(entries),
        deep_validation_entries=deep_validation_entries,
        payload_reference_entries=payload_reference_entries,
        completed_entries=completed_entries,
        entries=entries,
    )
