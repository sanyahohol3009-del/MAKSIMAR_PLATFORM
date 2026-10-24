from __future__ import annotations

from CONTROL_PLANE.api_server import jarvis_live_tools


def test_external_runtime_not_committed_policy_is_visible() -> None:
    payload = jarvis_live_tools()

    assert payload["external_code_commit_policy"] == "external runtime only, do not commit vendor code"
    assert payload["external_tools"]
    assert all(item["source"] in {"external_runtime", "vendor_quarantine"} for item in payload["external_tools"])
    assert all(item["external_path"] != "" for item in payload["external_tools"])
