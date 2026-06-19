from __future__ import annotations

import json
from pathlib import Path


MANIFESTS = (
    Path("EXTERNAL_BACKENDS/agent_tooling/manifests/openai_agents_sdk_manifest.json"),
    Path("EXTERNAL_BACKENDS/agent_tooling/manifests/mcp_manifest.json"),
    Path("EXTERNAL_BACKENDS/agent_tooling/manifests/autogen_manifest.json"),
    Path("EXTERNAL_BACKENDS/agent_tooling/manifests/langgraph_manifest.json"),
)

REPORT = Path("EXTERNAL_BACKENDS/agent_tooling/security_reports/agent_tooling_vendor_gate_report.json")


def test_agent_tooling_vendor_manifests_smoke() -> None:
    assert REPORT.exists()
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["hard_gate_passed"] is True
    assert report["manual_security_review_required"] is True
    assert report["owner_identity_gate_required"] is True
    assert report["risk_gate_required"] is True

    for manifest_path in MANIFESTS:
        assert manifest_path.exists(), str(manifest_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["adapter_mode"] == "external_adapter"
        assert manifest["provider_kind"] in {"tool_provider", "agent_provider"}
        assert manifest["not_canonical_truth"] is True
        assert manifest["requires_verified_owner"] is True
        assert manifest["safe_direct_allowed"] is False
