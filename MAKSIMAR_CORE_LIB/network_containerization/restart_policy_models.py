from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


RestartPolicyName = Literal["no", "on-failure", "unless-stopped"]
ALLOWED_RESTART_POLICIES: tuple[RestartPolicyName, ...] = ("no", "on-failure", "unless-stopped")


@dataclass(frozen=True, slots=True)
class RestartPolicyModel:
    policy_name: RestartPolicyName
    restart_policy_required: bool
    maximum_retry_count: int
    dashboard_safe: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.policy_name not in ALLOWED_RESTART_POLICIES:
            raise ValueError(f"unsupported restart policy: {self.policy_name}")
        if not self.restart_policy_required:
            raise ValueError("restart_policy_required must remain true")
        if not isinstance(self.maximum_retry_count, int):
            raise TypeError("maximum_retry_count must be an integer")
        if self.maximum_retry_count < 0:
            raise ValueError("maximum_retry_count must not be negative")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        _validate_reason_codes(self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "restart_policy_required": self.restart_policy_required,
            "maximum_retry_count": self.maximum_retry_count,
            "dashboard_safe": self.dashboard_safe,
            "reason_codes": self.reason_codes,
        }


def build_default_restart_policy_model() -> RestartPolicyModel:
    return RestartPolicyModel(
        policy_name="unless-stopped",
        restart_policy_required=True,
        maximum_retry_count=3,
        dashboard_safe=True,
        reason_codes=("restart_policy_required", "safe_restart_policy_declared"),
    )


def _validate_reason_codes(reason_codes: tuple[str, ...]) -> None:
    if not isinstance(reason_codes, tuple):
        raise TypeError("reason_codes must be a tuple")
    if not reason_codes:
        raise ValueError("reason_codes must not be empty")
    for reason_code in reason_codes:
        if not isinstance(reason_code, str) or not reason_code:
            raise ValueError("reason_codes must contain non-empty strings")
