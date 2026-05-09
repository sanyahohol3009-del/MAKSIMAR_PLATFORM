from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    RetrievalSourceBinding,
    build_default_retrieval_request,
    build_default_retrieval_scope,
    select_retrieval_sources,
)


def test_retrieval_policy_blocks_forbidden_source_smoke() -> None:
    request = build_default_retrieval_request()
    scope = build_default_retrieval_scope()

    forbidden_source = RetrievalSourceBinding(
        source_id="retrieval_source_forbidden_binary",
        source_kind="raw_binary_payload",
        memory_domain="project_history",
        registry_ref="forbidden://raw_binary",
        priority=1,
        evidence_supported=True,
        trace_supported=True,
        policy_allowed=True,
        backend_adapter_required=False,
    )

    with pytest.raises(ValueError, match="no retrieval sources selected"):
        select_retrieval_sources(request, scope, (forbidden_source,))
