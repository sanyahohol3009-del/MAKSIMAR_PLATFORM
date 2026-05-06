from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_writer import (
    execute_live_import_write,
)


def build_live_import_write_summary(
    import_root_path: str,
    write_root_path: str,
) -> Dict[str, object]:
    result = execute_live_import_write(
        import_root_path=import_root_path,
        write_root_path=write_root_path,
    )
    return {
        "session_manifest_written": result.session_manifest_written,
        "conversation_manifests_written": result.conversation_manifests_written,
        "normalized_records_written": result.normalized_records_written,
        "message_units_written": result.message_units_written,
        "attachment_root_count": result.attachment_root_count,
        "repeat_write_safe": result.repeat_write_safe,
        "write_ready": result.write_ready,
    }
