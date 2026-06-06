from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_SERVER.AI_ORCHESTRATION.live_sandbox_vendor_boundary_contract import (
    ALLOWED_DOWNLOAD_CANDIDATE_IDS,
    ALLOWED_LIVE_SANDBOX_RUNTIME_ROOTS,
    APPROVED_VENDOR_CANDIDATE_IDS,
    LiveSandboxVendorBoundaryContract,
    build_live_sandbox_vendor_boundary_contract,
)


def test_live_sandbox_vendor_boundary_declares_runtime_only_candidates() -> None:
    read_model = build_live_sandbox_vendor_boundary_contract().to_read_model()

    assert read_model["approved_vendor_candidate_ids"] == (
        "ollama",
        "kokoro",
        "faster_whisper",
        "vision_ocr",
    )
    assert read_model["approved_vendor_candidate_ids"] == APPROVED_VENDOR_CANDIDATE_IDS
    assert read_model["allowed_download_candidate_ids"] == ALLOWED_DOWNLOAD_CANDIDATE_IDS
    assert "ollama_qwen2_5_coder_14b" in read_model["allowed_download_candidate_ids"]
    assert "kokoro_tts_candidate" in read_model["allowed_download_candidate_ids"]
    assert "faster_whisper_candidate" in read_model["allowed_download_candidate_ids"]
    assert "ocr_vision_candidate" in read_model["allowed_download_candidate_ids"]
    assert read_model["allowed_runtime_roots"] == ALLOWED_LIVE_SANDBOX_RUNTIME_ROOTS


def test_live_sandbox_vendor_boundary_blocks_repo_and_execution_surfaces() -> None:
    read_model = build_live_sandbox_vendor_boundary_contract().to_read_model()

    assert read_model["git_storage_allowed"] is False
    assert read_model["core_storage_allowed"] is False
    assert read_model["server_canonical_storage_allowed"] is False
    assert read_model["dashboard_storage_allowed"] is False
    assert read_model["memory_truth_write_allowed"] is False
    assert read_model["tests_storage_allowed"] is False
    assert read_model["docs_storage_allowed"] is False
    assert read_model["external_network_call_allowed"] is False
    assert read_model["actual_download_started"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["model_execution_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True


def test_live_sandbox_vendor_boundary_rejects_invalid_root_or_enabled_flag() -> None:
    boundary = build_live_sandbox_vendor_boundary_contract()

    with pytest.raises(ValueError, match="allowed_runtime_roots"):
        LiveSandboxVendorBoundaryContract(
            boundary_id="live_sandbox_vendor_boundary_contract_v0_1",
            approved_vendor_candidate_ids=boundary.approved_vendor_candidate_ids,
            allowed_download_candidate_ids=boundary.allowed_download_candidate_ids,
            allowed_runtime_roots=("MAKSIMAR_CORE_LIB/runtime_models/",),
            blocked_storage_targets=boundary.blocked_storage_targets,
        )
    with pytest.raises(ValueError, match="must remain disabled"):
        LiveSandboxVendorBoundaryContract(
            boundary_id="live_sandbox_vendor_boundary_contract_v0_1",
            approved_vendor_candidate_ids=boundary.approved_vendor_candidate_ids,
            allowed_download_candidate_ids=boundary.allowed_download_candidate_ids,
            allowed_runtime_roots=boundary.allowed_runtime_roots,
            blocked_storage_targets=boundary.blocked_storage_targets,
            actual_download_started=True,
        )


def test_live_sandbox_vendor_boundary_source_has_no_download_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root
        / "MAKSIMAR_SERVER/AI_ORCHESTRATION/live_sandbox_vendor_boundary_contract.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    for marker in (
        "requests",
        "httpx",
        "subprocess",
        "os.system",
        "curl",
        "wget",
        "ollama pull",
        "git clone",
        "pip install",
    ):
        assert marker not in lowered

