from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class STTEngineCandidate:
    engine_id: str
    engine_kind: str
    model_id: str
    role: str
    device_class: str
    primary_allowed: bool
    fallback_allowed: bool
    legacy_only: bool

    def __post_init__(self) -> None:
        if not self.engine_id.strip():
            raise ValueError("engine_id must be non-empty")
        if self.role not in {"primary", "candidate", "fallback", "legacy"}:
            raise ValueError("unsupported role")
        if self.legacy_only and self.primary_allowed:
            raise ValueError("legacy_only engine cannot be primary")


@dataclass(frozen=True)
class STTEnginePolicy:
    candidates: tuple[STTEngineCandidate, ...]
    confidence_threshold: float
    profanity_allowed: bool
    domain: str
    raw_audio_to_core_allowed: bool

    def __post_init__(self) -> None:
        if not self.candidates:
            raise ValueError("candidates must be non-empty")
        if not 0.0 < self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be in (0, 1]")
        if self.raw_audio_to_core_allowed:
            raise ValueError("raw_audio_to_core_allowed must remain false")
        primary = [c for c in self.candidates if c.role == "primary" and c.primary_allowed]
        if len(primary) != 1:
            raise ValueError("exactly one primary STT candidate required")

    def to_read_model(self) -> dict[str, object]:
        return {
            "confidence_threshold": self.confidence_threshold,
            "profanity_allowed": self.profanity_allowed,
            "domain": self.domain,
            "raw_audio_to_core_allowed": self.raw_audio_to_core_allowed,
            "candidates": tuple(c.__dict__ for c in self.candidates),
        }


def build_default_stt_engine_policy() -> STTEnginePolicy:
    return STTEnginePolicy(
        confidence_threshold=0.85,
        profanity_allowed=True,
        domain="engineering_garage",
        raw_audio_to_core_allowed=False,
        candidates=(
            STTEngineCandidate(
                engine_id="faster_whisper_large_v3_turbo_cuda",
                engine_kind="faster_whisper",
                model_id="large-v3-turbo",
                role="primary",
                device_class="cuda_or_cpu_probe",
                primary_allowed=True,
                fallback_allowed=True,
                legacy_only=False,
            ),
            STTEngineCandidate(
                engine_id="gigaam_ru_candidate",
                engine_kind="gigaam",
                model_id="gigaam-v3-candidate",
                role="candidate",
                device_class="cuda_or_cpu_probe",
                primary_allowed=False,
                fallback_allowed=True,
                legacy_only=False,
            ),
            STTEngineCandidate(
                engine_id="faster_whisper_small_fallback",
                engine_kind="faster_whisper",
                model_id="small",
                role="fallback",
                device_class="cpu_or_cuda_probe",
                primary_allowed=False,
                fallback_allowed=True,
                legacy_only=False,
            ),
            STTEngineCandidate(
                engine_id="vosk_small_ru_legacy",
                engine_kind="vosk",
                model_id="vosk-model-small-ru-0.22",
                role="legacy",
                device_class="cpu",
                primary_allowed=False,
                fallback_allowed=False,
                legacy_only=True,
            ),
        ),
    )
