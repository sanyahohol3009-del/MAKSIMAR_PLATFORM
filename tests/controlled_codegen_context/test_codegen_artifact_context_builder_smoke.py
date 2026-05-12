from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_artifact_context


def test_codegen_artifact_context_builder_smoke() -> None:
    context = build_codegen_artifact_context()

    assert context["artifact_context_ready"] is True
    assert context["missing_surfaces"] == ()
    assert context["artifact_reference_required"] is True
    assert context["artifact_ownership_required"] is True
    assert context["direct_core_write_allowed"] is False
