from __future__ import annotations

from dataclasses import dataclass


DETAILED_TRIGGERS = ("подробно", "распиши", "план", "объясни", "детально", "пошагово")
COMMAND_TRIGGERS = ("открой", "запусти", "найди", "покажи", "проверь")
CODE_TRIGGERS = ("код", "ошибка", "тест", "команда", "терминал", "pytest", "git")


@dataclass(frozen=True)
class JarvisLiveResponseMode:
    response_mode: str
    ollama_num_predict: int
    ollama_temperature: float
    ollama_top_p: float
    instruction: str

    def to_read_model(self) -> dict[str, object]:
        return {
            "response_mode": self.response_mode,
            "ollama_num_predict": self.ollama_num_predict,
            "ollama_temperature": self.ollama_temperature,
            "ollama_top_p": self.ollama_top_p,
            "instruction": self.instruction,
            "pc_control_allowed": False,
        }


def classify_response_mode(transcript: str) -> JarvisLiveResponseMode:
    lowered = transcript.casefold()
    if _contains_any(lowered, DETAILED_TRIGGERS):
        return JarvisLiveResponseMode(
            response_mode="detailed_mode",
            ollama_num_predict=640,
            ollama_temperature=0.8,
            ollama_top_p=0.95,
            instruction=(
                "Режим detailed_mode: дай более длинный структурированный ответ. "
                "PC control disabled."
            ),
        )
    if _contains_any(lowered, COMMAND_TRIGGERS):
        return JarvisLiveResponseMode(
            response_mode="command_mode",
            ollama_num_predict=256,
            ollama_temperature=0.8,
            ollama_top_p=0.95,
            instruction=(
                "Режим command_mode: дай короткое подтверждение или preview. "
                "Не выполняй действия, PC control disabled."
            ),
        )
    if _contains_any(lowered, CODE_TRIGGERS):
        return JarvisLiveResponseMode(
            response_mode="code_mode",
            ollama_num_predict=384,
            ollama_temperature=0.8,
            ollama_top_p=0.95,
            instruction=(
                "Режим code_mode: дай структурированный ответ с командами или проверками, "
                "кратко, но не чрезмерно коротко. PC control disabled."
            ),
        )
    return JarvisLiveResponseMode(
        response_mode="voice_mode",
        ollama_num_predict=512,
        ollama_temperature=0.8,
        ollama_top_p=0.95,
        instruction=(
            "Answer in 1-2 short spoken Russian sentences. Do not repeat full identity "
            "every time. Do not give long intro. Sound alive and direct. PC control disabled."
        ),
    )


def build_ollama_options(response_mode: JarvisLiveResponseMode) -> dict[str, object]:
    return {
        "num_predict": response_mode.ollama_num_predict,
        "temperature": response_mode.ollama_temperature,
        "top_p": response_mode.ollama_top_p,
    }


def _contains_any(text: str, triggers: tuple[str, ...]) -> bool:
    return any(trigger in text for trigger in triggers)
