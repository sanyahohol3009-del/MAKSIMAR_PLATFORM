from __future__ import annotations

import importlib
from types import SimpleNamespace


def test_foundation_live_status_adapter_builds_snapshot_with_stubbed_status_command() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = module.subprocess.run
    try:
        module.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="runtime: alive\nkernel: alive\n",
            stderr="",
            returncode=0,
        )

        snapshot = module.build_foundation_live_status_snapshot()

        assert snapshot is not None
        assert hasattr(snapshot, "records")
        assert snapshot.records
    finally:
        module.subprocess.run = original_run


def test_foundation_live_status_adapter_record_shape_is_stable() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = module.subprocess.run
    try:
        module.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="runtime: alive\nkernel: alive\n",
            stderr="",
            returncode=0,
        )

        snapshot = module.build_foundation_live_status_snapshot()
        first_record = snapshot.records[0]

        assert hasattr(first_record, "truth_scope")
        assert hasattr(first_record, "status_command")
        assert hasattr(first_record, "command_succeeded")
    finally:
        module.subprocess.run = original_run


def test_foundation_live_status_adapter_handles_failed_command() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = module.subprocess.run
    try:
        module.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="",
            stderr="boom",
            returncode=1,
        )

        snapshot = module.build_foundation_live_status_snapshot()

        assert snapshot is not None
        assert hasattr(snapshot, "records")
        assert snapshot.records
    finally:
        module.subprocess.run = original_run
