from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_source_version_chain_contract


def test_source_version_chain_models_smoke() -> None:
    contract = build_source_version_chain_contract()

    assert contract.total_versions == 6
    assert contract.ready_versions == contract.total_versions
