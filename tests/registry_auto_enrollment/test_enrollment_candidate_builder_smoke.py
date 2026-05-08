from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_enrollment_candidate_contract,
)


def test_enrollment_candidate_builder_smoke() -> None:
    contract = build_enrollment_candidate_contract()

    assert contract.total_candidates == len(contract.candidates)
    assert contract.total_candidates == (
        contract.reuse_existing_manifest_candidates
        + contract.create_minimal_manifest_preview_candidates
    )

    for candidate in contract.candidates:
        assert candidate.candidate_ready is True
        if candidate.manifest_exists:
            assert candidate.enrollment_action == "reuse_existing_manifest"
        else:
            assert candidate.enrollment_action == "create_minimal_manifest_preview"
