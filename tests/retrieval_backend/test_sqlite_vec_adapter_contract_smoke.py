from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    SqliteVecAdapterContract,
    build_default_evidence_bound_retrieval_result,
    build_sqlite_vec_adapter_contract,
)


def test_sqlite_vec_adapter_contract_smoke() -> None:
    contract = build_sqlite_vec_adapter_contract()
    first = contract.to_read_model()
    second = contract.to_read_model()

    assert isinstance(contract, SqliteVecAdapterContract)
    assert first == second
    assert first["backend_kind"] == "sqlite_vec"
    assert first["contract_mode"] == "adapter_only"
    assert first["vector_metadata_adapter"] is True
    assert first["database_runtime_enabled"] is False
    assert first["direct_database_write_allowed"] is False
    assert first["direct_write_allowed"] is False
    assert first["source_of_truth"] is False
    assert first["output_requires_normalization"] is True
    assert first["source_ref_required"] is True
    assert first["evidence_binding_required"] is True
    assert first["runtime_mutation_allowed"] is False
    assert first["network_allowed_by_default"] is False
    assert first["vector_backend"]["backend_kind"] == "sqlite_vec"
    assert first["vector_backend"]["source_of_truth"] is False


def test_sqlite_vec_adapter_rejects_unsafe_flags() -> None:
    unsafe_values = (
        ("database_runtime_enabled", True),
        ("direct_database_write_allowed", True),
        ("direct_write_allowed", True),
        ("source_of_truth", True),
        ("output_requires_normalization", False),
        ("source_ref_required", False),
        ("evidence_binding_required", False),
        ("runtime_mutation_allowed", True),
        ("network_allowed_by_default", True),
    )

    for field_name, value in unsafe_values:
        with pytest.raises(ValueError, match=field_name):
            SqliteVecAdapterContract(**{field_name: value})


def test_sqlite_vec_adapter_validates_evidence_bound_output() -> None:
    contract = build_sqlite_vec_adapter_contract()
    result = build_default_evidence_bound_retrieval_result()

    assert contract.validate_output(result) is result
    with pytest.raises(TypeError, match="EvidenceBoundRetrievalResult"):
        contract.validate_output(object())  # type: ignore[arg-type]


def test_sqlite_vec_adapter_source_has_no_runtime_invocation_imports() -> None:
    source = Path("MAKSIMAR_CORE_LIB/retrieval_backend/sqlite_vec_adapter_contract.py").read_text(encoding="utf-8")

    assert "subprocess" not in source
    assert "sqlite3" not in source
    assert "connect(" not in source
    assert "docker" not in source.lower()
