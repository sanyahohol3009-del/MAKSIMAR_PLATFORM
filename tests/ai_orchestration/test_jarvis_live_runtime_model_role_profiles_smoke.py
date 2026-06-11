from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_read_model,
    select_jarvis_live_model_role,
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
    assert profiles["helper_classifier_model"]["model_id"] == "jarvis:helper3b"
    assert profiles["helper_classifier_model"]["target_model_id"] == "qwen2.5-coder:3b"
    for role_id in ("daily_coder_model", "helper_classifier_model", "jarvis_chat_model", "heavy_coder_model"):
        assert profiles[role_id]["installed"] is True
        assert profiles[role_id]["status"] == "installed"
        assert profiles[role_id]["model_download_allowed"] is False
        assert profiles[role_id]["runtime_start_allowed"] is False


def test_runtime_model_role_selection_routes_without_direct_execution() -> None:
    assert select_jarvis_live_model_role("обычный разговор")["selected_model_role"] == "jarvis_chat_model"
    assert select_jarvis_live_model_role("pytest ошибка в тесте")["selected_model_role"] == "daily_coder_model"
    assert select_jarvis_live_model_role("сложный architecture traceback")["selected_model_role"] == "heavy_coder_model"
    assert select_jarvis_live_model_role("сделай summary")["selected_model_role"] == "helper_classifier_model"
    classified = select_jarvis_live_model_role("Классифицируй одним словом: исправить traceback pytest")
    assert classified["selected_model_role"] == "helper_classifier_model"
    assert classified["model_id"] == "jarvis:helper3b"
    assert select_jarvis_live_model_role("Объясни BrokenPipeError в Python http.server")["model_id"] == "jarvis:coder7b"
    assert select_jarvis_live_model_role("Сделай architecture check PC-control approval gate")["model_id"] == "jarvis:coder14b"

    pc_action = select_jarvis_live_model_role("открой браузер")
    assert pc_action["route_reason"] == "pc_action_request_proposal_only"
    assert pc_action["direct_execution_allowed"] is False
    assert pc_action["pc_control_allowed"] is False
