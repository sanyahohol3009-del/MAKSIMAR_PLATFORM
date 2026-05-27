from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.chat_command.chat_message_contract import ChatMessageContract


_ALLOWED_ROUTE_TARGETS = ("message_reference_store", "command_review_queue", "blocked")
_ALLOWED_ROUTE_REASONS = ("normal_message", "command_intent_requires_review", "blocked_message_state")


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
class MessageRouteDecision:
    message_id: str
    route_target: str
    route_reason: str
    command_review_required: bool
    direct_execution_allowed: bool
    external_network_access_allowed: bool
    runtime_command_execution_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "route_target", _ensure_allowed(self.route_target, "route_target", _ALLOWED_ROUTE_TARGETS))
        object.__setattr__(self, "route_reason", _ensure_allowed(self.route_reason, "route_reason", _ALLOWED_ROUTE_REASONS))

        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_command_execution_allowed:
            raise ValueError("runtime_command_execution_allowed must be False")
        if self.route_target == "command_review_queue" and not self.command_review_required:
            raise ValueError("command_review_queue requires command_review_required=True")


class MessageRouterRuntime:
    """Deterministic in-process chat message router.

    It returns route decisions only. It does not send messages, call external
    services, execute commands, or mutate canonical truth.
    """

    def route_message(self, message: ChatMessageContract) -> MessageRouteDecision:
        if message.message_state == "rejected":
            return MessageRouteDecision(
                message_id=message.message_id,
                route_target="blocked",
                route_reason="blocked_message_state",
                command_review_required=False,
                direct_execution_allowed=False,
                external_network_access_allowed=False,
                runtime_command_execution_allowed=False,
            )

        if message.message_kind == "command_intent":
            return MessageRouteDecision(
                message_id=message.message_id,
                route_target="command_review_queue",
                route_reason="command_intent_requires_review",
                command_review_required=True,
                direct_execution_allowed=False,
                external_network_access_allowed=False,
                runtime_command_execution_allowed=False,
            )

        return MessageRouteDecision(
            message_id=message.message_id,
            route_target="message_reference_store",
            route_reason="normal_message",
            command_review_required=False,
            direct_execution_allowed=False,
            external_network_access_allowed=False,
            runtime_command_execution_allowed=False,
        )
