from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.storage_backend_contract import (
    StorageBackendRegistry,
    build_postgres_main_descriptor,
)
from MAKSIMAR_SERVER.DATA_PLANE.adapters.existing_storage_registry_adapter import (
    bind_existing_storage_registry,
)


def test_existing_storage_registry_adapter_is_reference_only() -> None:
    backend = build_postgres_main_descriptor(
        backend_id="postgres_main_metadata",
        endpoint_ref="secret-ref://postgres/main",
    )
    registry = StorageBackendRegistry(
        registry_id="data_plane_storage_registry",
        backends=(backend,),
    )

    binding = bind_existing_storage_registry(registry)

    assert binding.reference_only is True
    assert binding.backend_count == 1
    assert binding.canonical_write_allowed is False
    assert binding.direct_execution_allowed is False


def test_existing_storage_registry_adapter_rejects_wrong_registry() -> None:
    with pytest.raises(TypeError, match="registry"):
        bind_existing_storage_registry(object())  # type: ignore[arg-type]
