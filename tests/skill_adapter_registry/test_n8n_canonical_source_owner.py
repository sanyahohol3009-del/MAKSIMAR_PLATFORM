from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import existing_capability_inventory as inventory


def test_n8n_registry_source_provenance_comes_from_existing_execution_owner():
    records = inventory._scan_external_adapters({"adapters": ()})
    record = next(x for x in records if x.capability_id == "workflow_automation:n8n")
    assert inventory.N8N_ROOT == n8n_adapter._N8N_ROOT
    assert record.external_path == str(n8n_adapter._N8N_ROOT)
    assert record.status == ("available" if n8n_adapter._N8N_ROOT.exists() else "external_not_found")
