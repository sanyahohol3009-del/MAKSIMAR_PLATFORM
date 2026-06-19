from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


_RISK_CLASSES = {"read_only", "safe_direct", "risk_gate"}


@dataclass(frozen=True, slots=True)
class UniversalToolManifest:
    tool_id: str
    source_library: str
    capability_id: str
    description: str
    aliases: tuple[str, ...]
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    risk_class: str
    side_effects: tuple[str, ...]
    read_only: bool
    requires_verified_owner: bool
    safe_direct_allowed: bool
    semantic_fingerprint: str
    adapter_mode: str = "internal_adapter"
    provider_kind: str = "tool_provider"
    not_canonical_truth: bool = True
    module_import_name: str = ""
    package_name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in (
            "tool_id",
            "source_library",
            "capability_id",
            "description",
            "risk_class",
            "semantic_fingerprint",
            "adapter_mode",
            "provider_kind",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.risk_class not in _RISK_CLASSES:
            raise ValueError(f"unsupported risk_class: {self.risk_class!r}")
        if not self.aliases:
            raise ValueError("aliases must not be empty")
        if not self.side_effects:
            raise ValueError("side_effects must not be empty")
        if self.safe_direct_allowed and self.requires_verified_owner is not True:
            raise ValueError("safe_direct_allowed requires verified owner")
        if self.read_only and self.risk_class != "read_only":
            raise ValueError("read_only manifest must use risk_class=read_only")

    def normalized_aliases(self) -> tuple[str, ...]:
        return tuple(alias.strip().casefold() for alias in self.aliases if alias.strip())

    def to_read_model(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "source_library": self.source_library,
            "capability_id": self.capability_id,
            "description": self.description,
            "aliases": self.aliases,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "risk_class": self.risk_class,
            "side_effects": self.side_effects,
            "read_only": self.read_only,
            "requires_verified_owner": self.requires_verified_owner,
            "safe_direct_allowed": self.safe_direct_allowed,
            "semantic_fingerprint": self.semantic_fingerprint,
            "adapter_mode": self.adapter_mode,
            "provider_kind": self.provider_kind,
            "not_canonical_truth": self.not_canonical_truth,
            "module_import_name": self.module_import_name,
            "package_name": self.package_name,
            "metadata": self.metadata,
        }


def build_universal_tool_manifest(payload: dict[str, Any]) -> UniversalToolManifest:
    return UniversalToolManifest(
        tool_id=str(payload["tool_id"]),
        source_library=str(payload["source_library"]),
        capability_id=str(payload["capability_id"]),
        description=str(payload["description"]),
        aliases=tuple(str(alias) for alias in payload["aliases"]),
        input_schema=dict(payload["input_schema"]),
        output_schema=dict(payload["output_schema"]),
        risk_class=str(payload["risk_class"]),
        side_effects=tuple(str(effect) for effect in payload["side_effects"]),
        read_only=bool(payload["read_only"]),
        requires_verified_owner=bool(payload["requires_verified_owner"]),
        safe_direct_allowed=bool(payload["safe_direct_allowed"]),
        semantic_fingerprint=str(payload["semantic_fingerprint"]),
        adapter_mode=str(payload.get("adapter_mode", "internal_adapter")),
        provider_kind=str(payload.get("provider_kind", "tool_provider")),
        not_canonical_truth=bool(payload.get("not_canonical_truth", True)),
        module_import_name=str(payload.get("module_import_name", "")),
        package_name=str(payload.get("package_name", "")),
        metadata=dict(payload.get("metadata", {})),
    )
