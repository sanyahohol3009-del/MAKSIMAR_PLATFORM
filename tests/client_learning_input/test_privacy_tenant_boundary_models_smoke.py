from __future__ import annotations

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_privacy_tenant_boundary_preview


def test_privacy_tenant_boundary_models_smoke() -> None:
    preview = build_privacy_tenant_boundary_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_required_surfaces"] == ()
    assert preview["tenant_isolation_required"] is True
    assert preview["personal_data_redaction_required"] is True
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["raw_payload_storage_allowed"] is False
