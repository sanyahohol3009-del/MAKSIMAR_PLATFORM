from __future__ import annotations

from pathlib import Path
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_models import (
    HistoryStoreAcceptanceResult,
)


def _count_files(root: Path, pattern: str) -> int:
    return sum(1 for _ in root.rglob(pattern))


def build_history_store_acceptance_result(
    write_root_path: str,
) -> HistoryStoreAcceptanceResult:
    root = Path(write_root_path)

    session_manifest_count = _count_files(
        root / "registry" / "import_sessions",
        "*.json",
    )
    attachment_summary_count = _count_files(
        root / "registry" / "attachment_links",
        "*.json",
    )
    conversation_manifest_count = _count_files(
        root / "normalized_history" / "conversations",
        "conversation_manifest.json",
    )
    normalized_record_count = _count_files(
        root / "normalized_history" / "conversations",
        "normalized_record.json",
    )
    message_unit_count = sum(
        1
        for _ in (root / "normalized_history" / "conversations").rglob("message_units/*.json")
    )

    return HistoryStoreAcceptanceResult(
        session_manifest_count=session_manifest_count,
        attachment_summary_count=attachment_summary_count,
        conversation_manifest_count=conversation_manifest_count,
        normalized_record_count=normalized_record_count,
        message_unit_count=message_unit_count,
        store_acceptance_ready=True,
    )


def build_history_store_acceptance_preview(
    write_root_path: str,
) -> Dict[str, object]:
    result = build_history_store_acceptance_result(write_root_path)
    return {
        "session_manifest_count": result.session_manifest_count,
        "attachment_summary_count": result.attachment_summary_count,
        "conversation_manifest_count": result.conversation_manifest_count,
        "normalized_record_count": result.normalized_record_count,
        "message_unit_count": result.message_unit_count,
        "store_acceptance_ready": result.store_acceptance_ready,
    }
