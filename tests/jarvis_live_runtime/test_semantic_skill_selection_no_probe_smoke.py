from __future__ import annotations


def test_select_skills_for_tools_uses_static_descriptors_without_heavy_visibility(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_skill_visibility as visibility

    def fail_heavy_visibility() -> dict[str, object]:
        raise AssertionError("select_skills_for_tools must not call heavy skill visibility read model")

    monkeypatch.setattr(visibility, "build_jarvis_skill_visibility_read_model", fail_heavy_visibility)

    project_skills = visibility.select_skills_for_tools(
        ("repo_search", "read_file_snippet", "read_file_outline"),
        ("project_coder_agent",),
    )
    assert "project_workspace_analysis" in project_skills

    catalog_skills = visibility.select_skills_for_tools(
        ("build_jarvis_live_tool_catalog_read_model",),
        ("tool_selector_agent",),
    )
    assert "tool_selection" in catalog_skills
    assert "skill_visibility" in catalog_skills

    external_skills = visibility.select_skills_for_tools(
        ("external_adapter:mcp_python_sdk",),
        ("tool_selector_agent",),
    )
    assert "external_agent_tooling" in external_skills


def test_select_skills_for_tools_keeps_safety_boundaries_static() -> None:
    import tools.jarvis_live_runtime.jarvis_skill_visibility as visibility

    pc_skills = visibility.select_skills_for_tools(
        ("pc_open_browser",),
        ("action_worker_agent",),
    )
    assert "action_library_safe_direct" in pc_skills
    assert "action_library" in pc_skills

    gated_skills = visibility.select_skills_for_tools(
        ("risk_gate", "operator_proposal", "approval_boundary_read"),
        ("safety_guard_agent",),
    )
    assert "risk_gate_or_action_library" in gated_skills
    assert "safety_guard" in gated_skills
