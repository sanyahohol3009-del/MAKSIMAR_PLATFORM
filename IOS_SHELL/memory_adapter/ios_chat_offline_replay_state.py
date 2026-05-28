from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.chat_memory import ChatMemoryRetentionPolicy


_REF_PREFIXES = ("chat-memory://", "ios-local://", "ref://", "audit://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a reference")
    return value


def _ensure_refs(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    normalized = tuple(_ensure_ref(value, field_name[:-1] if field_name.endswith("s") else field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class IOSChatOfflineReplayState:
    replay_state_id: str
    device_id: str
    app_id: str
    owner_identity_id: str
    ios_bundle_id: str
    retention_policy: ChatMemoryRetentionPolicy
    queued_record_refs: tuple[str, ...]
    replay_cursor_ref: str
    replay_policy_ref: str
    audit_ref: str
    eligible_for_replay: bool
    local_policy_required: bool
    server_presence_required_for_upload: bool
    owner_approval_required: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    network_allowed: bool
    platform_api_calls_allowed: bool
    sync_runtime_allowed: bool
    mutates_queue: bool
    stores_message_body: bool
    stores_heavy_payload: bool

    def __post_init__(self) -> None:
        for field_name in ("replay_state_id", "device_id", "app_id", "owner_identity_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.retention_policy, ChatMemoryRetentionPolicy):
            raise ValueError("retention_policy must be ChatMemoryRetentionPolicy")

        object.__setattr__(self, "queued_record_refs", _ensure_refs(self.queued_record_refs, "queued_record_refs"))
        object.__setattr__(self, "replay_cursor_ref", _ensure_ref(self.replay_cursor_ref, "replay_cursor_ref"))
        object.__setattr__(self, "replay_policy_ref", _ensure_ref(self.replay_policy_ref, "replay_policy_ref"))
        object.__setattr__(self, "audit_ref", _ensure_ref(self.audit_ref, "audit_ref"))

        required_true = {
            "eligible_for_replay": self.eligible_for_replay,
            "local_policy_required": self.local_policy_required,
            "server_presence_required_for_upload": self.server_presence_required_for_upload,
            "owner_approval_required": self.owner_approval_required,
            "local_chat_memory_only": self.local_chat_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "openim_truth": self.openim_truth,
            "core_chat_truth": self.core_chat_truth,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "network_allowed": self.network_allowed,
            "platform_api_calls_allowed": self.platform_api_calls_allowed,
            "sync_runtime_allowed": self.sync_runtime_allowed,
            "mutates_queue": self.mutates_queue,
            "stores_message_body": self.stores_message_body,
            "stores_heavy_payload": self.stores_heavy_payload,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

        if not self.retention_policy.local_only:
            raise ValueError("retention_policy local_only must be True")
        if not self.retention_policy.server_deletion_requires_sync_policy:
            raise ValueError("retention_policy server deletion must require sync policy")
        if not self.retention_policy.offline_replay_policy_required:
            raise ValueError("retention_policy offline replay policy must be required")

    @classmethod
    def default_state(
        cls,
        *,
        replay_state_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
        ios_bundle_id: str,
        queued_record_refs: tuple[str, ...],
    ) -> "IOSChatOfflineReplayState":
        normalized_refs = _ensure_refs(queued_record_refs, "queued_record_refs")
        return cls(
            replay_state_id=replay_state_id,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            ios_bundle_id=ios_bundle_id,
            retention_policy=ChatMemoryRetentionPolicy.strict_default(
                retention_policy_id=f"{replay_state_id}_retention_policy",
                max_age_days=30,
            ),
            queued_record_refs=normalized_refs,
            replay_cursor_ref=f"ios-local://{device_id}/chat-memory/replay/{replay_state_id}/cursor",
            replay_policy_ref=f"ref://{replay_state_id}/offline-replay-policy",
            audit_ref=f"audit://{replay_state_id}",
            eligible_for_replay=True,
            local_policy_required=True,
            server_presence_required_for_upload=True,
            owner_approval_required=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            network_allowed=False,
            platform_api_calls_allowed=False,
            sync_runtime_allowed=False,
            mutates_queue=False,
            stores_message_body=False,
            stores_heavy_payload=False,
        )
