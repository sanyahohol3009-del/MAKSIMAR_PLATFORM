from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.chat_memory import ChatMemoryRetentionPolicy


_REF_PREFIXES = ("chat-memory://", "android-local://", "ref://")


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
class AndroidChatOfflineReplayState:
    state_id: str
    device_id: str
    app_id: str
    owner_identity_id: str
    android_package_name: str
    replay_record_refs: tuple[str, ...]
    replay_cursor_ref: str
    retention_policy: ChatMemoryRetentionPolicy
    offline_replay_enabled: bool
    offline_replay_policy_required: bool
    sync_requires_policy: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    delivery_semantics_defined: bool
    network_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    real_replay_execution_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("state_id", "device_id", "app_id", "owner_identity_id", "android_package_name"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "replay_record_refs", _ensure_refs(self.replay_record_refs, "replay_record_refs"))
        object.__setattr__(self, "replay_cursor_ref", _ensure_ref(self.replay_cursor_ref, "replay_cursor_ref"))

        if not isinstance(self.retention_policy, ChatMemoryRetentionPolicy):
            raise ValueError("retention_policy must be ChatMemoryRetentionPolicy")
        if self.retention_policy.local_only is not True:
            raise ValueError("retention_policy local_only must be True")
        if self.retention_policy.offline_replay_policy_required is not True:
            raise ValueError("retention_policy offline replay policy must be required")

        required_true = {
            "offline_replay_enabled": self.offline_replay_enabled,
            "offline_replay_policy_required": self.offline_replay_policy_required,
            "sync_requires_policy": self.sync_requires_policy,
            "local_chat_memory_only": self.local_chat_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "openim_truth": self.openim_truth,
            "core_chat_truth": self.core_chat_truth,
            "canonical_truth": self.canonical_truth,
            "delivery_semantics_defined": self.delivery_semantics_defined,
            "network_allowed": self.network_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "real_replay_execution_allowed": self.real_replay_execution_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_state(
        cls,
        *,
        state_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
        android_package_name: str,
        replay_record_refs: tuple[str, ...],
    ) -> "AndroidChatOfflineReplayState":
        retention_policy = ChatMemoryRetentionPolicy.strict_default(
            retention_policy_id=f"{state_id}_retention",
            max_age_days=30,
        )
        return cls(
            state_id=state_id,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            android_package_name=android_package_name,
            replay_record_refs=replay_record_refs,
            replay_cursor_ref=f"android-local://{device_id}/chat-memory/offline-replay/{state_id}/cursor",
            retention_policy=retention_policy,
            offline_replay_enabled=True,
            offline_replay_policy_required=True,
            sync_requires_policy=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            delivery_semantics_defined=False,
            network_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            real_replay_execution_allowed=False,
        )
