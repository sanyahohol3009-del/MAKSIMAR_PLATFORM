from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_voice_status_panel_contract import (
    BLOCKED_VOICE_PANEL_ACTIONS,
    JarvisVoiceStatusPanelContract,
    build_jarvis_voice_status_panel_read_model,
)
from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_voice_status_read_model import (
    build_jarvis_live_voice_status_read_model,
)


def test_jarvis_voice_status_panel_is_read_only_dashboard_safe() -> None:
    panel = build_jarvis_voice_status_panel_read_model(
        build_jarvis_live_voice_status_read_model()
    )

    assert panel["read_only"] is True
    assert panel["dashboard_safe"] is True
    assert panel["voice_runtime_enabled"] is False
    assert panel["audio_runtime_enabled"] is False
    assert panel["dashboard_execution_allowed"] is False
    assert panel["microphone_toggle_allowed"] is False
    assert panel["stt_toggle_allowed"] is False
    assert panel["tts_toggle_allowed"] is False
    assert panel["wake_word_toggle_allowed"] is False
    assert panel["pc_control_allowed"] is False
    assert panel["blocked_actions"] == BLOCKED_VOICE_PANEL_ACTIONS


def test_jarvis_voice_status_panel_rejects_enabled_flags() -> None:
    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisVoiceStatusPanelContract(
            panel_id="jarvis_voice_status_panel",
            panel_title="JARVIS-LIVE Voice Status",
            blocked_actions=BLOCKED_VOICE_PANEL_ACTIONS,
            blocked_reason="blocked",
            dashboard_execution_allowed=True,
        )

    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisVoiceStatusPanelContract(
            panel_id="jarvis_voice_status_panel",
            panel_title="JARVIS-LIVE Voice Status",
            blocked_actions=BLOCKED_VOICE_PANEL_ACTIONS,
            blocked_reason="blocked",
            microphone_toggle_allowed=True,
        )

