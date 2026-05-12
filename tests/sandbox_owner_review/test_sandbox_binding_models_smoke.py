from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_binding


def test_sandbox_binding_models_smoke() -> None:
    binding = build_sandbox_binding()

    assert binding["sandbox_binding_ready"] is True
    assert binding["missing_surfaces"] == ()
    assert binding["sandbox_contract_visible"] is True
    assert binding["patch_contract_visible"] is True
    assert binding["sandbox_execution_started_here"] is False
