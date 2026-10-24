from __future__ import annotations

import pytest

from CONTROL_PLANE.api_server import jarvis_live_tools
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import resolve_existing_capability


@pytest.mark.parametrize(
    ("capability_id", "kind"),
    (
        ("external_adapter:n8n", "external_adapter"),
        ("external_adapter:mempalace", "external_adapter"),
        ("external_adapter:smolagents", "external_adapter"),
    ),
)
def test_typed_registry_resolves_external_adapter_ids(capability_id: str, kind: str) -> None:
    """Migrated requirement: resolve typed registry IDs, never paraphrases."""
    payload = resolve_existing_capability(capability_id)
    assert payload["capability_id"] == capability_id
    assert payload["capability_kind"] == kind
    assert payload["selection_enabled"] is True


def test_typed_registry_resolves_mempalace_adapter_id() -> None:
    payload = resolve_existing_capability("external_adapter:mempalace")
    assert payload["capability_id"] == "external_adapter:mempalace"
    assert payload["capability_kind"] == "external_adapter"


def test_typed_registry_resolves_retrieval_and_runtime_tooling_ids() -> None:
    for capability_id, kind in (
        ("retrieval_backend:mgrep", "retrieval_backend"),
        ("retrieval_backend:qdrant", "retrieval_backend"),
        ("runtime_tooling:flutter", "runtime_tooling"),
    ):
        payload = resolve_existing_capability(capability_id)
        assert payload["capability_id"] == capability_id
        assert payload["capability_kind"] == kind


def test_tools_endpoint_uses_dispatcher_truth_for_new_capability_families() -> None:
    payload = jarvis_live_tools()
    external_ids = {item["capability_id"] for item in payload["external_adapters"]}
    retrieval_ids = {item["capability_id"] for item in payload["retrieval_backends"]}
    runtime_tooling_ids = {item["capability_id"] for item in payload["runtime_tooling"]}
    assert {"external_adapter:smolagents", "external_adapter:n8n", "external_adapter:mempalace"} <= external_ids
    assert {"retrieval_backend:mgrep", "retrieval_backend:qdrant", "retrieval_backend:sqlite_vec"} <= retrieval_ids
    assert "runtime_tooling:flutter" in runtime_tooling_ids
