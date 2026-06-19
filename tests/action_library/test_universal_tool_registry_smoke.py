from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    build_universal_tool_manifest,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_registry import (
    build_universal_tool_registry,
)


def test_universal_tool_registry_smoke() -> None:
    browser = build_universal_tool_manifest(
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
    registry = build_universal_tool_registry((browser,)).to_read_model()

    assert registry["safe_direct_tool_ids"] == ("browser.open",)
    assert registry["duplicate_tool_ids"] == ()
