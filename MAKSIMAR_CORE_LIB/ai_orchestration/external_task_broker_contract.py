from __future__ import annotations

from dataclasses import dataclass
from typing import Any


EXTERNAL_TASK_BROKER_IDS: tuple[str, ...] = ("codex", "gemini")
EXTERNAL_TASK_BROKER_MODES: tuple[str, ...] = (
    "task_broker",
    "proposal_source",
    "reference_source",
)
EXTERNAL_TASK_BROKER_TASK_CATEGORIES: tuple[str, ...] = (
    "code_review",
    "implementation_plan",
    "test_plan",
    "documentation_draft",
    "architecture_review",
    "error_analysis",
)
EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES: tuple[str, ...] = (
    "direct_execution",
    "shell_execution",
    "local_file_mutation",
    "git_operation",
    "browser_control",
    "app_control",
    "pc_control",
    "network_port_open",
    "model_download",
    "runtime_start",
    "dashboard_execution",
)


@dataclass(frozen=True, slots=True)
class ExternalTaskBrokerBinding:
    broker_id: str
    broker_modes: tuple[str, ...]
    allowed_task_categories: tuple[str, ...]
    forbidden_capabilities: tuple[str, ...]
    owner_command_required: bool = True
    approval_required: bool = True
    audit_required: bool = True
    preview_required: bool = True
    allowlist_required: bool = True
    proposal_only: bool = True
    direct_execution_allowed: bool = False
    local_mutation_allowed: bool = False
    runtime_start_allowed: bool = False
    model_download_allowed: bool = False
    pc_control_allowed: bool = False

    def __post_init__(self) -> None:
        _require_member(self.broker_id, EXTERNAL_TASK_BROKER_IDS, "broker_id")
        _require_exact_tuple(self.broker_modes, EXTERNAL_TASK_BROKER_MODES, "broker_modes")
        _require_exact_tuple(
            self.allowed_task_categories,
            EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
            "allowed_task_categories",
        )
        _require_exact_tuple(
            self.forbidden_capabilities,
            EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
            "forbidden_capabilities",
        )
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.preview_required, "preview_required")
        _require_true(self.allowlist_required, "allowlist_required")
        _require_true(self.proposal_only, "proposal_only")
        _require_false(self.direct_execution_allowed, "direct_execution_allowed")
        _require_false(self.local_mutation_allowed, "local_mutation_allowed")
        _require_false(self.runtime_start_allowed, "runtime_start_allowed")
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "broker_id": self.broker_id,
            "broker_modes": self.broker_modes,
            "allowed_task_categories": self.allowed_task_categories,
            "forbidden_capabilities": self.forbidden_capabilities,
            "owner_command_required": self.owner_command_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "preview_required": self.preview_required,
            "allowlist_required": self.allowlist_required,
            "proposal_only": self.proposal_only,
            "direct_execution_allowed": self.direct_execution_allowed,
            "local_mutation_allowed": self.local_mutation_allowed,
            "runtime_start_allowed": self.runtime_start_allowed,
            "model_download_allowed": self.model_download_allowed,
            "pc_control_allowed": self.pc_control_allowed,
        }


@dataclass(frozen=True, slots=True)
class ExternalTaskBrokerContract:
    brokers: tuple[ExternalTaskBrokerBinding, ...]
    broker_ids: tuple[str, ...] = EXTERNAL_TASK_BROKER_IDS
    broker_modes: tuple[str, ...] = EXTERNAL_TASK_BROKER_MODES
    allowed_task_categories: tuple[str, ...] = EXTERNAL_TASK_BROKER_TASK_CATEGORIES
    forbidden_capabilities: tuple[str, ...] = EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES

    def __post_init__(self) -> None:
        if tuple(broker.broker_id for broker in self.brokers) != EXTERNAL_TASK_BROKER_IDS:
            raise ValueError("brokers must match canonical external task broker ids")
        _require_exact_tuple(self.broker_ids, EXTERNAL_TASK_BROKER_IDS, "broker_ids")
        _require_exact_tuple(self.broker_modes, EXTERNAL_TASK_BROKER_MODES, "broker_modes")
        _require_exact_tuple(
            self.allowed_task_categories,
            EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
            "allowed_task_categories",
        )
        _require_exact_tuple(
            self.forbidden_capabilities,
            EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
            "forbidden_capabilities",
        )

    def is_external_broker_allowed(self, broker_id: str) -> bool:
        assert_external_broker_not_executor(broker_id)
        return broker_id in self.broker_ids

    def to_read_model(self) -> dict[str, Any]:
        return {
            "brokers": tuple(broker.to_read_model() for broker in self.brokers),
            "broker_ids": self.broker_ids,
            "broker_count": len(self.brokers),
            "broker_modes": self.broker_modes,
            "allowed_task_categories": self.allowed_task_categories,
            "forbidden_capabilities": self.forbidden_capabilities,
            "proposal_only": True,
            "direct_execution_allowed": False,
            "local_mutation_allowed": False,
            "runtime_start_allowed": False,
            "model_download_allowed": False,
            "pc_control_allowed": False,
        }


def build_external_task_broker_contract() -> ExternalTaskBrokerContract:
    return ExternalTaskBrokerContract(
        brokers=tuple(
            ExternalTaskBrokerBinding(
                broker_id=broker_id,
                broker_modes=EXTERNAL_TASK_BROKER_MODES,
                allowed_task_categories=EXTERNAL_TASK_BROKER_TASK_CATEGORIES,
                forbidden_capabilities=EXTERNAL_TASK_BROKER_FORBIDDEN_CAPABILITIES,
            )
            for broker_id in EXTERNAL_TASK_BROKER_IDS
        )
    )


def is_external_broker_allowed(broker_id: str) -> bool:
    return build_external_task_broker_contract().is_external_broker_allowed(broker_id)


def assert_external_broker_not_executor(broker_id: str) -> None:
    _require_non_empty(broker_id, "broker_id")
    if broker_id not in EXTERNAL_TASK_BROKER_IDS:
        raise ValueError(f"unsupported external task broker: {broker_id}")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_member(value: str, allowed_values: tuple[str, ...], field_name: str) -> None:
    _require_non_empty(value, field_name)
    if value not in allowed_values:
        raise ValueError(f"{field_name} has unsupported value: {value}")


def _require_exact_tuple(
    value: tuple[str, ...],
    expected: tuple[str, ...],
    field_name: str,
) -> None:
    if value != expected:
        raise ValueError(f"{field_name} must match canonical values")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain required")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

