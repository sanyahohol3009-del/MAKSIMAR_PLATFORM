from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_model_conductor_contract import (
    JarvisLiveModelConductorContract,
    JarvisLiveModelRole,
    build_jarvis_live_model_conductor_contract,
)
from MAKSIMAR_CORE_LIB.real_voice_runtime.jarvis_live_disabled_gate_contract import (
    JarvisLiveReadinessFlags,
    build_jarvis_live_disabled_gate_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_readiness_summary_builder import (
    build_jarvis_live_readiness_summary,
)


def test_jarvis_live_is_disabled_by_default() -> None:
    gate = build_jarvis_live_disabled_gate_contract()

    assert gate.jarvis_live_enabled is False
    assert gate.live_runtime_ready is False
    assert gate.readiness.all_ready is False
    assert "jarvis_live_disabled_by_default" in gate.denied_reasons


def test_jarvis_live_voice_audio_runtime_surfaces_are_disabled() -> None:
    gate = build_jarvis_live_disabled_gate_contract()
    read_model = gate.to_read_model()

    assert read_model["microphone_enabled"] is False
    assert read_model["stt_runtime_enabled"] is False
    assert read_model["tts_playback_enabled"] is False
    assert read_model["wake_word_enabled"] is False


def test_jarvis_live_model_download_and_runtime_start_are_blocked() -> None:
    conductor = build_jarvis_live_model_conductor_contract()
    gate = build_jarvis_live_disabled_gate_contract()

    assert conductor.model_download_allowed is False
    assert conductor.runtime_start_allowed is False
    assert gate.model_download_allowed is False
    assert gate.runtime_start_allowed is False
    assert gate.network_access_allowed is False


def test_jarvis_live_direct_execution_shell_core_write_and_app_control_are_blocked() -> None:
    conductor = build_jarvis_live_model_conductor_contract()

    assert conductor.direct_execution_allowed is False
    assert conductor.direct_shell_allowed is False
    assert conductor.direct_core_write_allowed is False
    assert conductor.direct_app_control_allowed is False
    assert conductor.dashboard_execution_allowed is False


def test_jarvis_live_dashboard_summary_is_read_only_and_lists_next_batches() -> None:
    summary = build_jarvis_live_readiness_summary()

    assert summary["status"] == "disabled_contract_entry_only"
    assert summary["enabled"] is False
    assert summary["model_download_allowed"] is False
    assert summary["runtime_start_allowed"] is False
    assert summary["direct_execution_allowed"] is False
    assert summary["dashboard_execution_allowed"] is False
    assert summary["dashboard_safe"] is True
    assert summary["read_only"] is True
    assert "security_action_allowlist_binding" in summary["required_next_batches"]
    assert "dashboard_observability_integration" in summary["required_next_batches"]


def test_jarvis_live_references_existing_architecture_without_duplication() -> None:
    conductor = build_jarvis_live_model_conductor_contract()
    read_model = conductor.to_read_model()

    assert "AI_SERVICES" in read_model["referenced_architecture_surfaces"]
    assert "MAKSIMAR_CORE_LIB/ai_orchestration" in read_model[
        "referenced_architecture_surfaces"
    ]
    assert "MAKSIMAR_SERVER/CONTROL_PLANE/ai_router_binding" in read_model[
        "referenced_architecture_surfaces"
    ]
    assert "MAKSIMAR_CORE_LIB/workers_registry" in read_model[
        "referenced_architecture_surfaces"
    ]
    assert "MAKSIMAR_CORE_LIB/execution_control" in read_model[
        "referenced_architecture_surfaces"
    ]
    assert "MAKSIMAR_CORE_LIB/security_layer" in read_model[
        "referenced_architecture_surfaces"
    ]
    assert read_model["duplicated_registry_surfaces"] == ()


def test_jarvis_live_model_roles_are_present_and_disabled() -> None:
    conductor = build_jarvis_live_model_conductor_contract()
    role_names = {binding.role.value for binding in conductor.role_bindings}

    assert role_names == {role.value for role in JarvisLiveModelRole}
    assert all(binding.proposal_only is True for binding in conductor.role_bindings)
    assert all(binding.enabled is False for binding in conductor.role_bindings)


def test_jarvis_live_conductor_rejects_execution_enablement() -> None:
    base = build_jarvis_live_model_conductor_contract()

    with pytest.raises(ValueError, match="direct_execution_allowed"):
        JarvisLiveModelConductorContract(
            contract_id="bad_jarvis_live_model_conductor_contract",
            role_bindings=base.role_bindings,
            referenced_architecture_surfaces=base.referenced_architecture_surfaces,
            duplicated_registry_surfaces=(),
            proposal_only=True,
            disabled_by_default=True,
            direct_execution_allowed=True,
            direct_shell_allowed=False,
            direct_core_write_allowed=False,
            direct_app_control_allowed=False,
            model_download_allowed=False,
            runtime_start_allowed=False,
            dashboard_execution_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_jarvis_live_readiness_requires_all_gates_before_runtime_ready() -> None:
    readiness = JarvisLiveReadinessFlags(
        voice_gate_ready=True,
        owner_identity_gate_ready=True,
        action_allowlist_ready=True,
        approval_binding_ready=True,
        audit_binding_ready=True,
        dashboard_status_ready=True,
        model_storage_boundary_ready=True,
        runtime_vendor_boundary_ready=True,
    )

    assert readiness.all_ready is True
    assert readiness.missing_gate_names == ()
    assert build_jarvis_live_disabled_gate_contract().readiness.all_ready is False
