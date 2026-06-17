from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TTSVoiceProfile:
    profile_id: str
    engine_kind: str
    voice_id: str
    role: str
    primary_allowed: bool
    rejected_as_primary: bool

    def __post_init__(self) -> None:
        if not self.profile_id.strip():
            raise ValueError("profile_id must be non-empty")
        if self.role not in {"primary_candidate", "fallback_candidate", "legacy_rejected"}:
            raise ValueError("unsupported role")
        if self.rejected_as_primary and self.primary_allowed:
            raise ValueError("rejected voice cannot be primary")


@dataclass(frozen=True)
class TTSVoiceProfilePolicy:
    profiles: tuple[TTSVoiceProfile, ...]
    direct_tts_to_core_allowed: bool

    def __post_init__(self) -> None:
        if not self.profiles:
            raise ValueError("profiles must be non-empty")
        if self.direct_tts_to_core_allowed:
            raise ValueError("direct_tts_to_core_allowed must remain false")

    def to_read_model(self) -> dict[str, object]:
        return {
            "direct_tts_to_core_allowed": self.direct_tts_to_core_allowed,
            "profiles": tuple(p.__dict__ for p in self.profiles),
        }


def build_default_tts_voice_profile_policy() -> TTSVoiceProfilePolicy:
    return TTSVoiceProfilePolicy(
        direct_tts_to_core_allowed=False,
        profiles=(
            TTSVoiceProfile(
                profile_id="windows_voice_edge_tts_candidate",
                engine_kind="windows_or_local_tts_candidate",
                voice_id="to_be_selected_by_smoke",
                role="primary_candidate",
                primary_allowed=True,
                rejected_as_primary=False,
            ),
            TTSVoiceProfile(
                profile_id="piper_ru_denis_medium_legacy_rejected",
                engine_kind="piper",
                voice_id="ru_RU-denis-medium",
                role="legacy_rejected",
                primary_allowed=False,
                rejected_as_primary=True,
            ),
        ),
    )
