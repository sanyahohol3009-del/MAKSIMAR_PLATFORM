from __future__ import annotations

from tools.jarvis_live_runtime.jarvis_skill_visibility import build_jarvis_skill_visibility_read_model


def test_jarvis_skill_visibility_smoke() -> None:
    payload = build_jarvis_skill_visibility_read_model()

    assert "weather_lookup" in payload["visible_tools"]
    assert "repo_search" in payload["visible_tools"]
    assert "browser_worker" in payload["visible_tools"]
    assert "external_adapter:langgraph" in payload["external_adapter_tools"]
    assert "tool_selector_agent" in payload["visible_agents"]
    assert any(path.endswith("tools/jarvis_live_runtime/read_only_tool_router.py") for path in payload["visible_skills"])
    assert payload["duplicate_tools"]
    assert payload["unknown_tools_blocked"] is True
    assert payload["semantic_dedupe_enabled"] is True
    assert "external_adapter:openai_agents_sdk" in payload["universal_registry_tools"]
