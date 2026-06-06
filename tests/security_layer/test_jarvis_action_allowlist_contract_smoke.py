from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.security_layer.jarvis_action_allowlist_contract import (
    ALLOWED_JARVIS_ACTION_CANDIDATES,
    FORBIDDEN_JARVIS_ACTIONS,
    JarvisAllowedActionCandidate,
    assert_action_not_forbidden,
    build_jarvis_action_allowlist_contract,
    is_action_allowed_candidate,
)


def test_jarvis_action_allowlist_candidates_are_exact_and_not_executable() -> None:
    read_model = build_jarvis_action_allowlist_contract().to_read_model()

    assert read_model["allowed_action_ids"] == (
        "open_youtube",
        "open_browser",
        "open_project_status",
        "read_test_status",
        "volume_up",
        "volume_down",
        "pause_media",
        "resume_media",
    )
    assert read_model["allowed_action_ids"] == ALLOWED_JARVIS_ACTION_CANDIDATES
    assert read_model["forbidden_actions"] == FORBIDDEN_JARVIS_ACTIONS
    assert read_model["execution_enabled"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["pc_control_allowed"] is False

    for candidate in read_model["allowed_action_candidates"]:
        assert candidate["owner_command_required"] is True
        assert candidate["approval_required"] is True
        assert candidate["audit_required"] is True
        assert candidate["preview_required"] is True
        assert candidate["allowlist_required"] is True
        assert candidate["execution_enabled"] is False
        assert candidate["runtime_start_allowed"] is False
        assert candidate["pc_control_allowed"] is False


def test_forbidden_actions_are_rejected() -> None:
    for action_id in FORBIDDEN_JARVIS_ACTIONS:
        with pytest.raises(ValueError, match="forbidden JARVIS action"):
            assert_action_not_forbidden(action_id)
        with pytest.raises(ValueError, match="forbidden JARVIS action"):
            is_action_allowed_candidate(action_id)


def test_invalid_action_id_raises_value_error() -> None:
    with pytest.raises(ValueError, match="action_id"):
        is_action_allowed_candidate("")
    with pytest.raises(ValueError, match="unsupported value"):
        JarvisAllowedActionCandidate(action_id="unknown_action")


def test_allowlist_post_init_invariants_are_active() -> None:
    with pytest.raises(ValueError, match="must remain required"):
        JarvisAllowedActionCandidate(
            action_id="open_youtube",
            approval_required=False,
        )
    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisAllowedActionCandidate(
            action_id="open_youtube",
            execution_enabled=True,
        )

