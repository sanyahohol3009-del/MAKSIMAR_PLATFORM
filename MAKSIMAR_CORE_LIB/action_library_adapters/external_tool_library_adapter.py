from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_manifest import (
    UniversalToolManifest,
    build_universal_tool_manifest,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.universal_tool_registry import (
    UniversalToolRegistry,
    build_universal_tool_registry,
)


_MANIFEST_ROOT = Path("EXTERNAL_BACKENDS/agent_tooling/manifests")


@dataclass(frozen=True, slots=True)
class ExternalToolAdapterStatus:
    tool_id: str
    source_library: str
    capability_id: str
    adapter_mode: str
    provider_kind: str
    installed: bool
    activation_blocked_reason: str
    import_probe_worked: bool
    requires_verified_owner: bool
    safe_direct_allowed: bool
    risk_gate_required: bool
    visible_to_jarvis: bool
    not_canonical_truth: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "source_library": self.source_library,
            "capability_id": self.capability_id,
            "adapter_mode": self.adapter_mode,
            "provider_kind": self.provider_kind,
            "installed": self.installed,
            "activation_blocked_reason": self.activation_blocked_reason,
            "import_probe_worked": self.import_probe_worked,
            "requires_verified_owner": self.requires_verified_owner,
            "safe_direct_allowed": self.safe_direct_allowed,
            "risk_gate_required": self.risk_gate_required,
            "visible_to_jarvis": self.visible_to_jarvis,
            "not_canonical_truth": self.not_canonical_truth,
        }


def _manifest_paths() -> tuple[Path, ...]:
    return tuple(sorted(_MANIFEST_ROOT.glob("*_manifest.json")))


def load_external_tool_manifests() -> tuple[UniversalToolManifest, ...]:
    manifests: list[UniversalToolManifest] = []
    for path in _manifest_paths():
        payload = json.loads(path.read_text(encoding="utf-8"))
        manifests.append(build_universal_tool_manifest(payload))
    return tuple(manifests)


def build_external_tool_registry() -> UniversalToolRegistry:
    return build_universal_tool_registry(load_external_tool_manifests())


def probe_external_tool_adapters() -> tuple[ExternalToolAdapterStatus, ...]:
    statuses: list[ExternalToolAdapterStatus] = []
    for manifest in load_external_tool_manifests():
        module_name = manifest.module_import_name or manifest.package_name
        spec = importlib.util.find_spec(module_name) if module_name else None
        installed = spec is not None
        statuses.append(
            ExternalToolAdapterStatus(
                tool_id=manifest.tool_id,
                source_library=manifest.source_library,
                capability_id=manifest.capability_id,
                adapter_mode=manifest.adapter_mode,
                provider_kind=manifest.provider_kind,
                installed=installed,
                activation_blocked_reason=""
                if installed
                else f"{module_name or manifest.tool_id} not installed",
                import_probe_worked=installed,
                requires_verified_owner=manifest.requires_verified_owner,
                safe_direct_allowed=manifest.safe_direct_allowed,
                risk_gate_required=manifest.risk_class == "risk_gate",
                visible_to_jarvis=True,
                not_canonical_truth=manifest.not_canonical_truth,
            )
        )
    return tuple(statuses)


def select_external_adapter_tools_for_text(user_text: str) -> tuple[UniversalToolManifest, ...]:
    lowered = str(user_text).casefold()
    matched: list[UniversalToolManifest] = []
    for manifest in load_external_tool_manifests():
        aliases = tuple(alias.casefold() for alias in manifest.aliases)
        if any(alias in lowered for alias in aliases) or manifest.source_library.casefold() in lowered:
            matched.append(manifest)
    return tuple(matched)


def build_jarvis_external_adapter_visibility_read_model() -> dict[str, Any]:
    return {
        "registry": build_external_tool_registry().to_read_model(),
        "adapters": tuple(status.to_read_model() for status in probe_external_tool_adapters()),
    }
