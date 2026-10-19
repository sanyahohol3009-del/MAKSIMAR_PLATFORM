#!/usr/bin/env python3
"""Incident history log for MAKSIMAR safety foundation."""

from __future__ import annotations

import json
import os
import time
from typing import Any

from CORE_ROOT.runtime_paths import (
    INCIDENT_HISTORY_FILE,
    ensure_runtime_layout,
)

from CORE_ROOT.run_context import read_run_metadata


def write_incident_record(
    reason: str,
    status: str = "crashed",
) -> dict[str, Any]:
    """
    Append incident record to history log.
    """

    ensure_runtime_layout()

    meta = read_run_metadata()

    wall = time.time()
    mono = time.monotonic()

    payload: dict[str, Any] = {
        "timestamp_wall": wall,
        "timestamp_monotonic": mono,
        "reason": reason,
        "status": status,
    }

    if meta:
        payload["run_id"] = meta.get("run_id")
        payload["boot_id"] = meta.get("boot_id")

    from CORE_ROOT.run_context import runtime_mutation
    with runtime_mutation():
        with open(INCIDENT_HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
            f.flush()
            os.fsync(f.fileno())

    return payload


def read_incident_history() -> list[dict[str, Any]]:
    """
    Read full incident history.
    """

    ensure_runtime_layout()

    if not INCIDENT_HISTORY_FILE.exists():
        return []

    history: list[dict[str, Any]] = []

    with open(INCIDENT_HISTORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                history.append(json.loads(line))
            except Exception:
                continue

    return history


def _evidence_file_identity(path):
    """Read a regular original without following a replaced/symlinked path."""
    import hashlib
    import stat
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("runtime evidence must be a regular file")
        digest = hashlib.sha256()
        remaining = before.st_size
        while remaining:
            block = os.read(fd, min(1024 * 1024, remaining))
            if not block:
                raise RuntimeError("runtime evidence changed during inspection")
            digest.update(block)
            remaining -= len(block)
        if os.read(fd, 1):
            raise RuntimeError("runtime evidence changed during inspection")
        after = os.fstat(fd)
        fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns", "st_mode", "st_uid", "st_gid")
        identity = {key: getattr(before, key) for key in fields}
        if any(getattr(after, key) != value for key, value in identity.items()):
            raise RuntimeError("runtime evidence changed during inspection")
        current = os.stat(path, follow_symlinks=False)
        if any(getattr(current, key) != value for key, value in identity.items()):
            raise RuntimeError("runtime evidence path changed during inspection")
        return {**identity, "sha256": digest.hexdigest()}
    finally:
        os.close(fd)


def _fsync_evidence_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _verify_runtime_evidence_archive(directory, manifest):
    """Verify durable copied bytes; this never authorizes source removal."""
    import hashlib
    from pathlib import Path
    directory = Path(directory)
    for item in manifest["originals"]:
        copied = directory / item["archive_file"]
        if copied.is_symlink() or not copied.is_file():
            raise RuntimeError("runtime evidence archive entry missing or unsafe")
        digest = hashlib.sha256()
        with copied.open("rb") as handle:
            while block := handle.read(1024 * 1024):
                digest.update(block)
        if digest.hexdigest() != item["identity"]["sha256"] or copied.stat().st_size != item["identity"]["st_size"]:
            raise RuntimeError("runtime evidence archive readback mismatch")


def preserve_runtime_evidence(paths, *, archive_root=None, expected_identities=None, reuse_verified=False):
    """Preserve raw originals locally; no cleanup, incident or health authority.

    This non-destructive snapshot is NOT a reconciliation transaction. A caller
    still needs complete writer coordination and fresh identity checks before
    any later effect. Partial archives remain private; originals stay in place.
    """
    import stat
    import uuid
    from pathlib import Path
    originals = [Path(path).absolute() for path in paths]
    if not originals or len(set(originals)) != len(originals):
        raise ValueError("nonempty unique evidence paths required")
    identities = {str(path): _evidence_file_identity(path) for path in originals}
    if expected_identities is not None and identities != expected_identities:
        raise RuntimeError("runtime evidence no longer matches inspected originals")
    root = Path(archive_root) if archive_root is not None else INCIDENT_HISTORY_FILE.parent / "incident_evidence"
    # Existing parent is intentional: no implicit runtime layout or store setup.
    created_root = False
    try:
        root.mkdir(mode=0o700)
        created_root = True
    except FileExistsError:
        pass
    st = root.lstat()
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) & 0o077:
        raise RuntimeError("runtime evidence archive root is not a private owned directory")
    if created_root:
        _fsync_evidence_directory(root.parent)
    if reuse_verified:
        # Reuse only exact originals already durably retained by this owner.
        # No separate index/registry; malformed or partial evidence is retained.
        for existing in sorted(root.iterdir()):
            if existing.is_symlink() or not existing.is_dir() or existing.name.startswith(".partial_"):
                continue
            try:
                saved = json.loads((existing / "manifest.json").read_text(encoding="utf-8"))
                items = saved["originals"]
                retained = {item["origin"]: item["identity"] for item in items}
                if any(retained.get(origin) != identity for origin, identity in identities.items()):
                    continue
                if len(items) != len(retained) or any(
                        item["archive_file"] != f"original_{index:04d}.bin"
                        for index, item in enumerate(items)):
                    continue
                _verify_runtime_evidence_archive(existing, saved)
                if any(_evidence_file_identity(source) != identities[str(source)] for source in originals):
                    raise RuntimeError("runtime evidence changed before archive reuse")
                return {"archive_path": str(existing), "manifest": saved,
                        "originals_retained": True, "safe_to_reconcile": False}
            except (OSError, ValueError, TypeError, KeyError):
                continue
    archive_id = uuid.uuid4().hex
    partial = root / (".partial_" + archive_id)
    partial.mkdir(mode=0o700)
    _fsync_evidence_directory(root)
    entries = []
    for index, source in enumerate(originals):
        identity = identities[str(source)]
        archive_name = f"original_{index:04d}.bin"
        target = partial / archive_name
        source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            current = os.fstat(source_fd)
            if any(getattr(current, key) != value for key, value in identity.items() if key != "sha256"):
                raise RuntimeError("runtime evidence changed before preservation")
            target_fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(target_fd, "wb") as handle:
                remaining = identity["st_size"]
                while remaining:
                    block = os.read(source_fd, min(1024 * 1024, remaining))
                    if not block:
                        raise RuntimeError("runtime evidence changed during preservation")
                    handle.write(block)
                    remaining -= len(block)
                if os.read(source_fd, 1):
                    raise RuntimeError("runtime evidence changed during preservation")
                handle.flush()
                os.fsync(handle.fileno())
        finally:
            os.close(source_fd)
        if _evidence_file_identity(source) != identity:
            raise RuntimeError("runtime evidence changed during preservation")
        entries.append({"origin": str(source), "archive_file": archive_name, "identity": identity})
    manifest = {"schema_version": 1, "timestamp_wall": time.time(),
                "timestamp_monotonic": time.monotonic(), "status": "originals_preserved",
                "originals": entries}
    manifest_path = partial / "manifest.json"
    with manifest_path.open("x", encoding="utf-8") as handle:
        os.chmod(manifest_path, 0o600)
        json.dump(manifest, handle, ensure_ascii=False, sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())
    readback = json.loads(manifest_path.read_text(encoding="utf-8"))
    if readback != manifest:
        raise RuntimeError("runtime evidence manifest readback mismatch")
    _verify_runtime_evidence_archive(partial, readback)
    if any(_evidence_file_identity(source) != identities[str(source)] for source in originals):
        raise RuntimeError("runtime evidence changed before archive commit")
    _fsync_evidence_directory(partial)
    committed = root / archive_id
    partial.rename(committed)
    _fsync_evidence_directory(root)
    return {"archive_path": str(committed), "manifest": manifest,
            "originals_retained": True, "safe_to_reconcile": False}
