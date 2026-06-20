from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.external_tool_library_adapter import (
    build_jarvis_external_adapter_visibility_read_model,
)
from tools.jarvis_live_runtime.agent_tooling_runtime_probe import build_agent_tooling_runtime_probe_read_model


@dataclass(frozen=True, slots=True)
class AgentToolingRuntimeAdapterReadModel:
    adapter_id: str
    runtime_python: str
    registry: dict[str, Any]
    probe: dict[str, Any]
    visible_to_jarvis: bool
    proposal_only: bool
    risk_gate_required: bool
    execution_allowed: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "runtime_python": self.runtime_python,
            "registry": self.registry,
            "probe": self.probe,
            "visible_to_jarvis": self.visible_to_jarvis,
            "proposal_only": self.proposal_only,
            "risk_gate_required": self.risk_gate_required,
            "execution_allowed": self.execution_allowed,
        }


def build_agent_tooling_runtime_adapter_read_model() -> dict[str, Any]:
    visibility = build_jarvis_external_adapter_visibility_read_model()
    probe = build_agent_tooling_runtime_probe_read_model()
    return AgentToolingRuntimeAdapterReadModel(
        adapter_id="agent_tooling_runtime_adapter_v1",
        runtime_python=probe["runtime_python"],
        registry=visibility["registry"],
        probe=probe,
        visible_to_jarvis=True,
        proposal_only=True,
        risk_gate_required=True,
        execution_allowed=False,
    ).to_read_model()
