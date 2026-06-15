from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception.voice_perception_status_read_model import (
    build_voice_perception_status_read_model,
)


def test_voice_message_is_not_command_without_explicit_intent() -> None:
    read_model = build_voice_perception_status_read_model().to_read_model()

    assert read_model["voice_message_not_command_without_intent"] is True
    assert read_model["text_intent_only"] is True
    assert read_model["action_execution_allowed"] is False
    assert read_model["proposal_only"] is True
