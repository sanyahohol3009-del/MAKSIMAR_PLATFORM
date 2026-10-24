from __future__ import annotations

import importlib
from types import SimpleNamespace


def _patch_live_status_run():
    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )
    original_run = live_adapter.subprocess.run
    live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
        stdout="runtime: alive\nkernel: alive\nguard: alive\n",
        stderr="",
        returncode=0,
    )
    return live_adapter, original_run


def test_foundation_status_read_model_builds() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_read_model_contract"
        )
        read_model = module.build_foundation_status_read_model_contract()
        assert read_model is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_status_read_model_has_identity_or_content_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_read_model_contract"
        )
        read_model = module.build_foundation_status_read_model_contract()

        read_model_dict = read_model if isinstance(read_model, dict) else getattr(read_model, "__dict__", {})
        assert read_model_dict or hasattr(read_model, "contract_id") or hasattr(read_model, "view_id") or hasattr(read_model, "summary")
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_status_read_model_builds_under_failed_status_command_too() -> None:
    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )
    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="",
            stderr="boom",
            returncode=1,
        )

        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_read_model_contract"
        )
        read_model = module.build_foundation_status_read_model_contract()
        assert read_model is not None
    finally:
        live_adapter.subprocess.run = original_run
