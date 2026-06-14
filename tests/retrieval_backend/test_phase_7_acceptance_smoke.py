from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from MAKSIMAR_CORE_LIB.retrieval_backend import build_retrieval_backend_status_read_model


PHASE_7_1_FILES = (
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_adapter_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/vector_backend_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/semantic_search_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/evidence_binding_contract.py"),
)
PHASE_7_2_FILES = (
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_policy_gate_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/mgrep_adapter_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/sqlite_vec_adapter_contract.py"),
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/qdrant_adapter_contract.py"),
)
PHASE_7_3_FILES = (
    Path("MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_backend_status_read_model.py"),
    Path("tools/retrieval_backend_status_preview.py"),
    Path("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml"),
)
ACCEPTANCE_DOC = Path("docs/architecture/retrieval_backend/phase_7_retrieval_backend_acceptance_v1.md")
CONTAINER_CONTRACT = Path("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/container_contract.yaml")
RUNTIME_PROFILE = Path("CONTAINER_DEPLOYMENT/cubes/retrieval_backend/runtime_profile.yaml")
PREVIEW_TOOL = Path("tools/retrieval_backend_status_preview.py")


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_phase_7_expected_files_exist() -> None:
    for path in PHASE_7_1_FILES + PHASE_7_2_FILES + PHASE_7_3_FILES + (ACCEPTANCE_DOC,):
        assert path.exists(), f"missing PHASE 7 acceptance surface: {path}"


def test_phase_7_status_read_model_acceptance_flags() -> None:
    read_model = build_retrieval_backend_status_read_model().to_read_model()
    adapters = {adapter["backend_kind"]: adapter for adapter in read_model["adapter_statuses"]}

    assert tuple(adapters) == ("mgrep", "sqlite_vec", "qdrant")
    assert read_model["source_of_truth"] is False
    assert read_model["execution_allowed_now"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_canonical_write_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False

    for adapter in adapters.values():
        assert adapter["source_of_truth"] is False
        assert adapter["source_ref_required"] is True
        assert adapter["evidence_binding_required"] is True
        assert adapter["output_requires_normalization"] is True
        assert adapter["execution_allowed_now"] is False
        assert adapter["runtime_mutation_allowed"] is False
        assert adapter["direct_canonical_write_allowed"] is False
        assert adapter["direct_execution_allowed"] is False
        assert adapter["network_allowed_by_default"] is False

    qdrant = adapters["qdrant"]
    assert qdrant["network_service_adapter_candidate"] is True
    assert qdrant["runtime_container_required_now"] is False
    assert qdrant["qdrant_server_required_now"] is False


def test_phase_7_container_contract_and_runtime_profile_remain_disabled() -> None:
    contract = _load_yaml(CONTAINER_CONTRACT)
    runtime_profile = _load_yaml(RUNTIME_PROFILE)

    assert contract["cube_id"] == "retrieval_backend"
    assert contract["container_ready"] is True
    assert contract["runtime_enabled"] is False
    assert contract["docker_required_now"] is False
    assert contract["network_allowed_by_default"] is False
    assert contract["source_of_truth"] is False
    assert contract["direct_canonical_write_allowed"] is False
    assert contract["runtime_mutation_allowed"] is False
    assert contract["execution_allowed_now"] is False
    assert contract["vendor_gate_required_before_real_backend"] is True
    assert contract["evidence_binding_required"] is True
    assert contract["source_ref_required"] is True
    assert contract["output_requires_normalization"] is True

    assert runtime_profile["runtime_enabled"] is False
    assert runtime_profile["backend_execution_enabled"] is False
    assert runtime_profile["mgrep_enabled"] is False
    assert runtime_profile["sqlite_vec_enabled"] is False
    assert runtime_profile["qdrant_enabled"] is False
    assert runtime_profile["qdrant_container_enabled"] is False
    assert runtime_profile["docker_runtime_enabled"] is False
    assert runtime_profile["network_allowed_by_default"] is False
    assert runtime_profile["read_only_preview_allowed"] is True


def test_phase_7_preview_tool_has_no_execution_surface() -> None:
    text = PREVIEW_TOOL.read_text(encoding="utf-8")
    forbidden_markers = (
        "subprocess",
        "requests",
        "httpx",
        "aiohttp",
        "socket",
        "docker",
        "qdrant",
        "/api/",
        "Popen",
    )

    for marker in forbidden_markers:
        assert marker not in text


def test_phase_7_acceptance_document_records_closure() -> None:
    text = ACCEPTANCE_DOC.read_text(encoding="utf-8")

    required_markers = (
        "PHASE 7.1 Retrieval Core Contracts",
        "PHASE 7.2 Retrieval Adapter Contracts",
        "PHASE 7.3 Retrieval Read Model / Container",
        "Retrieval Vendor Acquisition / Tool Enablement",
        "source_ref",
        "evidence_binding",
        "runtime_enabled=false",
        "docker_required_now=false",
        "qdrant_container_enabled=false",
        "vendor gate",
    )
    for marker in required_markers:
        assert marker in text
