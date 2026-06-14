from tools.jarvis_live_runtime.jarvis_live_response_mode import (
    build_ollama_options,
    classify_response_mode,
)


def test_response_modes_and_num_predict_are_deterministic() -> None:
    voice_mode = classify_response_mode("ответь коротко")
    detailed_mode = classify_response_mode("распиши подробный план пошагово")
    command_mode = classify_response_mode("покажи статус")
    code_mode = classify_response_mode("pytest ошибка git")

    assert voice_mode.response_mode == "voice_mode"
    assert detailed_mode.response_mode == "detailed_mode"
    assert command_mode.response_mode == "command_mode"
    assert code_mode.response_mode == "code_mode"
    assert build_ollama_options(voice_mode) == {"num_predict": 512, "temperature": 0.8, "top_p": 0.95}
    assert build_ollama_options(detailed_mode) == {"num_predict": 640, "temperature": 0.8, "top_p": 0.95}
    assert build_ollama_options(command_mode) == {"num_predict": 256, "temperature": 0.8, "top_p": 0.95}
    assert build_ollama_options(code_mode) == {"num_predict": 384, "temperature": 0.8, "top_p": 0.95}
    assert build_ollama_options(voice_mode)["num_predict"] > 160
    assert "1-2 short spoken Russian sentences" in voice_mode.instruction
    assert "Do not repeat full identity every time" in voice_mode.instruction
    assert "короткое подтверждение" in command_mode.instruction
    assert "командами или проверками" in code_mode.instruction
