from __future__ import annotations

from pathlib import Path


def test_jarvis_live_docs_context_mentions_required_controls() -> None:
    root = Path(__file__).resolve().parents[2]
    context = (
        root / "docs/architecture/jarvis_live/jarvis_live_layer_context_v0_1.md"
    ).read_text(encoding="utf-8")
    usage = (
        root / "docs/architecture/jarvis_live/jarvis_live_ci_guard_usage_v0_1.md"
    ).read_text(encoding="utf-8")
    combined = context + "\n" + usage

    for required in (
        "JL-0",
        "JL-1",
        "JL-2",
        "JL-10",
        "JL-11",
        "JL-14",
        "no new AI registry",
        "no new worker registry",
        "no new memory engine",
        "no raw shell",
        "allowlist",
        "approval",
        "model weights",
        "runtime assets",
        "memory_engine",
        "runtime_history_store",
    ):
        assert required in combined

