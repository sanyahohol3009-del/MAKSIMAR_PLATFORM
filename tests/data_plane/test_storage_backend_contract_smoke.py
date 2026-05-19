from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.storage_backend_contract import (
    StorageBackendRegistry,
    build_postgres_main_descriptor,
    build_storage_backend_readiness_read_model,
)
from MAKSIMAR_CORE_LIB.data_plane.storage_backend_models import StorageBackendDescriptor


def test_postgres_main_storage_backend_descriptor_is_policy_gated() -> None:
    backend = build_postgres_main_descriptor(
        backend_id="postgres_main_metadata",
        endpoint_ref="secret-ref://postgres/main",
    )
    read_model = build_storage_backend_readiness_read_model(backend)

    assert backend.backend_kind.value == "postgres_main"
    assert backend.canonical_write_allowed is False
    assert backend.heavy_payload_in_control_path_allowed is False
    assert read_model.backend_kind == "postgres_main"
    assert read_model.status == "policy_gated"


def test_storage_backend_registry_requires_unique_ids() -> None:
    backend = build_postgres_main_descriptor(
        backend_id="postgres_main_metadata",
        endpoint_ref="secret-ref://postgres/main",
    )
    registry = StorageBackendRegistry(registry_id="data_plane_storage_registry", backends=(backend,))

    assert registry.require_backend("postgres_main_metadata") is backend

    with pytest.raises(ValueError, match="unique"):
        StorageBackendRegistry(registry_id="bad", backends=(backend, backend))


def test_storage_backend_descriptor_rejects_canonical_write() -> None:
    with pytest.raises(ValueError, match="canonical_write_allowed"):
        StorageBackendDescriptor(
            backend_id="bad",
            backend_kind=backend_kind_for_test(),
            status=status_for_test(),
            endpoint_ref="secret-ref://bad",
            capability_ids=("bad",),
            reason_codes=("bad",),
            canonical_write_allowed=True,
        )


def backend_kind_for_test():
    from MAKSIMAR_CORE_LIB.data_plane.storage_backend_models import StorageBackendKind

    return StorageBackendKind.POSTGRES_MAIN


def status_for_test():
    from MAKSIMAR_CORE_LIB.data_plane.storage_backend_models import StorageBackendStatus

    return StorageBackendStatus.POLICY_GATED
