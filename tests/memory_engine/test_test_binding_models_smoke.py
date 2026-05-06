from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_test_binding_models import (
    MemoryTestBinding,
)


def test_test_binding_models_smoke() -> None:
    binding = MemoryTestBinding(
        memory_id="ARCH-0001",
        test_ref="tests/runtime_core/test_core_guard.py",
        binding_ready=True,
    )

    assert binding.binding_ready is True
