from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
)
from MAKSIMAR_SERVER.DATA_PLANE.data_plane_append_log_adapter import (
    DataPlaneAppendLogAdapterResult,
    append_payload_reference_to_log,
)


def write_append_only_payload_reference(
    *,
    log_path: Path,
    stream_id: str,
    payload_reference: DataPlanePayloadReference,
    created_at_utc: str,
) -> DataPlaneAppendLogAdapterResult:
    return append_payload_reference_to_log(
        log_path=log_path,
        stream_id=stream_id,
        payload_reference=payload_reference,
        created_at_utc=created_at_utc,
    )
