from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tools.jarvis_live_runtime import jarvis_skill_visibility as visibility
from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter
from MAKSIMAR_CORE_LIB.action_library_adapters import external_tool_library_adapter as external
from tools.jarvis_live_runtime.jarvis_skill_visibility import (
    build_jarvis_skill_visibility_read_model,
    select_skills_for_tools,
)


@pytest.fixture(autouse=True)
def controlled_visibility_inputs(monkeypatch, tmp_path):
    """Synthetic read-model inputs; these tests do not assert live availability."""
    catalog = dict.fromkeys(("read_tools", "proposal_tools", "memory_surfaces",
        "project_repo_read_only_tools", "memory_history_read_only_tools",
        "retrieval_read_only_tools", "model_status_read_only_tools"), ())
    catalog["read_tools"] = ("weather_lookup", "repo_search")
    monkeypatch.setattr(visibility, "build_jarvis_live_tool_catalog_read_model", lambda: catalog)
    monkeypatch.setattr(visibility, "build_jarvis_live_memory_federation_status", lambda: {})
    libraries = dict.fromkeys(("packages", "package_names", "available_package_names", "agents",
        "skills_rag", "tools_browser", "categories", "probe_reports_read"), ())
    monkeypatch.setattr(visibility, "build_runtime_library_store_read_model", lambda: libraries)
    probe = {"runtime_python": "synthetic-test-only", "probe_results": tuple({
        "package_name": manifest.package_name, "import_name": manifest.module_import_name,
        "installed": True, "import_probe_passed": True, "errors": (),
        "runtime_capability_verified": False,
    } for manifest in external.load_external_tool_manifests())}
    monkeypatch.setattr(visibility, "build_jarvis_external_adapter_visibility_read_model",
        lambda: external.build_jarvis_external_adapter_visibility_read_model(probe_read_model=probe))
    monkeypatch.setattr(visibility, "_SKILL_SCAN_ROOTS", (tmp_path,))
    monkeypatch.setattr(visibility, "PROJECT_ROOT", tmp_path)


def test_jarvis_skill_visibility_smoke() -> None:
    payload = build_jarvis_skill_visibility_read_model()

    assert "weather_lookup" in payload["visible_tools"]
    assert "repo_search" in payload["visible_tools"]
    assert "browser_worker" in payload["visible_tools"]
    assert "external_adapter:langgraph" in payload["external_adapter_tools"]
    assert "external_adapter:autogen_agentchat" in payload["external_adapter_tools"]
    assert "external_adapter:autogen_ext" in payload["external_adapter_tools"]
    assert "tool_selector_agent" in payload["visible_agents"]
    assert all(not path.endswith("tools/jarvis_live_runtime/read_only_tool_router.py") for path in payload["visible_skills"])
    assert payload["duplicate_tools"]
    assert payload["unknown_tools_blocked"] is True
    assert payload["semantic_dedupe_enabled"] is True
    assert "external_adapter:openai_agents_sdk" in payload["universal_registry_tools"]


def test_n8n_authoring_skills_are_private_to_automation_organ() -> None:
    payload = build_jarvis_skill_visibility_read_model()
    profile = payload["skill_execution_profiles"]["automation_n8n"]
    assert profile["organ_id"] == "automation"
    assert "using-n8n-skills-official" in profile["bounded_skill_ids"]
    assert profile["bounded_skill_ids"] == (
        "using-n8n-skills-official", "n8n-workflow-lifecycle-official",
        "n8n-node-configuration-official", "n8n-agents-official", "n8n-extending-mcp-official",
    )
    assert "using-n8n-skills-official" not in select_skills_for_tools(("repo_search",), ())
    selected = select_skills_for_tools(("workflow_automation:n8n",), ())
    assert selected == ("automation_n8n",)
    assert profile["provider_policy_evidence_owned_by_host"] is True
    assert profile["direct_execution_allowed"] is False


def test_private_skill_compatibility_resolves_current_canonical_reader_lazily(monkeypatch):
    selected = ("n8n-agents-official", "n8n-extending-mcp-official")
    for marker in ({"canonical": "first"}, {"canonical": "renewed"}):
        calls = []
        def reader(value):
            assert value is selected
            calls.append(value)
            return marker
        monkeypatch.setattr(n8n_adapter, "load_automation_n8n_private_skill_context", reader)
        assert visibility.load_automation_n8n_private_skill_context(selected) is marker
        assert calls == [selected]
    # The compatibility import stays inside the function, avoiding an eager cycle.
    module = ast.parse(Path(visibility.__file__).read_text(encoding="utf-8"))
    assert not any(isinstance(node, ast.ImportFrom) and node.module == n8n_adapter.__name__
                   for node in module.body)
    shim = next(node for node in module.body if isinstance(node, ast.FunctionDef)
                and node.name == "load_automation_n8n_private_skill_context")
    assert any(isinstance(node, ast.ImportFrom) and node.module == n8n_adapter.__name__
               for node in shim.body)


def test_private_skill_compatibility_preserves_reader_failure(monkeypatch):
    def denied(value):
        raise PermissionError("canonical skill read denial")
    monkeypatch.setattr(n8n_adapter, "load_automation_n8n_private_skill_context", denied)
    with pytest.raises(PermissionError, match="canonical skill read denial"):
        visibility.load_automation_n8n_private_skill_context(("n8n-agents-official",))
