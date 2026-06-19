from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.tool_semantic_dedupe import dedupe_tool_manifests
from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    build_universal_tool_manifest,
)


def test_tool_semantic_dedupe_smoke() -> None:
    manifest_a = build_universal_tool_manifest(
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
    )
    manifest_b = build_universal_tool_manifest(
        {
            "tool_id": "browser_open",
            "source_library": "internal",
            "capability_id": "browser_worker",
            "description": "Open browser safely again",
            "aliases": ["browser", "launch browser"],
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "risk_class": "safe_direct",
            "side_effects": ["launch_browser"],
            "read_only": False,
            "requires_verified_owner": True,
            "safe_direct_allowed": True,
            "semantic_fingerprint": "browser_open_safe_v1",
        }
    )
    unique, duplicates = dedupe_tool_manifests((manifest_a, manifest_b))

    assert len(unique) == 1
    assert duplicates == ("browser_open",)
