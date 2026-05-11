from __future__ import annotations

import json

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    write_mempalace_real_backend_approval_envelope_report,
)


def test_mempalace_real_backend_approval_report_written_smoke() -> None:
    path = write_mempalace_real_backend_approval_envelope_report()

    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["approval_envelope_ready"] is True
    assert payload["controlled_real_backend_probe_allowed"] is True
    assert payload["full_real_backend_enablement_allowed"] is False
    assert payload["general_real_backend_query_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
