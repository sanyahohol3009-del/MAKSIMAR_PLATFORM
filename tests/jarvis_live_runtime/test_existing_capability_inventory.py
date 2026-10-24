from __future__ import annotations

from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
    build_existing_capability_inventory,
    build_existing_capability_catalog,
    build_existing_capability_inventory_summary,
    resolve_existing_capability,
)


def test_existing_capability_inventory_exposes_expected_capability_families() -> None:
    inventory = build_existing_capability_inventory()
    summary = build_existing_capability_inventory_summary()
    by_id = {item["capability_id"]: item for item in inventory}

    assert summary["inventory_id"] == "existing_capability_inventory_v2"
    assert summary["total_capabilities"] >= 20
    assert by_id["close_opera"]["capability_kind"] == "pc_action"
    assert by_id["close_opera"]["direct_allowed"] is True
    assert by_id["build_jarvis_live_tool_catalog_read_model"]["capability_kind"] == "readonly_tool"
    assert by_id["session_memory"]["capability_kind"] == "memory_tool"
    assert "protected_mutation_gate" not in by_id
    assert by_id["external_adapter:smolagents"]["capability_kind"] == "external_adapter"
    assert by_id["external_adapter:n8n"]["capability_kind"] == "external_adapter"
    assert by_id["external_adapter:mempalace"]["capability_kind"] == "external_adapter"
    assert by_id["retrieval_backend:qdrant"]["capability_kind"] == "retrieval_backend"
    assert by_id["runtime_tooling:flutter"]["capability_kind"] == "runtime_tooling"
    assert by_id["jarvis_runtime_library:agents"]["capability_kind"] == "jarvis_runtime_library"


def test_existing_inventory_groups_typed_records_and_blocks_unknown_ids() -> None:
    catalog = build_existing_capability_catalog()
    unknown = resolve_existing_capability("missing_capability")

    assert catalog["source"] == "existing_capability_inventory"
    assert len(catalog["direct_pc_actions"]) >= 1
    assert len(catalog["readonly_tools"]) >= 1
    assert len(catalog["memory_tools"]) >= 1
    assert len(catalog["retrieval_tools"]) >= 1
    assert unknown["status"] == "blocked_unknown_capability"
