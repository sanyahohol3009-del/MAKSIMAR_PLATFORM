from __future__ import annotations

from dataclasses import dataclass


PROJECT_TRIGGERS = (
    "проект", "джарвис", "jarvis", "код", "pytest", "git", "файл", "архитектур", "слой",
)
ACTION_TRIGGERS = (
    "открой", "запусти", "включи", "выключи", "удали", "снеси", "перемести", "создай",
)
GAME_TRIGGERS = ("игра", "игровой", "minecraft", "roblox", "steam")
SMART_HOME_TRIGGERS = ("свет", "лампа", "температура", "розетка", "дом")


@dataclass(frozen=True)
class VoiceResponseModePolicy:
    response_mode: str
    max_sentences: int
    allow_template_confirmation: bool
    approval_required: bool
    pc_control_allowed: bool
    direct_execution_allowed: bool

    def __post_init__(self) -> None:
        allowed = {
            "ordinary_chat",
            "project_engineer",
            "approval_required",
            "game_mode",
            "child_game_mode",
            "smart_home",
        }
        if self.response_mode not in allowed:
            raise ValueError(f"unsupported response_mode={self.response_mode}")
        if self.max_sentences < 1:
            raise ValueError("max_sentences must be positive")
        if self.pc_control_allowed:
            raise ValueError("pc_control_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_read_model(self) -> dict[str, object]:
        return {
            "response_mode": self.response_mode,
            "max_sentences": self.max_sentences,
            "allow_template_confirmation": self.allow_template_confirmation,
            "approval_required": self.approval_required,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


def classify_voice_response_mode(user_text: str, speaker_id: str = "owner") -> VoiceResponseModePolicy:
    lowered = (user_text or "").casefold()

    if speaker_id in {"maxim", "makar", "child"} and any(t in lowered for t in GAME_TRIGGERS):
        return VoiceResponseModePolicy("child_game_mode", 2, False, False, False, False)

    if any(t in lowered for t in ACTION_TRIGGERS):
        return VoiceResponseModePolicy("approval_required", 2, True, True, False, False)

    if any(t in lowered for t in SMART_HOME_TRIGGERS):
        return VoiceResponseModePolicy("smart_home", 1, True, True, False, False)

    if any(t in lowered for t in GAME_TRIGGERS):
        return VoiceResponseModePolicy("game_mode", 2, False, False, False, False)

    if any(t in lowered for t in PROJECT_TRIGGERS):
        return VoiceResponseModePolicy("project_engineer", 4, False, False, False, False)

    return VoiceResponseModePolicy("ordinary_chat", 2, False, False, False, False)
