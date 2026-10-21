from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_read_model,
)


def test_runtime_model_roles_keep_14b_as_heavy_coder_only() -> None:
    read_model = build_jarvis_live_runtime_model_role_read_model()
    profiles = {profile["role_id"]: profile for profile in read_model["profiles"]}

    heavy = profiles["heavy_coder_model"]
    assert heavy["model_id"] == "jarvis:coder14b"
    assert heavy["target_model_id"] == "qwen2.5-coder:14b"
    assert heavy["role"] == "heavy_coder"
    assert heavy["load_policy"] == "load_on_demand"
    assert heavy["exclusive_gpu"] is True
    assert heavy["default_context_tokens"] == 4096
    assert heavy["max_safe_context_tokens"] == 8192
    assert heavy["agents_direct_access_allowed"] is False
    assert heavy["pc_control_allowed"] is False


def test_installed_jarvis_wrappers_are_marked_installed_not_planned() -> None:
    read_model = build_jarvis_live_runtime_model_role_read_model()
    profiles = {profile["role_id"]: profile for profile in read_model["profiles"]}

    assert profiles["jarvis_chat_model"]["model_id"] == "jarvis:chat8b"
    assert profiles["jarvis_chat_model"]["target_model_id"] == "qwen3:8b"
    assert profiles["daily_coder_model"]["model_id"] == "jarvis:coder7b"
    assert profiles["daily_coder_model"]["target_model_id"] == "qwen2.5-coder:7b"
    assert profiles["helper_input_correction_model"]["model_id"] == "jarvis:helper3b"
    assert profiles["helper_input_correction_model"]["target_model_id"] == "qwen2.5-coder:3b"
    for role_id in ("daily_coder_model", "helper_input_correction_model", "jarvis_chat_model", "heavy_coder_model"):
        assert profiles[role_id]["installed"] is True
        assert profiles[role_id]["status"] == "installed"
        assert profiles[role_id]["model_download_allowed"] is False
        assert profiles[role_id]["runtime_start_allowed"] is False


def test_helper_profile_is_correction_only_not_semantic_routing() -> None:
    profiles = {
        profile["role_id"]: profile
        for profile in build_jarvis_live_runtime_model_role_read_model()["profiles"]
    }
    helper = profiles["helper_input_correction_model"]
    assert helper["role"] == "helper_input_correction"
    assert helper["use_cases"] == (
        "STT correction", "typing correction", "input normalization", "ambiguity evidence",
    )


def test_existing_registry_resolves_swapped_heavy_profile_without_fixed_tag(monkeypatch):
    from dataclasses import replace
    from MAKSIMAR_CORE_LIB.ai_orchestration import model_profile_registry_contract as registry
    profiles=registry.build_jarvis_live_runtime_model_role_profiles()
    swapped=tuple(replace(p,model_id="fixture-next-heavy",target_model_id="fixture-next-base")
                  if p.role_id=="heavy_coder_model" else p for p in profiles)
    monkeypatch.setattr(registry,"build_jarvis_live_runtime_model_role_profiles",lambda:swapped)
    profile=registry.resolve_runtime_model_profile(role_id="heavy_coder_model")
    assert profile.model_id=="fixture-next-heavy" and profile.load_policy=="load_on_demand"
    assert registry.resolve_runtime_model_profile(model_id="fixture-next-heavy").role_id=="heavy_coder_model"


def test_unknown_model_never_resolves_to_primary():
    import pytest
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import model_role_for_model_id
    with pytest.raises(KeyError):model_role_for_model_id("fixture-unregistered")
