from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    _looks_like_incomplete_model_output,
)


def test_generation_incomplete_guard_detects_live_broken_tails() -> None:
    broken_samples = (
        "Активен мост Windows для ввода",
        "2. Голосовые команды:\n - Режим",
        "Контроллеры:\n - Здоровье:",
        "Запрос на включение в будущем (",
        "TTS профиль `kokoro_bm_lewis_speed_1",
    )

    for sample in broken_samples:
        incomplete, reason = _looks_like_incomplete_model_output(
            sample,
            grounded_answer=True,
        )
        assert incomplete is True
        assert reason.startswith("model_response_looks_incomplete:")


def test_generation_incomplete_guard_allows_complete_grounded_answer() -> None:
    complete = (
        "Typed Windows bridge активен. Полный microphone/STT/live loop не запущен. "
        "TTS output разрешён. PC-control выключен."
    )

    incomplete, reason = _looks_like_incomplete_model_output(
        complete,
        grounded_answer=True,
    )

    assert incomplete is False
    assert reason == ""
