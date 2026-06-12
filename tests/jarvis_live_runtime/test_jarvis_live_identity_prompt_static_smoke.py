from tools.jarvis_live_runtime.jarvis_live_identity_prompt import (
    JARVIS_IDENTITY_FIRST_SENTENCE,
    build_jarvis_live_identity_prompt,
)


def test_identity_prompt_keeps_jarvis_identity_and_platform_capability_style() -> None:
    prompt = build_jarvis_live_identity_prompt("Кто ты?")
    lowered = prompt.lower()

    assert prompt.startswith("JARVIS IDENTITY PROMPT v2")
    assert JARVIS_IDENTITY_FIRST_SENTENCE in prompt
    assert "ты jarvis." in lowered
    assert "ты не jarvis-live, не qwen, не chatgpt, не alibaba" in lowered
    assert "jarvis-live — это только runtime mode" in lowered
    assert "личность одна: jarvis" in lowered
    assert "создатель и владелец проекта: александр" in lowered
    assert "жена александра: юля" in lowered
    assert "старший сын александра: максим" in lowered
    assert "младший сын александра: макар" in lowered
    assert "быстро отвечать владельцу и семье" in lowered
    assert "maksimar/jarvis" in lowered
    assert "кода" in lowered
    assert "архитектурой" in lowered
    assert "терминалом" in lowered
    assert "operator proposal" in lowered
    assert "approval" in lowered
    assert "не выдумывай состояние проекта" in lowered
    assert "canonical path" in lowered
    assert "доступные capabilities платформы" in lowered
    assert "control-plane" in lowered
    assert "параллельный brain/router/server/runtime" in lowered
    assert "быстрый режим" in lowered
    assert "маленькую модель" in lowered
    assert "operator trace" in lowered
    assert "voice identity layer" in lowered
    assert "не должен сам выполнять распознавание голоса" in lowered
    assert "pc control currently disabled" not in lowered
    assert "не управляй пк" not in lowered
    assert "watchdog" not in lowered
    assert "supervisor" not in lowered
