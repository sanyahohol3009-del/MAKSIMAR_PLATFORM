from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.chat_command.media_attachment_contract import MediaAttachmentContract


_ALLOWED_MEDIA_RUNTIME_STATES = ("inspection_required", "quarantined_reference", "accepted_reference", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class MediaAttachmentRuntimeRecord:
    attachment_id: str
    message_id: str
    media_kind: str
    runtime_state: str
    scan_required: bool
    quarantine_required: bool
    direct_render_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "media_kind", _ensure_non_empty(self.media_kind, "media_kind"))

        if self.runtime_state not in _ALLOWED_MEDIA_RUNTIME_STATES:
            raise ValueError(f"runtime_state must be one of {_ALLOWED_MEDIA_RUNTIME_STATES}: {self.runtime_state}")
        if not self.scan_required:
            raise ValueError("scan_required must be True")
        if not self.quarantine_required:
            raise ValueError("quarantine_required must be True")
        if self.direct_render_allowed:
            raise ValueError("direct_render_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")


@dataclass
class MediaAttachmentRuntime:
    """In-memory media attachment runtime.

    It tracks media attachment references only. It does not render media, scan
    files, write files, upload/download data, or call external services.
    """

    _records: Dict[str, MediaAttachmentRuntimeRecord] = field(default_factory=dict)

    def register_attachment(self, contract: MediaAttachmentContract) -> MediaAttachmentRuntimeRecord:
        if contract.attachment_id in self._records:
            raise ValueError(f"attachment already registered: {contract.attachment_id}")

        record = MediaAttachmentRuntimeRecord(
            attachment_id=contract.attachment_id,
            message_id=contract.message_id,
            media_kind=contract.media_kind,
            runtime_state="inspection_required",
            scan_required=True,
            quarantine_required=True,
            direct_render_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[record.attachment_id] = record
        return record

    def mark_quarantined_reference(self, attachment_id: str) -> MediaAttachmentRuntimeRecord:
        current = self.get_record(attachment_id)
        quarantined = MediaAttachmentRuntimeRecord(
            attachment_id=current.attachment_id,
            message_id=current.message_id,
            media_kind=current.media_kind,
            runtime_state="quarantined_reference",
            scan_required=True,
            quarantine_required=True,
            direct_render_allowed=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
        )
        self._records[attachment_id] = quarantined
        return quarantined

    def get_record(self, attachment_id: str) -> MediaAttachmentRuntimeRecord:
        attachment_id = _ensure_non_empty(attachment_id, "attachment_id")
        try:
            return self._records[attachment_id]
        except KeyError as exc:
            raise KeyError(f"unknown media attachment: {attachment_id}") from exc

    def list_records(self) -> Tuple[MediaAttachmentRuntimeRecord, ...]:
        return tuple(self._records.values())
