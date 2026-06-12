from tools.jarvis_live_runtime.jarvis_live_identity_prompt import (
    JARVIS_IDENTITY_FIRST_SENTENCE,
    build_jarvis_live_identity_prompt,
)


def test_identity_prompt_keeps_jarvis_identity_and_pc_control_disabled() -> None:
    prompt = build_jarvis_live_identity_prompt("Кто ты?")
    lowered = prompt.lower()

    assert prompt.startswith("Я JARVIS, локальный голосовой помощник Александра.")
    assert JARVIS_IDENTITY_FIRST_SENTENCE in prompt
    assert "qwen является только backend-моделью" in lowered
    assert "jarvis live является только внутренним именем runtime" in lowered
    assert "никогда не называй себя jarvis live" in lowered
    assert "никогда не представляйся qwen, alibaba, chatgpt" in lowered
    assert "не просто чат" in lowered
    assert "maksimar/jarvis" in lowered
    assert "кода" in lowered
    assert "диагностики" in lowered
    assert "планов" in lowered
    assert "локальной системы" in lowered
    assert "pc control currently disabled" in lowered
