from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.affected_file_binding_models import (
    AffectedFileBinding,
)


def test_affected_file_preview_smoke() -> None:
    binding = AffectedFileBinding(
        memory_id="ARCH-0001",
        file_path="CORE_ROOT/core_guard.py",
        binding_ready=True,
    )

    assert binding.file_path == "CORE_ROOT/core_guard.py"
