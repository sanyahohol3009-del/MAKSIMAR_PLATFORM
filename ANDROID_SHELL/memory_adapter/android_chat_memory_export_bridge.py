from __future__ import annotations

from dataclasses import dataclass


_REF_PREFIXES = ("chat-memory://", "android-local://", "ref://")
_ALLOWED_FORMATS = ("reference_bundle", "audit_reference_bundle")


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
class AndroidChatMemoryExportBridge:
    bridge_id: str
    device_id: str
    app_id: str
    owner_identity_id: str
    android_package_name: str
    export_request_ref: str
    exported_record_refs: tuple[str, ...]
    export_format: str
    export_requires_policy: bool
    export_payload_embedded: bool
    read_only_export: bool
    local_chat_memory_only: bool
    openim_truth: bool
    core_chat_truth: bool
    canonical_truth: bool
    network_allowed: bool
    file_io_allowed: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("bridge_id", "device_id", "app_id", "owner_identity_id", "android_package_name"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "export_request_ref", _ensure_ref(self.export_request_ref, "export_request_ref"))
        object.__setattr__(self, "exported_record_refs", _ensure_refs(self.exported_record_refs, "exported_record_refs"))

        object.__setattr__(self, "export_format", _ensure_non_empty(self.export_format, "export_format"))
        if self.export_format not in _ALLOWED_FORMATS:
            raise ValueError(f"export_format must be one of {_ALLOWED_FORMATS}")

        required_true = {
            "export_requires_policy": self.export_requires_policy,
            "read_only_export": self.read_only_export,
            "local_chat_memory_only": self.local_chat_memory_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "export_payload_embedded": self.export_payload_embedded,
            "openim_truth": self.openim_truth,
            "core_chat_truth": self.core_chat_truth,
            "canonical_truth": self.canonical_truth,
            "network_allowed": self.network_allowed,
            "file_io_allowed": self.file_io_allowed,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_bridge(
        cls,
        *,
        bridge_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
        android_package_name: str,
        exported_record_refs: tuple[str, ...],
    ) -> "AndroidChatMemoryExportBridge":
        return cls(
            bridge_id=bridge_id,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            android_package_name=android_package_name,
            export_request_ref=f"ref://{bridge_id}/export-request",
            exported_record_refs=exported_record_refs,
            export_format="reference_bundle",
            export_requires_policy=True,
            export_payload_embedded=False,
            read_only_export=True,
            local_chat_memory_only=True,
            openim_truth=False,
            core_chat_truth=False,
            canonical_truth=False,
            network_allowed=False,
            file_io_allowed=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )
