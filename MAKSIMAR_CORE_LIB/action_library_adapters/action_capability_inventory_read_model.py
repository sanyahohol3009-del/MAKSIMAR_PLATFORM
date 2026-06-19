from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.action_library_adapters.browser_worker_adapter_contract import (
    build_browser_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.cad_cam_worker_adapter_contract import (
    build_cad_cam_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.cli_worker_adapter_contract import (
    build_cli_worker_adapter_contract,
)
from MAKSIMAR_CORE_LIB.action_library_adapters.gui_worker_adapter_contract import (
    build_gui_worker_adapter_contract,
)


@dataclass(frozen=True, slots=True)
class ActionCapabilityInventoryReadModel:
    read_model_id: str
    capabilities: tuple[dict[str, Any], ...]
    safe_direct_capabilities: tuple[str, ...]
    risk_gated_capabilities: tuple[str, ...]

    def to_read_model(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "capabilities": self.capabilities,
            "safe_direct_capabilities": self.safe_direct_capabilities,
            "risk_gated_capabilities": self.risk_gated_capabilities,
        }


def build_action_capability_inventory_read_model() -> ActionCapabilityInventoryReadModel:
    capabilities = (
        build_browser_worker_adapter_contract().to_read_model(),
        build_gui_worker_adapter_contract().to_read_model(),
        build_cli_worker_adapter_contract().to_read_model(),
        build_cad_cam_worker_adapter_contract().to_read_model(),
    )
    safe_direct = tuple(cap["capability_id"] for cap in capabilities if cap["safe_direct_allowed"] is True)
    risk_gated = tuple(cap["capability_id"] for cap in capabilities if cap["risk_class"] == "risk_gate")
    return ActionCapabilityInventoryReadModel(
        read_model_id="action_capability_inventory_read_model_v1",
        capabilities=capabilities,
        safe_direct_capabilities=safe_direct,
        risk_gated_capabilities=risk_gated,
    )
