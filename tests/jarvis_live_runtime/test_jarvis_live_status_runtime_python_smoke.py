from pathlib import Path


def test_status_source_prints_runtime_python_and_live_voice_state() -> None:
    source = Path("tools/jarvis_live_runtime/jarvis_live_status.py").read_text(
        encoding="utf-8"
    )

    assert "runtime_python=" in source
    assert "owner_detected=" in source
    assert "always_listening_enabled=" in source
    assert "latest_transcript=" in source
    assert "latest_voice_reply=" in source
    assert "pc_control_allowed=false" in source
