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
class MobileIntentParserContract:
    contract_id: str
    parser_mode: str
    mobile_change_request_becomes_server_intent: bool
    local_command_execution_allowed: bool
    core_action_execution_allowed: bool
    direct_phone_control_allowed: bool
    shell_execution_allowed: bool
    canonical_write_allowed: bool
    canonical_memory_write_allowed: bool
    server_canonical_write_allowed: bool
    proposal_only: bool
    approval_required_for_actions: bool
    text_intent_only: bool
    app_safe_only: bool
    sends_to_server_as_intent_candidate: bool
    mobile_junior_may_not_execute_core_actions: bool
    server_jARVIS_remains_senior_authority: bool
    direct_execution_allowed: bool
    canonical_mutation_allowed: bool
    deployment_allowed: bool
    owner_approval_bypass_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        object.__setattr__(self, "parser_mode", _ensure_non_empty(self.parser_mode, "parser_mode"))
        _require_true(
            self.mobile_change_request_becomes_server_intent,
            "mobile_change_request_becomes_server_intent",
        )
        _require_false(
            self.local_command_execution_allowed,
            "local_command_execution_allowed",
        )
        _require_false(
            self.core_action_execution_allowed,
            "core_action_execution_allowed",
        )
        _require_false(
            self.direct_phone_control_allowed,
            "direct_phone_control_allowed",
        )
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(
            self.canonical_memory_write_allowed,
            "canonical_memory_write_allowed",
        )
        _require_false(
            self.server_canonical_write_allowed,
            "server_canonical_write_allowed",
        )
        _require_true(self.proposal_only, "proposal_only")
        _require_true(
            self.approval_required_for_actions,
            "approval_required_for_actions",
        )
        _require_true(self.text_intent_only, "text_intent_only")
        _require_true(self.app_safe_only, "app_safe_only")
        _require_true(
            self.sends_to_server_as_intent_candidate,
            "sends_to_server_as_intent_candidate",
        )
        _require_true(
            self.mobile_junior_may_not_execute_core_actions,
            "mobile_junior_may_not_execute_core_actions",
        )
        _require_true(
            self.server_jARVIS_remains_senior_authority,
            "server_jARVIS_remains_senior_authority",
        )
        _require_false(self.direct_execution_allowed, "direct_execution_allowed")
        _require_false(
            self.canonical_mutation_allowed,
            "canonical_mutation_allowed",
        )
        _require_false(self.deployment_allowed, "deployment_allowed")
        _require_false(
            self.owner_approval_bypass_allowed,
            "owner_approval_bypass_allowed",
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "parser_mode": self.parser_mode,
            "mobile_change_request_becomes_server_intent": (
                self.mobile_change_request_becomes_server_intent
            ),
            "local_command_execution_allowed": self.local_command_execution_allowed,
            "core_action_execution_allowed": self.core_action_execution_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "canonical_memory_write_allowed": self.canonical_memory_write_allowed,
            "server_canonical_write_allowed": self.server_canonical_write_allowed,
            "proposal_only": self.proposal_only,
            "approval_required_for_actions": self.approval_required_for_actions,
            "text_intent_only": self.text_intent_only,
            "app_safe_only": self.app_safe_only,
            "sends_to_server_as_intent_candidate": (
                self.sends_to_server_as_intent_candidate
            ),
            "mobile_junior_may_not_execute_core_actions": (
                self.mobile_junior_may_not_execute_core_actions
            ),
            "server_jARVIS_remains_senior_authority": (
                self.server_jARVIS_remains_senior_authority
            ),
            "direct_execution_allowed": self.direct_execution_allowed,
            "canonical_mutation_allowed": self.canonical_mutation_allowed,
            "deployment_allowed": self.deployment_allowed,
            "owner_approval_bypass_allowed": self.owner_approval_bypass_allowed,
        }


def build_mobile_intent_parser_contract() -> MobileIntentParserContract:
    return MobileIntentParserContract(
        contract_id="mobile_intent_parser_contract_v0_1",
        parser_mode="mobile_text_to_app_safe_intent_candidate",
        mobile_change_request_becomes_server_intent=True,
        local_command_execution_allowed=False,
        core_action_execution_allowed=False,
        direct_phone_control_allowed=False,
        shell_execution_allowed=False,
        canonical_write_allowed=False,
        canonical_memory_write_allowed=False,
        server_canonical_write_allowed=False,
        proposal_only=True,
        approval_required_for_actions=True,
        text_intent_only=True,
        app_safe_only=True,
        sends_to_server_as_intent_candidate=True,
        mobile_junior_may_not_execute_core_actions=True,
        server_jARVIS_remains_senior_authority=True,
        direct_execution_allowed=False,
        canonical_mutation_allowed=False,
        deployment_allowed=False,
        owner_approval_bypass_allowed=False,
    )
