from __future__ import annotations

import json

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    write_mempalace_read_only_routing_integration_report,
)


def test_mempalace_read_only_routing_report_smoke() -> None:
    path = write_mempalace_read_only_routing_integration_report()

    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["routing_integration_ready"] is True
    assert payload["read_only_routing_enabled"] is True
    assert payload["subordinate_backend"] is True
    assert payload["write_request_allowed_count"] == 0
    assert payload["write_routing_enabled"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
