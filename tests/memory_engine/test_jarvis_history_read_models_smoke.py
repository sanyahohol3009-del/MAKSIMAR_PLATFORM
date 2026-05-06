from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_read_models import (
    JarvisHistoryReadModel,
)


def test_jarvis_history_read_models_smoke() -> None:
    model = JarvisHistoryReadModel(
        memory_ids=("ARCH-0001",),
        titles=("Runtime truth path fixed",),
        readable_by_jarvis=True,
        context_ready=True,
    )

    assert model.readable_by_jarvis is True
