from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.MOBILE_SYNC_RUNTIME.mobile_sync_session_registry import MobileSyncSessionState
from shared_mobile_core.mobile_sync_models.mobile_sync_cursor_contract import MobileSyncCursorContract
from shared_mobile_core.mobile_sync_models.mobile_sync_envelope_contract import MobileSyncEnvelopeContract
from shared_mobile_core.mobile_sync_models.mobile_sync_policy import MobileSyncPolicy


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class AppMemorySyncDecision:
    decision_id: str
    session: MobileSyncSessionState
    envelope: MobileSyncEnvelopeContract
    cursor: MobileSyncCursorContract
    policy: MobileSyncPolicy
    decision_status: str
    decision_reason: str
    success_requires_evidence: bool
    silent_success_allowed: bool
    read_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_connection_allowed: bool
    runtime_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_id", _ensure_non_empty(self.decision_id, "decision_id"))
        object.__setattr__(self, "decision_status", _ensure_non_empty(self.decision_status, "decision_status"))
        object.__setattr__(self, "decision_reason", _ensure_non_empty(self.decision_reason, "decision_reason"))

        if not isinstance(self.session, MobileSyncSessionState):
            raise ValueError("session must be MobileSyncSessionState")
        if not isinstance(self.envelope, MobileSyncEnvelopeContract):
            raise ValueError("envelope must be MobileSyncEnvelopeContract")
        if not isinstance(self.cursor, MobileSyncCursorContract):
            raise ValueError("cursor must be MobileSyncCursorContract")
        if not isinstance(self.policy, MobileSyncPolicy):
            raise ValueError("policy must be MobileSyncPolicy")

        if self.envelope.memory_domain != "app_memory":
            raise ValueError("app memory runtime accepts only app_memory envelopes")
        if self.cursor.memory_domain != "app_memory":
            raise ValueError("app memory runtime requires app_memory cursor")
        if self.envelope.policy_ref != self.policy.policy_ref:
            raise ValueError("envelope policy_ref must match runtime policy")
        if self.session.policy.policy_ref != self.policy.policy_ref:
            raise ValueError("session policy_ref must match runtime policy")
        if not self.policy.allows_domain("app_memory"):
            raise ValueError("policy must allow app_memory domain")
        if tuple(self.envelope.record_refs) == ():
            raise ValueError("envelope must contain record references")

        if self.decision_status != "accepted_reference_sync":
            raise ValueError("decision_status must be accepted_reference_sync")
        if self.success_requires_evidence is not True:
            raise ValueError("success_requires_evidence must be True")
        if self.silent_success_allowed is not False:
            raise ValueError("silent_success_allowed must be False")
        if self.read_only is not True:
            raise ValueError("read_only must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_connection_allowed": self.runtime_connection_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "session_id": self.session.session_id,
            "memory_domain": self.envelope.memory_domain,
            "record_refs": self.envelope.record_refs,
            "cursor_ref": self.envelope.cursor_ref,
            "policy_ref": self.policy.policy_ref,
            "decision_status": self.decision_status,
            "decision_reason": self.decision_reason,
            "success_requires_evidence": self.success_requires_evidence,
            "silent_success_allowed": self.silent_success_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
        }


@dataclass(frozen=True)
class AppMemorySyncRuntime:
    runtime_id: str
    policy: MobileSyncPolicy
    read_only_runtime: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    runtime_connection_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "runtime_id", _ensure_non_empty(self.runtime_id, "runtime_id"))
        if not isinstance(self.policy, MobileSyncPolicy):
            raise ValueError("policy must be MobileSyncPolicy")
        if self.read_only_runtime is not True:
            raise ValueError("read_only_runtime must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "runtime_connection_allowed": self.runtime_connection_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default(cls, *, runtime_id: str, policy: MobileSyncPolicy) -> "AppMemorySyncRuntime":
        return cls(
            runtime_id=runtime_id,
            policy=policy,
            read_only_runtime=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    def evaluate(
        self,
        *,
        session: MobileSyncSessionState,
        envelope: MobileSyncEnvelopeContract,
        cursor: MobileSyncCursorContract,
    ) -> AppMemorySyncDecision:
        return AppMemorySyncDecision(
            decision_id=f"{self.runtime_id}:{session.session_id}:{envelope.envelope_id}",
            session=session,
            envelope=envelope,
            cursor=cursor,
            policy=self.policy,
            decision_status="accepted_reference_sync",
            decision_reason="app_memory_envelope_validated_against_policy_and_cursor",
            success_requires_evidence=True,
            silent_success_allowed=False,
            read_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            runtime_connection_allowed=False,
            runtime_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )
