from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_MEDIA_KINDS = ("image", "audio", "video", "document", "binary")
_ALLOWED_PREVIEW_STATES = ("metadata_only", "preview_blocked", "quarantine_reference", "accepted_reference")


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
class IOSMediaAttachmentBridgeContract:
    """iOS media attachment bridge.

    Contract only. It does not render media, generate thumbnails, decode binary
    payloads, upload/download media, or call iOS media APIs.
    """

    bridge_id: str
    attachment_id: str
    message_id: str
    media_kind: str
    mime_type: str
    preview_state: str
    scan_required: bool
    quarantine_required: bool
    metadata_only: bool
    direct_media_render_allowed: bool
    thumbnail_generation_allowed: bool
    ios_media_api_call_allowed: bool
    external_network_access_allowed: bool
    runtime_execution_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _ensure_non_empty(self.bridge_id, "bridge_id"))
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "media_kind", _ensure_allowed(self.media_kind, "media_kind", _ALLOWED_MEDIA_KINDS))
        object.__setattr__(self, "mime_type", _ensure_non_empty(self.mime_type, "mime_type"))
        object.__setattr__(
            self,
            "preview_state",
            _ensure_allowed(self.preview_state, "preview_state", _ALLOWED_PREVIEW_STATES),
        )

        if not self.scan_required:
            raise ValueError("scan_required must be True")
        if not self.quarantine_required:
            raise ValueError("quarantine_required must be True")
        if not self.metadata_only:
            raise ValueError("metadata_only must be True")
        if self.direct_media_render_allowed:
            raise ValueError("direct_media_render_allowed must be False")
        if self.thumbnail_generation_allowed:
            raise ValueError("thumbnail_generation_allowed must be False")
        if self.ios_media_api_call_allowed:
            raise ValueError("ios_media_api_call_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
