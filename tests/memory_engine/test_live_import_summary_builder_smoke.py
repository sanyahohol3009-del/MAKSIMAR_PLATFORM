from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_summary_builder import (
    build_live_import_summary,
)


def test_live_import_summary_builder_smoke() -> None:
    summary = build_live_import_summary(
        "runtime_imports/chatgpt_export_01",
    )
    assert summary["primary_source"] == "conversations.json"



def test_live_import_summary_and_attachment_counts_follow_existing_source_reader(tmp_path, monkeypatch):
    import json
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_summary_builder import build_live_import_summary
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_builder import build_message_attachment_linkage_result
    source = tmp_path / "conversations.json"
    # Reuse the canonical session DTO with a synthetic attachment identity.
    # Export-owner discovery is separate from this source-count regression.
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_models import LiveImportSession
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion import live_import_summary_builder as summary_owner
    from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion import message_attachment_linkage_builder as linkage_owner
    attachment = tmp_path / "user-fixture"
    attachment.mkdir()
    (attachment / "isolated.png").write_bytes(b"isolated reference fixture")
    session = LiveImportSession(
        session_id="fixture-session",
        source_manifest_path=str(tmp_path / "export_manifest.json"),
        source_conversations_path=str(source),
        conversation_count=1, attachment_roots=(str(attachment),),
        by_conversation_ready=True, whole_file_ready=True,
    )
    monkeypatch.setattr(summary_owner, "build_live_import_session", lambda _: session)
    monkeypatch.setattr(linkage_owner, "build_live_import_session", lambda _: session)
    for count in (1, 3):
        source.write_text(json.dumps([{"id": "isolated-conversation", "mapping": {
            str(i): {"message": {"author": {"role": "user"}}} for i in range(count)}}]))
        assert build_live_import_summary(str(tmp_path))["message_unit_count"] == count
        assert build_message_attachment_linkage_result(str(tmp_path)).message_unit_count == count
