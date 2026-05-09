from __future__ import annotations

from pathlib import Path


def test_evidence_memory_no_server_import_smoke() -> None:
    root = Path("MAKSIMAR_CORE_LIB/evidence_memory")

    for path in root.rglob("*.py"):
        content = path.read_text(encoding="utf-8")
        assert "MAKSIMAR_SERVER" not in content
