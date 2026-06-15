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
class MobileCoreMirrorContract:
    contract_id: str
    mirror_is_read_only: bool
    mirror_is_app_safe: bool
    mirror_is_canonical_truth: bool
    mirror_can_execute_actions: bool
    mirror_can_write_core: bool
    mirror_can_write_memory: bool
    mirror_can_mutate_runtime: bool
    mirror_can_deploy: bool
    mirror_can_control_pc: bool
    mirror_can_control_phone: bool
    mirror_can_bypass_approval: bool
    mirror_source_is_server_senior: bool
    junior_consumes_mirror_as_context: bool
    junior_cannot_promote_mirror_to_truth: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        _require_true(self.mirror_is_read_only, "mirror_is_read_only")
        _require_true(self.mirror_is_app_safe, "mirror_is_app_safe")
        _require_false(self.mirror_is_canonical_truth, "mirror_is_canonical_truth")
        _require_false(self.mirror_can_execute_actions, "mirror_can_execute_actions")
        _require_false(self.mirror_can_write_core, "mirror_can_write_core")
        _require_false(self.mirror_can_write_memory, "mirror_can_write_memory")
        _require_false(self.mirror_can_mutate_runtime, "mirror_can_mutate_runtime")
        _require_false(self.mirror_can_deploy, "mirror_can_deploy")
        _require_false(self.mirror_can_control_pc, "mirror_can_control_pc")
        _require_false(self.mirror_can_control_phone, "mirror_can_control_phone")
        _require_false(self.mirror_can_bypass_approval, "mirror_can_bypass_approval")
        _require_true(
            self.mirror_source_is_server_senior,
            "mirror_source_is_server_senior",
        )
        _require_true(
            self.junior_consumes_mirror_as_context,
            "junior_consumes_mirror_as_context",
        )
        _require_true(
            self.junior_cannot_promote_mirror_to_truth,
            "junior_cannot_promote_mirror_to_truth",
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "mirror_is_read_only": self.mirror_is_read_only,
            "mirror_is_app_safe": self.mirror_is_app_safe,
            "mirror_is_canonical_truth": self.mirror_is_canonical_truth,
            "mirror_can_execute_actions": self.mirror_can_execute_actions,
            "mirror_can_write_core": self.mirror_can_write_core,
            "mirror_can_write_memory": self.mirror_can_write_memory,
            "mirror_can_mutate_runtime": self.mirror_can_mutate_runtime,
            "mirror_can_deploy": self.mirror_can_deploy,
            "mirror_can_control_pc": self.mirror_can_control_pc,
            "mirror_can_control_phone": self.mirror_can_control_phone,
            "mirror_can_bypass_approval": self.mirror_can_bypass_approval,
            "mirror_source_is_server_senior": self.mirror_source_is_server_senior,
            "junior_consumes_mirror_as_context": self.junior_consumes_mirror_as_context,
            "junior_cannot_promote_mirror_to_truth": (
                self.junior_cannot_promote_mirror_to_truth
            ),
        }


def build_mobile_core_mirror_contract() -> MobileCoreMirrorContract:
    return MobileCoreMirrorContract(
        contract_id="mobile_core_mirror_contract_v0_1",
        mirror_is_read_only=True,
        mirror_is_app_safe=True,
        mirror_is_canonical_truth=False,
        mirror_can_execute_actions=False,
        mirror_can_write_core=False,
        mirror_can_write_memory=False,
        mirror_can_mutate_runtime=False,
        mirror_can_deploy=False,
        mirror_can_control_pc=False,
        mirror_can_control_phone=False,
        mirror_can_bypass_approval=False,
        mirror_source_is_server_senior=True,
        junior_consumes_mirror_as_context=True,
        junior_cannot_promote_mirror_to_truth=True,
    )
