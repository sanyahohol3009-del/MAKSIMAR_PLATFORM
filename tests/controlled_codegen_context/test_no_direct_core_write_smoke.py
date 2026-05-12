from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_preview


def test_no_direct_core_write_smoke() -> None:
    preview = build_codegen_preview()

    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed"] is False
    assert preview["sandbox_execution_allowed_now"] is False
    assert preview["self_expansion_allowed_now"] is False
    assert preview["productization_allowed_now"] is False
