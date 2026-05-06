from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_id_models import (
    StorageNodeId,
)


def test_storage_node_id_models_smoke() -> None:
    node_id = StorageNodeId("HSTORE-RAW-001")
    assert node_id.value == "HSTORE-RAW-001"


def test_storage_node_id_models_reject_wrong_format() -> None:
    with pytest.raises(ValueError, match="value must match STORAGE_NODE_ID_PATTERN"):
        StorageNodeId("RAW")
