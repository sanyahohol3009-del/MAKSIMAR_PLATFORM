from __future__ import annotations

from tools.jarvis_live_runtime.voice_response_cleaner import build_output_channels


def test_spoken_output_cleaner_hides_technical_fields_but_keeps_visible_text() -> None:
    payload = build_output_channels(
        "selected_capability_id=close_opera {\"route\":\"DIRECT_OWNER_PC_ACTION\"} Закрываю окно оперы.",
        mode="command",
    )

    assert "selected_capability_id=close_opera" in payload["visible_text"]
    assert "selected_capability_id=close_opera" not in payload["spoken_text"]
    assert "DIRECT_OWNER_PC_ACTION" not in payload["spoken_text"]
    assert "Закрываю окно оперы" in payload["spoken_text"]


def test_spoken_output_cleaner_keeps_symbols_in_code_mode() -> None:
    payload = build_output_channels("print(x == 1):", mode="code")

    assert payload["spoken_text"] == "print(x == 1):"
