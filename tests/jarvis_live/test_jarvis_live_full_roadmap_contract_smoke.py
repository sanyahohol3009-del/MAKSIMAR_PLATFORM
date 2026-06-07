from __future__ import annotations

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_full_roadmap_contract import (
    DRIFT_COMMAND_HINT,
    FULL_AUTO_COMMAND_HINT,
    XRAY_COMMAND_HINT,
    build_jarvis_live_full_roadmap_read_model,
    get_jarvis_live_batch,
    list_jarvis_live_batches,
)


def test_jarvis_live_full_roadmap_has_exact_jl0_to_jl14_batches() -> None:
    batches = list_jarvis_live_batches()

    assert len(batches) == 15
    assert tuple(batch.batch_id for batch in batches) == tuple(
        f"JL-{index}" for index in range(15)
    )


def test_jarvis_live_key_batches_have_expected_gate_semantics() -> None:
    assert get_jarvis_live_batch("JL-4").download_allowed is False

    jl10 = get_jarvis_live_batch("JL-10")
    assert jl10.download_allowed is True
    assert jl10.runtime_allowed is False
    assert set(jl10.depends_on) == {"JL-4", "JL-9"}

    jl11 = get_jarvis_live_batch("JL-11")
    assert jl11.voice_allowed is True
    assert jl11.pc_control_allowed is False

    jl14 = get_jarvis_live_batch("JL-14")
    assert jl14.pc_control_allowed is False
    assert jl14.runtime_allowed is False
    assert "allowlist" in jl14.status_rule
    assert "approval" in jl14.status_rule
    assert "audit" in jl14.status_rule


def test_jarvis_live_full_roadmap_read_model_is_read_only_and_has_command_hints() -> None:
    read_model = build_jarvis_live_full_roadmap_read_model()

    assert read_model["read_only"] is True
    assert read_model["runtime_start_allowed_now"] is False
    assert read_model["model_download_allowed_now"] is True
    assert read_model["voice_allowed_now"] is False
    assert read_model["pc_control_allowed_now"] is False
    assert read_model["xray_command_hint"] == XRAY_COMMAND_HINT
    assert read_model["drift_command_hint"] == DRIFT_COMMAND_HINT
    assert read_model["full_auto_command_hint"] == FULL_AUTO_COMMAND_HINT
