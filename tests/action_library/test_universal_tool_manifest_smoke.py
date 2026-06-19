from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    build_universal_tool_manifest,
)


def test_universal_tool_manifest_smoke() -> None:
    manifest = build_universal_tool_manifest(
        {
            "tool_id": "browser.open",
            "source_library": "internal",
            "capability_id": "browser_worker",
            "description": "Open browser safely",
            "aliases": ["browser", "open browser"],
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "risk_class": "safe_direct",
            "side_effects": ["launch_browser"],
            "read_only": False,
            "requires_verified_owner": True,
            "safe_direct_allowed": True,
            "semantic_fingerprint": "browser_open_safe_v1",
        }
    ).to_read_model()

    assert manifest["tool_id"] == "browser.open"
    assert manifest["safe_direct_allowed"] is True
    assert manifest["requires_verified_owner"] is True
