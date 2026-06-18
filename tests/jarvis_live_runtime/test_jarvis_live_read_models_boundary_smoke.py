from __future__ import annotations

import inspect

from tools.jarvis_live_runtime import jarvis_live_brain_loop
from tools.jarvis_live_runtime import jarvis_live_read_models


def test_brain_loop_uses_extracted_read_model_facade() -> None:
    assert inspect.getmodule(jarvis_live_brain_loop.build_project_workspace_read_model).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_read_models"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.model_runtime_status).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_read_models"
    )
    assert inspect.getmodule(jarvis_live_brain_loop.build_jarvis_live_tool_catalog_read_model).__name__ == (
        "tools.jarvis_live_runtime.jarvis_live_read_models"
    )


def test_read_models_remain_read_only() -> None:
    payload = jarvis_live_read_models.build_jarvis_live_project_status_read_model()
    assert payload["read_only"] is True
    assert payload["pc_control_allowed"] is False
    assert payload["canonical_memory_write_allowed"] is False


def test_memory_federation_read_model_blocks_mutation() -> None:
    payload = jarvis_live_read_models.build_jarvis_live_memory_federation_status()
    assert payload["memory_federation_available"] is True
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False
