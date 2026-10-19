from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.security_layer.jarvis_family_profile_contract import (
    build_child_profile,
    build_owner_profile,
    build_trusted_family_profile,
)
from MAKSIMAR_CORE_LIB.security_layer.owner_identity_claim import OwnerIdentityClaim


_OWNER_HINTS = {"owner", "owner_profile_aleksandr_v1", "aleksandr"}
_TRUSTED_FAMILY_HINTS = {"trusted_family", "trusted_family_yulia_v1", "yulia", "юля"}
_CHILD_MAKSIM_HINTS = {"child_maksim_v1", "maksim", "максим"}
_CHILD_MAKAR_HINTS = {"child_makar_v1", "makar", "макар"}
_UNKNOWN_HINTS = {"unknown", "unknown_profile_v1"}


@dataclass(frozen=True, slots=True)
class ResolvedSpeakerProfile:
    profile_id: str
    profile_type: str
    display_name: str
    direct_pc_action_eligible: bool
    reason_codes: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "profile_type": self.profile_type,
            "display_name": self.display_name,
            "direct_pc_action_eligible": self.direct_pc_action_eligible,
            "reason_codes": self.reason_codes,
        }


def resolve_speaker_profile(
    owner_identity_claim: OwnerIdentityClaim,
    *,
    speaker_profile_hint: str | None = None,
) -> ResolvedSpeakerProfile:
    normalized_hint = str(speaker_profile_hint or "").strip().casefold()

    if normalized_hint in _OWNER_HINTS:
        profile = build_owner_profile().to_read_model()
        return ResolvedSpeakerProfile(
            profile_id=str(profile["profile_id"]),
            profile_type=str(profile["profile_type"]),
            display_name=str(profile["display_name"]),
            direct_pc_action_eligible=bool(
                owner_identity_claim.verified and owner_identity_claim.source == "local_terminal_session"
            ),
            reason_codes=("speaker_hint_owner", "approval_gate_preserved"),
        )
    if normalized_hint in _TRUSTED_FAMILY_HINTS:
        profile = build_trusted_family_profile().to_read_model()
        return ResolvedSpeakerProfile(
            profile_id="trusted_family_yulia_v1",
            profile_type=str(profile["profile_type"]),
            display_name=str(profile["display_name"]),
            direct_pc_action_eligible=False,
            reason_codes=("speaker_hint_trusted_family", "contract_fixture_only"),
        )
    if normalized_hint in _CHILD_MAKSIM_HINTS:
        profile = build_child_profile(child_name="Максим").to_read_model()
        return ResolvedSpeakerProfile(
            profile_id="child_maksim_v1",
            profile_type=str(profile["profile_type"]),
            display_name=str(profile["display_name"]),
            direct_pc_action_eligible=False,
            reason_codes=("speaker_hint_child", "contract_fixture_only"),
        )
    if normalized_hint in _CHILD_MAKAR_HINTS:
        profile = build_child_profile(child_name="Макар").to_read_model()
        return ResolvedSpeakerProfile(
            profile_id="child_makar_v1",
            profile_type=str(profile["profile_type"]),
            display_name=str(profile["display_name"]),
            direct_pc_action_eligible=False,
            reason_codes=("speaker_hint_child", "contract_fixture_only"),
        )
    if normalized_hint in _UNKNOWN_HINTS:
        return _build_unknown_profile("speaker_hint_unknown")

    if owner_identity_claim.source == "local_terminal_session":
        profile = build_owner_profile().to_read_model()
        return ResolvedSpeakerProfile(
            profile_id=str(profile["profile_id"]),
            profile_type=str(profile["profile_type"]),
            display_name=str(profile["display_name"]),
            direct_pc_action_eligible=bool(owner_identity_claim.verified),
            reason_codes=("local_terminal_session", "owner_default"),
        )
    if owner_identity_claim.source == "voice_unverified":
        return _build_unknown_profile("voice_unverified")

    return _build_unknown_profile("unknown_source_fallback")


def resolve_family_profile(*, identity_id: str, profile_type: str) -> ResolvedSpeakerProfile | None:
    """Resolve an authenticated family identity from the canonical family profile builders."""
    normalized_identity = str(identity_id).strip().casefold()
    normalized_type = str(profile_type).strip()
    if normalized_type == "owner" and normalized_identity in _OWNER_HINTS:
        profile = build_owner_profile().to_read_model()
    elif normalized_type == "trusted_family" and normalized_identity in _TRUSTED_FAMILY_HINTS:
        profile = build_trusted_family_profile().to_read_model()
    elif normalized_type == "child" and normalized_identity in _CHILD_MAKSIM_HINTS:
        profile = build_child_profile(child_name="Максим").to_read_model()
    elif normalized_type == "child" and normalized_identity in _CHILD_MAKAR_HINTS:
        profile = build_child_profile(child_name="Макар").to_read_model()
    else:
        return None
    return ResolvedSpeakerProfile(
        profile_id=str(profile["profile_id"]),
        profile_type=str(profile["profile_type"]),
        display_name=str(profile["display_name"]),
        direct_pc_action_eligible=normalized_type == "owner",
        reason_codes=("canonical_family_profile", "authenticated_identity_match"),
    )


def _build_unknown_profile(reason_code: str) -> ResolvedSpeakerProfile:
    return ResolvedSpeakerProfile(
        profile_id="unknown_profile_v1",
        profile_type="unknown",
        display_name="Unknown",
        direct_pc_action_eligible=False,
        reason_codes=(reason_code, "direct_pc_action_blocked"),
    )
