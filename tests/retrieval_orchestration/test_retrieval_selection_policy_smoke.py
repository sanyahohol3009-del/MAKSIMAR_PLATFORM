from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_default_retrieval_request,
    build_default_retrieval_scope,
    build_default_retrieval_source_bindings,
    select_retrieval_sources,
)


def test_retrieval_selection_policy_smoke() -> None:
    request = build_default_retrieval_request()
    scope = build_default_retrieval_scope()
    sources = build_default_retrieval_source_bindings()

    selected = select_retrieval_sources(request, scope, sources)

    assert selected
    assert tuple(source.priority for source in selected) == tuple(
        sorted(source.priority for source in selected)
    )
