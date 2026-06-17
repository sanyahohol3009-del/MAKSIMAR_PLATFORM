from __future__ import annotations

from dataclasses import dataclass


CONTROL_PLANE_STREAM_URL = "http://127.0.0.1:8765/jarvis-live/chat/stream"
CONTROL_PLANE_HEALTH_URL = "http://127.0.0.1:8765/jarvis-live/health"


@dataclass(frozen=True)
class VoiceEdgeV2Policy:
    policy_id: str
    control_plane_stream_url: str
    control_plane_health_url: str
    direct_ollama_allowed: bool
    pc_control_allowed: bool
    direct_execution_allowed: bool
    public_network_allowed: bool
    tunnel_allowed: bool
    final_mode_requires_always_listening: bool

    def __post_init__(self) -> None:
        if not self.policy_id.strip():
            raise ValueError("policy_id must be non-empty")
        if "127.0.0.1:8765" not in self.control_plane_stream_url:
            raise ValueError("voice edge must route to CONTROL_PLANE 127.0.0.1:8765")
        if "11434" in self.control_plane_stream_url:
            raise ValueError("voice edge must not route directly to Ollama")
        if self.direct_ollama_allowed:
            raise ValueError("direct_ollama_allowed must remain false")
        if self.pc_control_allowed:
            raise ValueError("pc_control_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")
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
            "pc_control_allowed": self.pc_control_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
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
        pc_control_allowed=False,
        direct_execution_allowed=False,
        public_network_allowed=False,
        tunnel_allowed=False,
        final_mode_requires_always_listening=True,
    )
