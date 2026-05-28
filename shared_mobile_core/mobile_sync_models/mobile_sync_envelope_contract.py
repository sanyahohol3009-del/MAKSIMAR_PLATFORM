from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_ALLOWED_MEMORY_DOMAINS = ("app_memory", "chat_memory")
_APP_MEMORY_REF_PREFIX = "app-memory://"
_CHAT_MEMORY_REF_PREFIX = "chat-memory://"
_CURSOR_REF_PREFIXES = ("cursor://", "ref://")
_POLICY_REF_PREFIXES = ("policy://", "ref://")
_AUDIT_REF_PREFIXES = ("audit://", "ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed_memory_domain(value: str) -> str:
    value = _ensure_non_empty(value, "memory_domain")
    if value not in _ALLOWED_MEMORY_DOMAINS:
        raise ValueError(f"memory_domain must be one of {_ALLOWED_MEMORY_DOMAINS}")
    return value


def _ensure_ref(value: str, field_name: str, allowed_prefixes: tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(allowed_prefixes):
        raise ValueError(f"{field_name} must start with one of {allowed_prefixes}")
    return value


def _ensure_record_refs(values: tuple[str, ...], memory_domain: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("record_refs must be a non-empty tuple")
    required_prefix = _APP_MEMORY_REF_PREFIX if memory_domain == "app_memory" else _CHAT_MEMORY_REF_PREFIX
    normalized = tuple(_ensure_ref(value, "record_ref", (required_prefix,)) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("record_refs must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class MobileSyncEnvelopeContract:
    envelope_id: str
    memory_domain: str
    source_device_id: str
    app_id: str
    owner_identity_id: str
    record_refs: tuple[str, ...]
    cursor_ref: str
    policy_ref: str
    audit_ref: str
    idempotency_key: str
    reference_only: bool
    inline_payload_present: bool
    message_body_present: bool
    heavy_payload_present: bool
    embedded_secret_present: bool
    embedded_key_material_present: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    socket_allowed: bool
    tunnel_allowed: bool
    canonical_truth_mutation_allowed: bool
    mutates_app_memory_store: bool
    mutates_chat_memory_store: bool

    def __post_init__(self) -> None:
        for field_name in ("envelope_id", "source_device_id", "app_id", "owner_identity_id", "idempotency_key"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "memory_domain", _ensure_allowed_memory_domain(self.memory_domain))
        object.__setattr__(self, "record_refs", _ensure_record_refs(self.record_refs, self.memory_domain))
        object.__setattr__(self, "cursor_ref", _ensure_ref(self.cursor_ref, "cursor_ref", _CURSOR_REF_PREFIXES))
        object.__setattr__(self, "policy_ref", _ensure_ref(self.policy_ref, "policy_ref", _POLICY_REF_PREFIXES))
        object.__setattr__(self, "audit_ref", _ensure_ref(self.audit_ref, "audit_ref", _AUDIT_REF_PREFIXES))

        if self.reference_only is not True:
            raise ValueError("reference_only must be True")

        required_false = {
            "inline_payload_present": self.inline_payload_present,
            "message_body_present": self.message_body_present,
            "heavy_payload_present": self.heavy_payload_present,
            "embedded_secret_present": self.embedded_secret_present,
            "embedded_key_material_present": self.embedded_key_material_present,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "canonical_truth_mutation_allowed": self.canonical_truth_mutation_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def for_app_memory(
        cls,
        *,
        envelope_id: str,
        source_device_id: str,
        app_id: str,
        owner_identity_id: str,
        record_refs: tuple[str, ...],
        cursor_ref: str,
        policy_ref: str,
        audit_ref: str,
    ) -> "MobileSyncEnvelopeContract":
        return cls(
            envelope_id=envelope_id,
            memory_domain="app_memory",
            source_device_id=source_device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            record_refs=record_refs,
            cursor_ref=cursor_ref,
            policy_ref=policy_ref,
            audit_ref=audit_ref,
            idempotency_key=f"{envelope_id}:app_memory:{source_device_id}",
            reference_only=True,
            inline_payload_present=False,
            message_body_present=False,
            heavy_payload_present=False,
            embedded_secret_present=False,
            embedded_key_material_present=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            canonical_truth_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    @classmethod
    def for_chat_memory(
        cls,
        *,
        envelope_id: str,
        source_device_id: str,
        app_id: str,
        owner_identity_id: str,
        record_refs: tuple[str, ...],
        cursor_ref: str,
        policy_ref: str,
        audit_ref: str,
    ) -> "MobileSyncEnvelopeContract":
        return cls(
            envelope_id=envelope_id,
            memory_domain="chat_memory",
            source_device_id=source_device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            record_refs=record_refs,
            cursor_ref=cursor_ref,
            policy_ref=policy_ref,
            audit_ref=audit_ref,
            idempotency_key=f"{envelope_id}:chat_memory:{source_device_id}",
            reference_only=True,
            inline_payload_present=False,
            message_body_present=False,
            heavy_payload_present=False,
            embedded_secret_present=False,
            embedded_key_material_present=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            socket_allowed=False,
            tunnel_allowed=False,
            canonical_truth_mutation_allowed=False,
            mutates_app_memory_store=False,
            mutates_chat_memory_store=False,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "memory_domain": self.memory_domain,
            "source_device_id": self.source_device_id,
            "app_id": self.app_id,
            "owner_identity_id": self.owner_identity_id,
            "record_refs": self.record_refs,
            "cursor_ref": self.cursor_ref,
            "policy_ref": self.policy_ref,
            "audit_ref": self.audit_ref,
            "idempotency_key": self.idempotency_key,
            "reference_only": self.reference_only,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "mutates_app_memory_store": self.mutates_app_memory_store,
            "mutates_chat_memory_store": self.mutates_chat_memory_store,
        }
