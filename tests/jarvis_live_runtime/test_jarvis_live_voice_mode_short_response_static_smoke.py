from tools.jarvis_live_runtime.jarvis_live_response_mode import (
    build_ollama_options,
    classify_response_mode,
)


def test_voice_mode_is_short_and_spoken() -> None:
    mode = classify_response_mode("ты здесь")

    assert mode.response_mode == "voice_mode"
    assert build_ollama_options(mode) == {"num_predict": 60, "temperature": 0.35}
    assert "1-2 short spoken Russian sentences" in mode.instruction
    assert "Do not repeat full identity every time" in mode.instruction
    assert "Sound alive and direct" in mode.instruction
