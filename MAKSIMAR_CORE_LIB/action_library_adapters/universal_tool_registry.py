from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.tool_semantic_dedupe import dedupe_tool_manifests
from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import UniversalToolManifest


@dataclass(frozen=True, slots=True)
class UniversalToolRegistry:
    registry_id: str
    tools: tuple[UniversalToolManifest, ...]
    duplicate_tool_ids: tuple[str, ...]
    read_only_enabled_tool_ids: tuple[str, ...]
    safe_direct_tool_ids: tuple[str, ...]
    risk_gated_tool_ids: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "tools": tuple(tool.to_read_model() for tool in self.tools),
            "duplicate_tool_ids": self.duplicate_tool_ids,
            "read_only_enabled_tool_ids": self.read_only_enabled_tool_ids,
            "safe_direct_tool_ids": self.safe_direct_tool_ids,
            "risk_gated_tool_ids": self.risk_gated_tool_ids,
        }


def build_universal_tool_registry(manifests: tuple[UniversalToolManifest, ...]) -> UniversalToolRegistry:
    unique, duplicates = dedupe_tool_manifests(manifests)
    return UniversalToolRegistry(
        registry_id="universal_tool_registry_v1",
        tools=unique,
        duplicate_tool_ids=duplicates,
        read_only_enabled_tool_ids=tuple(tool.tool_id for tool in unique if tool.read_only),
        safe_direct_tool_ids=tuple(tool.tool_id for tool in unique if tool.safe_direct_allowed),
        risk_gated_tool_ids=tuple(tool.tool_id for tool in unique if tool.risk_class == "risk_gate"),
    )
