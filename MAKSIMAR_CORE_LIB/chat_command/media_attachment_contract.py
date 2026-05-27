from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_MEDIA_KINDS = ("image", "audio", "video", "document", "binary")
_ALLOWED_ATTACHMENT_STATES = ("declared", "scan_required", "quarantined", "accepted_reference", "blocked")


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
class MediaAttachmentContract:
    """Canonical media attachment contract.

    Contract only. It does not render media, scan files, upload files, download
    files, or call OpenIM/mobile/server APIs.
    """

    attachment_id: str
    message_id: str
    media_kind: str
    mime_type: str
    filename: str
    storage_ref: str
    attachment_state: str
    scan_required: bool
    quarantine_required: bool
    direct_render_allowed: bool
    external_network_access_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "media_kind", _ensure_allowed(self.media_kind, "media_kind", _ALLOWED_MEDIA_KINDS))
        object.__setattr__(self, "mime_type", _ensure_non_empty(self.mime_type, "mime_type"))
        object.__setattr__(self, "filename", _ensure_non_empty(self.filename, "filename"))
        object.__setattr__(self, "storage_ref", _ensure_non_empty(self.storage_ref, "storage_ref"))
        object.__setattr__(
            self,
            "attachment_state",
            _ensure_allowed(self.attachment_state, "attachment_state", _ALLOWED_ATTACHMENT_STATES),
        )

        if not self.scan_required:
            raise ValueError("scan_required must be True")
        if not self.quarantine_required:
            raise ValueError("quarantine_required must be True")
        if self.direct_render_allowed:
            raise ValueError("direct_render_allowed must be False until scan/runtime gates approve")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
