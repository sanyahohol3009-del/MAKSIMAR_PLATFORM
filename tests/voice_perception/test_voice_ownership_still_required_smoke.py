from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception import (
    build_perception_policy_contract,
)


def test_voice_ownership_still_required_for_any_action_path() -> None:
    read_model = build_perception_policy_contract().to_read_model()

    assert read_model["owner_voice_gate_required"] is True
    assert read_model["voice_ownership_still_required"] is True
    assert read_model["unauthenticated_voice_may_execute_actions"] is False
    assert read_model["child_family_mobile_voices_may_bypass_approval"] is False
    assert read_model["approval_required_for_actions"] is True
