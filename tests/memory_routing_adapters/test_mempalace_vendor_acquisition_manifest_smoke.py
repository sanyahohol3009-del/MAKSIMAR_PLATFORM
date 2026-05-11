from __future__ import annotations

import json
from pathlib import Path


def test_mempalace_vendor_acquisition_manifest_smoke() -> None:
    manifest_path = Path("EXTERNAL_BACKENDS/mempalace/manifests/mempalace_source_manifest.json")
    lock_path = Path("EXTERNAL_BACKENDS/mempalace/manifests/mempalace_version_lock.json")

    assert manifest_path.exists()
    assert lock_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lock = json.loads(lock_path.read_text(encoding="utf-8"))

    assert manifest["official_source_verified"] is True
    assert manifest["official_git_remote"] == "https://github.com/MemPalace/mempalace.git"
    assert manifest["external_code_not_committed"] is True
    assert manifest["canonical_memory_access"] is False
    assert manifest["runtime_mutation_allowed"] is False
    assert manifest["network_access_reviewed"] is True
    assert manifest["sandbox_data_only"] is True

    assert lock["version_or_commit_pinned"] is True
    assert lock["git_remote"] == "https://github.com/MemPalace/mempalace.git"
    assert lock["git_commit"]
    assert lock["separate_venv"] is True
    assert lock["external_code_not_committed"] is True
