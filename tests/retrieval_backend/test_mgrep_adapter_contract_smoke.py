from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    MgrepAdapterContract,
    build_default_evidence_bound_retrieval_result,
    build_mgrep_adapter_contract,
)


def test_mgrep_adapter_contract_smoke() -> None:
    contract = build_mgrep_adapter_contract()
    first = contract.to_read_model()
    second = contract.to_read_model()

    assert isinstance(contract, MgrepAdapterContract)
    assert first == second
    assert first["backend_kind"] == "mgrep"
    assert first["contract_mode"] == "adapter_only"
    assert first["local_file_search_adapter"] is True
    assert first["execution_allowed_now"] is False
    assert first["binary_execution_allowed"] is False
    assert first["output_requires_normalization"] is True
    assert first["source_ref_required"] is True
    assert first["evidence_binding_required"] is True
    assert first["source_of_truth"] is False
    assert first["direct_filesystem_mutation_allowed"] is False
    assert first["direct_canonical_write_allowed"] is False
    assert first["runtime_mutation_allowed"] is False
    assert first["network_allowed_by_default"] is False


def test_mgrep_adapter_rejects_unsafe_flags() -> None:
    unsafe_values = (
        ("execution_allowed_now", True),
        ("binary_execution_allowed", True),
        ("output_requires_normalization", False),
        ("source_ref_required", False),
        ("evidence_binding_required", False),
        ("source_of_truth", True),
        ("direct_filesystem_mutation_allowed", True),
        ("direct_canonical_write_allowed", True),
        ("runtime_mutation_allowed", True),
        ("network_allowed_by_default", True),
    )

    for field_name, value in unsafe_values:
        with pytest.raises(ValueError, match=field_name):
            MgrepAdapterContract(**{field_name: value})


def test_mgrep_adapter_validates_evidence_bound_output() -> None:
    contract = build_mgrep_adapter_contract()
    result = build_default_evidence_bound_retrieval_result()

    assert contract.validate_output(result) is result
    with pytest.raises(TypeError, match="EvidenceBoundRetrievalResult"):
        contract.validate_output(object())  # type: ignore[arg-type]


def test_mgrep_adapter_source_has_no_runtime_invocation_imports() -> None:
    source = Path("MAKSIMAR_CORE_LIB/retrieval_backend/mgrep_adapter_contract.py").read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "requests" not in source
    assert "docker" not in source.lower()
