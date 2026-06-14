from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


CUBE_DIR = Path("CONTAINER_DEPLOYMENT/cubes/retrieval_backend")
CONTAINER_CONTRACT = CUBE_DIR / "container_contract.yaml"
RUNTIME_PROFILE = CUBE_DIR / "runtime_profile.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_retrieval_backend_container_contract_is_declarative_only() -> None:
    assert CONTAINER_CONTRACT.exists()
    assert RUNTIME_PROFILE.exists()

    contract = _load_yaml(CONTAINER_CONTRACT)
    assert contract["cube_id"] == "retrieval_backend"
    assert contract["container_ready"] is True
    assert contract["runtime_enabled"] is False
    assert contract["docker_required_now"] is False
    assert contract["network_allowed_by_default"] is False
    assert contract["source_of_truth"] is False
    assert contract["direct_canonical_write_allowed"] is False
    assert contract["runtime_mutation_allowed"] is False
    assert contract["execution_allowed_now"] is False
    assert contract["direct_execution_allowed"] is False
    assert contract["approval_required_before_runtime"] is True
    assert contract["vendor_gate_required_before_real_backend"] is True
    assert contract["evidence_binding_required"] is True
    assert contract["source_ref_required"] is True
    assert contract["output_requires_normalization"] is True
    assert contract["read_model_source"] == "MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_status_read_model.py"
    assert contract["preview_tool"] == "tools/retrieval_backend_status_preview.py"


def test_retrieval_backend_runtime_profile_keeps_all_backends_disabled() -> None:
    profile = _load_yaml(RUNTIME_PROFILE)

    assert profile["runtime_profile_id"] == "retrieval_backend_runtime_profile_v1"
    assert profile["runtime_enabled"] is False
    assert profile["backend_execution_enabled"] is False
    assert profile["mgrep_enabled"] is False
    assert profile["sqlite_vec_enabled"] is False
    assert profile["qdrant_enabled"] is False
    assert profile["qdrant_container_enabled"] is False
    assert profile["docker_runtime_enabled"] is False
    assert profile["network_allowed_by_default"] is False
    assert profile["read_only_preview_allowed"] is True
    assert profile["source_of_truth"] is False
    assert profile["direct_canonical_write_allowed"] is False
    assert profile["runtime_mutation_allowed"] is False
    assert profile["execution_allowed_now"] is False
    assert profile["direct_execution_allowed"] is False
    assert profile["output_requires_normalization"] is True
    assert profile["source_ref_required"] is True
    assert profile["evidence_binding_required"] is True
