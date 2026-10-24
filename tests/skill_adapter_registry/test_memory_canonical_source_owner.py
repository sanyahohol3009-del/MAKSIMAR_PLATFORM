from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import existing_capability_inventory as inventory


def test_memory_view_descriptors_reference_canonical_source_module(monkeypatch):
    monkeypatch.setattr(inventory, "build_jarvis_live_memory_federation_status", lambda: {"surfaces":({"surface_id":"local_chat_memory", "status":"usable_now"},)})
    monkeypatch.setattr(inventory, "list_memory_definitions", lambda: ())
    monkeypatch.setattr(inventory, "_mempalace_ready", lambda: False)
    records = inventory._scan_memory_tools()
    record = next(r for r in records if r.capability_id == "local_chat_memory")
    assert record.import_path == "MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_context_sources"
    assert record.source_file_or_path == str(inventory.PROJECT_ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/memory_context_sources.py")
