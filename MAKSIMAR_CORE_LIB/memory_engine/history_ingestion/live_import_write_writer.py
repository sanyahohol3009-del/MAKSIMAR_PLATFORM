from __future__ import annotations

import json
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_builder import (
    build_live_import_write_plan,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_models import (
    LiveImportWriteResult,
)


def _write_json_if_missing(path: Path, payload: object) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return True


def execute_live_import_write(
    import_root_path: str,
    write_root_path: str,
) -> LiveImportWriteResult:
    plan = build_live_import_write_plan(import_root_path)
    write_root = Path(write_root_path)

    session_payload = plan["session"]
    session_id = session_payload["session_id"]

    session_manifest_path = (
        write_root / "registry" / "import_sessions" / f"{session_id}.json"
    )
    _write_json_if_missing(session_manifest_path, session_payload)

    conversation_manifests_written = 0
    normalized_records_written = 0
    message_units_written = 0

    for payload in plan["conversation_manifests"]:
        conversation_id = payload["conversation_id"]
        path = (
            write_root
            / "normalized_history"
            / "conversations"
            / conversation_id
            / "conversation_manifest.json"
        )
        if _write_json_if_missing(path, payload):
            conversation_manifests_written += 1

    for payload in plan["normalized_records"]:
        conversation_id = payload["conversation_id"]
        path = (
            write_root
            / "normalized_history"
            / "conversations"
            / conversation_id
            / "normalized_record.json"
        )
        if _write_json_if_missing(path, payload):
            normalized_records_written += 1

    for payload in plan["message_units"]:
        conversation_id = payload["conversation_id"]
        message_node_id = payload["message_node_id"]
        path = (
            write_root
            / "normalized_history"
            / "conversations"
            / conversation_id
            / "message_units"
            / f"{message_node_id}.json"
        )
        if _write_json_if_missing(path, payload):
            message_units_written += 1

    attachment_summary_path = (
        write_root / "registry" / "attachment_links" / f"{session_id}.json"
    )
    _write_json_if_missing(
        attachment_summary_path,
        {
            "session_id": session_id,
            "attachment_roots": plan["attachment_roots"],
            "attachment_root_count": len(plan["attachment_roots"]),
            "linkage_kind": "attachment_root_summary",
        },
    )

    return LiveImportWriteResult(
        session_manifest_written=True,
        conversation_manifests_written=conversation_manifests_written,
        normalized_records_written=normalized_records_written,
        message_units_written=message_units_written,
        attachment_root_count=len(plan["attachment_roots"]),
        repeat_write_safe=True,
        write_ready=True,
    )
