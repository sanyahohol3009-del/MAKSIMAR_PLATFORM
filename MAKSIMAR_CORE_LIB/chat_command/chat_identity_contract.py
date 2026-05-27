from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_IDENTITY_KINDS = ("human_owner", "human_family", "jarvis_agent", "system_service", "external_adapter")
_ALLOWED_TRUST_LEVELS = ("owner", "trusted", "restricted", "adapter_read_only")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class ChatIdentityContract:
    """Canonical chat identity contract.

    Contract only. It does not authenticate, send messages, execute commands,
    mutate runtime, or call mobile/server APIs.
    """

    identity_id: str
    display_name: str
    identity_kind: str
    trust_level: str
    command_source_allowed: bool
    direct_execution_allowed: bool
    external_adapter: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "identity_id", _ensure_non_empty(self.identity_id, "identity_id"))
        object.__setattr__(self, "display_name", _ensure_non_empty(self.display_name, "display_name"))
        object.__setattr__(
            self,
            "identity_kind",
            _ensure_allowed(self.identity_kind, "identity_kind", _ALLOWED_IDENTITY_KINDS),
        )
        object.__setattr__(
            self,
            "trust_level",
            _ensure_allowed(self.trust_level, "trust_level", _ALLOWED_TRUST_LEVELS),
        )

        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False for chat identity contracts")

        if self.identity_kind == "external_adapter" and not self.external_adapter:
            raise ValueError("external_adapter identity_kind requires external_adapter=True")

        if self.external_adapter and self.command_source_allowed:
            raise ValueError("external adapters must not be command sources")


def build_owner_chat_identity(identity_id: str, display_name: str) -> ChatIdentityContract:
    return ChatIdentityContract(
        identity_id=identity_id,
        display_name=display_name,
        identity_kind="human_owner",
        trust_level="owner",
        command_source_allowed=True,
        direct_execution_allowed=False,
        external_adapter=False,
    )
