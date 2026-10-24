from __future__ import annotations

import CONTROL_PLANE.api_server as api_server


def test_jarvis_live_tools_returns_existing_inventory_catalog(monkeypatch) -> None:
    catalog = {
        "catalog_id": "existing_capability_inventory_v2", "source": "existing_capability_inventory",
        "capability_visible_count": 9, "capability_direct_count": 4,
        "counts_by_capability_kind": {"pc_action": 1, "readonly_tool": 1},
        "counts_by_status": {"available": 2}, "direct_pc_actions": ({"capability_id": "pc"},),
        "readonly_tools": ({"capability_id": "read"},), "memory_tools": (),
        "retrieval_backends": ({"capability_id": "r1"}, {"capability_id": "r2"}, {"capability_id": "r3"}),
        "skills": (), "agents": (), "workers": (),
        "external_adapters": ({"capability_id": "e1"}, {"capability_id": "e2"}, {"capability_id": "e3"}),
        "workflow_automation": (), "runtime_tooling": ({"capability_id": "runtime"},),
        "runtime_voice": (), "runtime_windows_edge": (), "jarvis_runtime_library": (),
        "external_tools": (), "protected_tools": (), "unavailable_capabilities": (),
        "external_code_commit_policy": "external runtime only, do not commit vendor code",
    }
    calls = {"legacy_catalog": 0, "inventory_catalog": 0}
    def legacy_catalog():
        calls["legacy_catalog"] += 1
        return {"catalog_id": "legacy", "_external_visibility": {"adapters": ()}}
    def inventory_catalog(**kwargs):
        calls["inventory_catalog"] += 1
        assert kwargs["readonly_catalog"]["catalog_id"] == "legacy"
        assert kwargs["external_visibility"] == {"adapters": ()}
        return catalog
    monkeypatch.setattr(api_server, "_legacy_readonly_adapter", lambda: type("Legacy", (), {
        "build_jarvis_live_tool_catalog_read_model": staticmethod(legacy_catalog)
    })())
    monkeypatch.setattr(api_server, "_existing_capability_catalog", inventory_catalog)

    payload = api_server.jarvis_live_tools()

    assert payload["ok"] is True
    assert payload["source"] == "existing_capability_inventory"
    assert payload["external_code_commit_policy"] == "external runtime only, do not commit vendor code"
    assert "counts_by_capability_kind" in payload
    assert len(payload["direct_pc_actions"]) >= 1
    assert len(payload["readonly_tools"]) >= 1
    assert len(payload["external_adapters"]) >= 3
    assert len(payload["retrieval_backends"]) >= 3
    assert len(payload["runtime_tooling"]) >= 1
    assert "legacy_tools" in payload
    assert calls == {"legacy_catalog": 1, "inventory_catalog": 1}
