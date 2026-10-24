from __future__ import annotations

from dataclasses import dataclass


CONTROL_PLANE_STREAM_URL = "http://127.0.0.1:8000/jarvis-live/hot"
CONTROL_PLANE_HEALTH_URL = "http://127.0.0.1:8000/jarvis-live/health"


@dataclass(frozen=True)
class VoiceEdgeV2Policy:
    policy_id: str
    control_plane_stream_url: str
    control_plane_health_url: str
    direct_ollama_allowed: bool
    visibility_allowed: bool
    selection_allowed: bool
    safe_owner_pc_control_allowed: bool
    protected_execution_allowed: bool
    owner_gate_required: bool
    approval_required: bool
    public_network_allowed: bool
    tunnel_allowed: bool
    final_mode_requires_always_listening: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if "127.0.0.1:8000" not in self.control_plane_stream_url:
            raise ValueError("voice edge must route to CONTROL_PLANE 127.0.0.1:8000")
        if "11434" in self.control_plane_stream_url:
            raise ValueError("voice edge must not route directly to Ollama")
        if self.direct_ollama_allowed:
            raise ValueError("direct_ollama_allowed must remain false")
        if not self.visibility_allowed:
            raise ValueError("visibility_allowed must remain true")
        if not self.selection_allowed:
            raise ValueError("selection_allowed must remain true")
        if self.protected_execution_allowed:
            raise ValueError("protected_execution_allowed must remain false without approval")
        if not self.owner_gate_required:
            raise ValueError("owner_gate_required must remain true")
        if not self.approval_required:
            raise ValueError("approval_required must remain true")
        if self.public_network_allowed:
            raise ValueError("public_network_allowed must remain false")
        if self.tunnel_allowed:
            raise ValueError("tunnel_allowed must remain false")
        if not self.final_mode_requires_always_listening:
            raise ValueError("final voice mode must require always-listening")

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "control_plane_stream_url": self.control_plane_stream_url,
            "control_plane_health_url": self.control_plane_health_url,
            "direct_ollama_allowed": self.direct_ollama_allowed,
            "visibility_allowed": self.visibility_allowed,
            "selection_allowed": self.selection_allowed,
            "safe_owner_pc_control_allowed": self.safe_owner_pc_control_allowed,
            "protected_execution_allowed": self.protected_execution_allowed,
            "owner_gate_required": self.owner_gate_required,
            "approval_required": self.approval_required,
            "public_network_allowed": self.public_network_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "final_mode_requires_always_listening": self.final_mode_requires_always_listening,
        }


def build_default_voice_edge_v2_policy() -> VoiceEdgeV2Policy:
    return VoiceEdgeV2Policy(
        policy_id="voice_edge_v2_policy_001",
        control_plane_stream_url=CONTROL_PLANE_STREAM_URL,
        control_plane_health_url=CONTROL_PLANE_HEALTH_URL,
        direct_ollama_allowed=False,
        visibility_allowed=True,
        selection_allowed=True,
        safe_owner_pc_control_allowed=True,
        protected_execution_allowed=False,
        owner_gate_required=True,
        approval_required=True,
        public_network_allowed=False,
        tunnel_allowed=False,
        final_mode_requires_always_listening=True,
    )
