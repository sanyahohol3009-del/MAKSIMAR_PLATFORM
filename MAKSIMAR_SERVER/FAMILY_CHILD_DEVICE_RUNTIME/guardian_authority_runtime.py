from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.family_child_device_control.guardian_authority_contract import (
    GuardianAuthorityContract,
)


@dataclass(frozen=True)
class GuardianAuthorityDecision:
    guardian_id: str
    child_profile_id: str
    authorized: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "guardian_id": self.guardian_id,
            "child_profile_id": self.child_profile_id,
            "authorized": self.authorized,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class GuardianAuthorityRuntime:
    def evaluate(self, authority: GuardianAuthorityContract) -> GuardianAuthorityDecision:
        return GuardianAuthorityDecision(
            guardian_id=authority.guardian_id,
            child_profile_id=authority.child_profile_id,
            authorized=authority.can_authorize_child_control(),
            reason="guardian_authority_verified",
        )
