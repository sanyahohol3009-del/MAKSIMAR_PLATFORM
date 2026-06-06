from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.screen_vision_candidate_contract import (
    SCREEN_VISION_CANDIDATE_ROLES,
    SCREEN_VISION_SOURCE_SURFACES,
    ScreenVisionCandidateContract,
    build_screen_vision_candidate_contract,
)


def test_screen_vision_candidate_contract_is_read_only() -> None:
    contract = build_screen_vision_candidate_contract()
    read_model = contract.to_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["candidate_role_ids"] == SCREEN_VISION_CANDIDATE_ROLES
    assert read_model["source_surfaces"] == SCREEN_VISION_SOURCE_SURFACES
    assert read_model["screen_capture_runtime_enabled"] is False
    assert read_model["ocr_runtime_enabled"] is False
    assert read_model["pixel_decode_allowed"] is False
    assert read_model["screenshot_allowed"] is False
    assert read_model["screen_recording_allowed"] is False
    assert read_model["mouse_control_allowed"] is False
    assert read_model["keyboard_control_allowed"] is False
    assert read_model["app_control_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False


def test_screen_vision_candidate_contract_rejects_enabled_flags() -> None:
    base = build_screen_vision_candidate_contract()

    with pytest.raises(ValueError, match="must remain disabled"):
        ScreenVisionCandidateContract(
            contract_id="screen_vision_candidate_contract_v0_1",
            candidate_roles=base.candidate_roles,
            source_surfaces=base.source_surfaces,
            screenshot_allowed=True,
        )

    with pytest.raises(ValueError, match="must remain disabled"):
        ScreenVisionCandidateContract(
            contract_id="screen_vision_candidate_contract_v0_1",
            candidate_roles=base.candidate_roles,
            source_surfaces=base.source_surfaces,
            pc_control_allowed=True,
        )


def test_screen_vision_candidate_contract_post_init_invariants_are_active() -> None:
    base = build_screen_vision_candidate_contract()

    with pytest.raises(ValueError, match="contract_id"):
        ScreenVisionCandidateContract(
            contract_id="",
            candidate_roles=base.candidate_roles,
            source_surfaces=base.source_surfaces,
        )

    with pytest.raises(ValueError, match="candidate_roles"):
        ScreenVisionCandidateContract(
            contract_id="screen_vision_candidate_contract_v0_1",
            candidate_roles=base.candidate_roles[:-1],
            source_surfaces=base.source_surfaces,
        )

