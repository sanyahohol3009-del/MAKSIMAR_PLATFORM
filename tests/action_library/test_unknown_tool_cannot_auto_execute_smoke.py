from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    build_universal_tool_manifest,
)


def test_unknown_tool_cannot_auto_execute_smoke() -> None:
    manifest = build_universal_tool_manifest(
        {
            "tool_id": "unknown.side_effect.tool",
            "source_library": "vendor",
            "capability_id": "external_tool_provider",
            "description": "Unknown tool with side effects",
            "aliases": ["unknown tool"],
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "risk_class": "risk_gate",
            "side_effects": ["unknown_side_effect"],
            "read_only": False,
            "requires_verified_owner": True,
            "safe_direct_allowed": False,
            "semantic_fingerprint": "unknown_side_effect_v1",
        }
    ).to_read_model()

    assert manifest["risk_class"] == "risk_gate"
    assert manifest["safe_direct_allowed"] is False
