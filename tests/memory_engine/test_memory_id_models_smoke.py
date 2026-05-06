from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_id_models import (
    MemoryObjectId,
)


def test_memory_id_models_smoke() -> None:
    obj = MemoryObjectId(
        prefix="ARCH",
        numeric_id=1,
        value="ARCH-0001",
    )
    assert obj.value == "ARCH-0001"


def test_memory_id_models_reject_wrong_format() -> None:
    with pytest.raises(ValueError, match="value must match MEMORY_ID_PATTERN"):
        MemoryObjectId(
            prefix="ARCH",
            numeric_id=1,
            value="BAD",
        )
