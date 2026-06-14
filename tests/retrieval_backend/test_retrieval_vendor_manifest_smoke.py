from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MANIFEST = Path("EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backend_manifest.yaml")


def _load_manifest() -> dict[str, Any]:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_retrieval_vendor_manifest_declares_sources_without_runtime() -> None:
    payload = _load_manifest()

    assert payload["runtime_enabled"] is False
    assert payload["install_allowed"] is False
    assert payload["download_allowed_now"] is False
    assert payload["direct_execution_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["source_of_truth"] is False
    assert payload["vendor_gate_required"] is True
    assert payload["scanner_required_before_runtime"] is True
    assert payload["license_review_required_before_runtime"] is True

    backends = payload["backends"]
    assert backends["sqlite_vec"]["source_url"] == "https://github.com/asg017/sqlite-vec"
    assert backends["sqlite_vec"]["vendor_gate_required"] is True
    assert backends["sqlite_vec"]["runtime_enabled"] is False
    assert backends["sqlite_vec"]["write_allowed"] is False
    assert backends["sqlite_vec"]["source_of_truth"] is False

    assert backends["qdrant"]["source_url"] == "https://github.com/qdrant/qdrant"
    assert backends["qdrant"]["vendor_gate_required"] is True
    assert backends["qdrant"]["runtime_enabled"] is False
    assert backends["qdrant"]["network_allowed_by_default"] is False
    assert backends["qdrant"]["qdrant_server_required_now"] is False
    assert backends["qdrant"]["qdrant_container_enabled"] is False
    assert backends["qdrant"]["source_of_truth"] is False

    assert backends["mgrep"]["source_url"] == "unresolved_until_verified"
    assert backends["mgrep"]["vendor_gate_required"] is True
    assert backends["mgrep"]["runtime_enabled"] is False
    assert backends["mgrep"]["fail_closed_until_source_verified"] is True
    assert backends["mgrep"]["source_of_truth"] is False
