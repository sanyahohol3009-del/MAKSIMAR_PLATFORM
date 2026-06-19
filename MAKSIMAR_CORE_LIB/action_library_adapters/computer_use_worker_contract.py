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
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


@dataclass(frozen=True, slots=True)
class ComputerUseActionRequest:
    request_id: str
    capability_id: str
    action_name: str
    target: str
    input_channel: str
    owner_identity_claim: OwnerIdentityClaim
    risk_class: str
    read_only: bool
    side_effects: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("request_id", "capability_id", "action_name", "target", "input_channel", "risk_class"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.input_channel not in {"text", "voice", "screen"}:
            raise ValueError(f"unsupported input_channel: {self.input_channel!r}")
        if not self.side_effects:
            raise ValueError("side_effects must not be empty")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "capability_id": self.capability_id,
            "action_name": self.action_name,
            "target": self.target,
            "input_channel": self.input_channel,
            "owner_identity_claim": self.owner_identity_claim.to_read_model(),
            "risk_class": self.risk_class,
            "read_only": self.read_only,
            "side_effects": self.side_effects,
        }


@dataclass(frozen=True, slots=True)
class ComputerUseWorkerContract:
    contract_id: str
    supported_capabilities: tuple[str, ...]
    direct_os_mutation_allowed: bool
    risk_gate_available: bool
    recording_required: bool
    replay_preview_required: bool
    local_safe_action_env_var: str

    def __post_init__(self) -> None:
        if not isinstance(self.contract_id, str) or not self.contract_id.strip():
            raise ValueError("contract_id must be a non-empty string")
        if not self.supported_capabilities:
            raise ValueError("supported_capabilities must not be empty")
        if self.direct_os_mutation_allowed is not False:
            raise ValueError("direct_os_mutation_allowed must be False")
        if self.risk_gate_available is not True:
            raise ValueError("risk_gate_available must be True")
        if self.recording_required is not True:
            raise ValueError("recording_required must be True")
        if self.replay_preview_required is not True:
            raise ValueError("replay_preview_required must be True")
        if self.local_safe_action_env_var != "JARVIS_LOCAL_SAFE_ACTION_EXECUTION":
            raise ValueError("local_safe_action_env_var must be JARVIS_LOCAL_SAFE_ACTION_EXECUTION")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "supported_capabilities": self.supported_capabilities,
            "direct_os_mutation_allowed": self.direct_os_mutation_allowed,
            "risk_gate_available": self.risk_gate_available,
            "recording_required": self.recording_required,
            "replay_preview_required": self.replay_preview_required,
            "local_safe_action_env_var": self.local_safe_action_env_var,
        }


def build_computer_use_worker_contract() -> ComputerUseWorkerContract:
    return ComputerUseWorkerContract(
        contract_id="computer_use_worker_contract_v1",
        supported_capabilities=(
            "browser_worker",
            "gui_worker",
            "cli_worker",
            "cad_cam_worker",
        ),
        direct_os_mutation_allowed=False,
        risk_gate_available=True,
        recording_required=True,
        replay_preview_required=True,
        local_safe_action_env_var="JARVIS_LOCAL_SAFE_ACTION_EXECUTION",
    )


def build_action_request_from_intent(
    user_text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
) -> ComputerUseActionRequest | None:
    decision = build_autonomous_tool_model_decision(
        user_text,
        input_channel=input_channel,
        owner_identity_claim=owner_identity_claim,
    )
    selected_tools = tuple(str(tool) for tool in decision["selected_tools"])
    if "pc_open_browser" in selected_tools:
        contract = build_browser_worker_adapter_contract()
        return ComputerUseActionRequest(
            request_id="computer_use_action_request_v1",
            capability_id=contract.capability_id,
            action_name="open_browser",
            target="default_browser",
            input_channel=input_channel,
            owner_identity_claim=owner_identity_claim,
            risk_class=contract.risk_class,
            read_only=contract.read_only,
            side_effects=contract.side_effects,
        )
    if "pc_open_app" in selected_tools:
        contract = build_gui_worker_adapter_contract()
        return ComputerUseActionRequest(
            request_id="computer_use_action_request_v1",
            capability_id=contract.capability_id,
            action_name="open_application",
            target="desktop_application",
            input_channel=input_channel,
            owner_identity_claim=owner_identity_claim,
            risk_class=contract.risk_class,
            read_only=contract.read_only,
            side_effects=contract.side_effects,
        )
    lowered = str(user_text).casefold()
    if any(marker in lowered for marker in ("git push", "delete", "sudo", "rm -rf")):
        contract = build_cli_worker_adapter_contract()
        return ComputerUseActionRequest(
            request_id="computer_use_action_request_v1",
            capability_id=contract.capability_id,
            action_name="mutating_shell_request",
            target=str(user_text),
            input_channel=input_channel,
            owner_identity_claim=owner_identity_claim,
            risk_class=contract.risk_class,
            read_only=contract.read_only,
            side_effects=contract.side_effects,
        )
    if any(marker in lowered for marker in ("cad", "cam", "cnc", "machine")):
        contract = build_cad_cam_worker_adapter_contract()
        return ComputerUseActionRequest(
            request_id="computer_use_action_request_v1",
            capability_id=contract.capability_id,
            action_name="machine_control_request",
            target=str(user_text),
            input_channel=input_channel,
            owner_identity_claim=owner_identity_claim,
            risk_class=contract.risk_class,
            read_only=contract.read_only,
            side_effects=contract.side_effects,
        )
    return None
