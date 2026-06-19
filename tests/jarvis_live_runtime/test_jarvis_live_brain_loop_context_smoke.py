from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_brain_context,
    build_jarvis_live_project_status_read_model,
    build_project_workspace_read_model,
    read_file_outline,
    read_file_snippet,
    repo_git_status,
    repo_import_graph,
    repo_search,
    repo_tree,
)


def test_brain_context_includes_session_history_project_boundaries() -> None:
    state = {
        "recent_turns": [
            {"role": "user", "text": "Джарвис, кто ты?"},
            {"role": "assistant", "text": "Я JARVIS."},
        ],
        "rolling_summary": "owner asked identity",
        "active_topics": ["identity"],
    }

    context = build_jarvis_live_brain_context("Что я спрашивал до этого?", state)
    read_model = context.to_read_model()
    prompt = context.to_prompt()

    assert read_model["recent_turn_count"] == 2
    assert read_model["pc_control_allowed"] is False
    assert read_model["canonical_memory_write_allowed"] is False
    assert "RECENT_SESSION_TURNS" in prompt
    assert "JARVIS_PERSONALITY_CANONICAL_POLICY_V1" in prompt
    assert "RESPONSE_MODE: conversation" in prompt
    assert "THINKING_FREEDOM" in prompt
    assert "ACTION_SAFETY" in prompt
    assert "ANTI_TEMPLATE_RULES" in prompt
    assert "Скажи, что нужно" not in prompt
    assert "ROLLING_SESSION_SUMMARY" in prompt
    assert "RETRIEVED_LONG_TERM_MEMORY" not in prompt


def test_fast_conversation_uses_session_memory_without_deep_retrieval() -> None:
    state = {
        "recent_turns": [
            {"role": "user", "text": "Мне нравится спокойный стиль общения."},
            {"role": "assistant", "text": "Понял, буду отвечать спокойно."},
        ],
        "rolling_summary": "owner prefers calm conversation",
        "active_topics": ["conversation"],
    }

    context = build_jarvis_live_brain_context("Джарвис, просто поговори со мной.", state)
    read_model = context.to_read_model()
    prompt = context.to_prompt()

    assert read_model["request_route"] == "conversation"
    assert read_model["route_mode"] == "FAST"
    assert read_model["retrieval_mode"] == "session_only"
    assert read_model["selected_model_role"]["model_id"] == "jarvis:chat8b"
    assert "session_memory" in read_model["retrieval_surfaces_used"]
    assert "local_chat_memory" in read_model["retrieval_surfaces_used"]
    assert read_model["retrieved_snippet_count"] == 0
    assert "RECENT_SESSION_TURNS" in prompt
    assert "JARVIS_PERSONALITY_CANONICAL_POLICY_V1" in prompt
    assert "RESPONSE_MODE: conversation" in prompt
    assert "THINKING_FREEDOM" in prompt
    assert "ACTION_SAFETY" in prompt
    assert "ANTI_TEMPLATE_RULES" in prompt
    assert "Скажи, что нужно" not in prompt
    assert "FAST_RESPONSE_RULES" not in prompt
    assert "owner prefers calm conversation" in prompt
    assert "STYLE_MEMORY_ANSWER_RULES" not in prompt
    assert "RETRIEVED_LONG_TERM_MEMORY" not in prompt
    assert read_model["pc_control_allowed"] is False


def test_project_status_read_model_is_read_only() -> None:
    payload = build_jarvis_live_project_status_read_model()

    assert payload["read_only"] is True
    assert payload["pc_control_allowed"] is False
    assert payload["canonical_memory_write_allowed"] is False
    assert "runtime_history_store" in payload["project_status"]
    assert "project_workspace_read_enabled=true" in payload["project_status"]
    assert "project_file_read_enabled=true" in payload["project_status"]
    assert "direct_execution_allowed=false" in payload["project_status"]


def test_project_visibility_reads_tree_and_bounded_file_snippets() -> None:
    context = build_jarvis_live_brain_context(
        "Джарвис, покажи структуру проекта, дерево файлов и ядро terminal chat",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
    )
    read_model = context.to_read_model()
    prompt = context.to_prompt()

    assert read_model["route_mode"] == "DEEP"
    assert read_model["retrieval_mode"] == "deep_memory"
    assert "project_workspace_read_model" in read_model["retrieval_surfaces_used"]
    assert "project_workspace_read_enabled" in str(read_model["dangerous_mutation_flags"]) or "project_workspace" in read_model["memory_truth_contract"]
    assert "project_workspace_read_model" in prompt
    assert "project_file_snippet:" in prompt
    assert "tools/jarvis_live_runtime/jarvis_live_brain_loop.py" in prompt
    assert "canonical_write_allowed=false" in prompt
    assert "direct_execution_allowed=false" in prompt


def test_project_workspace_read_model_is_dynamic_and_read_only() -> None:
    model = build_project_workspace_read_model()

    assert model["project_root"]
    assert "git_branch" in model
    assert "git_head" in model
    assert "git_status_short" in model
    assert isinstance(model["dirty_files"], tuple)
    assert isinstance(model["untracked_files"], tuple)
    assert isinstance(model["staged_files"], tuple)
    assert model["tracked_file_count"] > 0
    assert model["tracked_files_by_page"]["files"]
    assert model["top_level_tree"]["entries"]
    assert "JARVIS terminal runtime" in model["domain_groups"]
    assert model["read_only"] is True
    assert model["direct_execution_allowed"] is False
    assert model["canonical_write_allowed"] is False
    assert model["pc_control_allowed"] is False


def test_project_read_tools_are_bounded_and_safe() -> None:
    git_status = repo_git_status()
    tree = repo_tree(depth=2, max_entries=20)
    search = repo_search("memory", max_results=5)
    snippet = read_file_snippet("tools/jarvis_live_runtime/jarvis_live_brain_loop.py", page=1)
    denied = read_file_snippet("../outside.py", page=1)
    binary_denied = read_file_snippet("fake.pyc", page=1)
    outline = read_file_outline("tools/jarvis_live_runtime/jarvis_live_brain_loop.py")
    imports = repo_import_graph("tools/jarvis_live_runtime/jarvis_live_brain_loop.py", max_edges=10)

    assert "branch" in git_status
    assert tree["entry_count"] <= 20
    assert search["result_count"] <= 5
    assert snippet["allowed"] is True
    assert any(line.startswith("1:") for line in snippet["snippet"])
    assert denied["allowed"] is False
    assert binary_denied["allowed"] is False
    assert outline["allowed"] is True
    assert "json" in outline["imports"]
    assert outline["functions"]
    assert imports["edge_count"] <= 10
