from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_request_models import (
    RetrievalRequest,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_scope_models import (
    RetrievalScope,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_source_binding_models import (
    RetrievalSourceBinding,
)


def select_retrieval_sources(
    request: RetrievalRequest,
    scope: RetrievalScope,
    sources: tuple[RetrievalSourceBinding, ...],
) -> tuple[RetrievalSourceBinding, ...]:
    """Select allowed sources for one retrieval request.

    This function is policy-only. It does not execute search and does not call
    any backend adapter.
    """

    if not sources:
        raise ValueError("sources must be non-empty")

    selected: list[RetrievalSourceBinding] = []

    for source in sources:
        if source.memory_domain not in scope.allowed_memory_domains:
            continue
        if source.source_kind not in scope.allowed_source_kinds:
            continue
        if source.source_kind in scope.forbidden_source_kinds:
            continue
        if not source.policy_allowed:
            continue
        if request.requested_domain != "any" and source.memory_domain != request.requested_domain:
            continue

        selected.append(source)

    if not selected:
        raise ValueError("no retrieval sources selected")

    return tuple(sorted(selected, key=lambda source: source.priority))
