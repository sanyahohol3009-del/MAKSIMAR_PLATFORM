"""Non-destructive raw retention draft; never a reconciliation authorization."""
import hashlib
import json
import os
import stat
from pathlib import Path

import pytest
from CORE_ROOT import incident_history as history


@pytest.fixture
def originals(tmp_path):
    files = [tmp_path / "heartbeat.json", tmp_path / "incident.jsonl"]
    contents = [b'{"status":"alive"}\xff\x00', b'corrupt historical JSON\n']
    for path, data in zip(files, contents):
        path.write_bytes(data)
    return files, contents, tmp_path / "private_archive"


def assert_originals(files, contents):
    assert [p.read_bytes() for p in files] == contents


def test_raw_original_bytes_hash_origin_and_private_readback(originals):
    files, contents, root = originals
    expected = {str(p): history._evidence_file_identity(p) for p in files}
    result = history.preserve_runtime_evidence(files, archive_root=root, expected_identities=expected)
    assert result["originals_retained"] is True and result["safe_to_reconcile"] is False
    directory = Path(result["archive_path"])
    manifest = json.loads((directory / "manifest.json").read_text())
    assert manifest["status"] == "originals_preserved"
    assert [n["origin"] for n in manifest["originals"]] == [str(p) for p in files]
    assert stat.S_IMODE(root.stat().st_mode) == stat.S_IMODE(directory.stat().st_mode) == 0o700
    for item, data in zip(manifest["originals"], contents):
        copied = directory / item["archive_file"]
        assert copied.read_bytes() == data
        assert item["identity"]["sha256"] == hashlib.sha256(data).hexdigest()
        assert stat.S_IMODE(copied.stat().st_mode) == 0o600
    assert_originals(files, contents)


@pytest.mark.parametrize("bad", ["missing", "symlink", "fifo", "duplicate", "empty"])
def test_missing_or_unsafe_source_fails_without_original_loss(originals, bad):
    files, contents, root = originals
    if bad == "missing":
        selected = [files[0].parent / "missing"]
    elif bad in {"symlink", "fifo"}:
        path = files[0].parent / bad
        if bad == "symlink": path.symlink_to(files[0])
        else: os.mkfifo(path)
        selected = [path]
    else:
        selected = [files[0], files[0]] if bad == "duplicate" else []
    with pytest.raises((OSError, ValueError)):
        history.preserve_runtime_evidence(selected, archive_root=root)
    assert_originals(files, contents)
    assert not root.exists()


@pytest.mark.parametrize("unsafe_root", ["public", "symlink"])
def test_archive_root_must_be_owned_private_directory(originals, unsafe_root):
    files, contents, root = originals
    if unsafe_root == "public":
        root.mkdir(); root.chmod(0o777)
    else:
        other = root.parent / "other"; other.mkdir(); root.symlink_to(other, target_is_directory=True)
    with pytest.raises(RuntimeError, match="private owned"):
        history.preserve_runtime_evidence(files, archive_root=root)
    assert_originals(files, contents)


def test_changed_expected_identity_refuses_before_archive(originals):
    files, contents, root = originals
    expected = {str(p): history._evidence_file_identity(p) for p in files}
    expected[str(files[0])]["sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="no longer matches"):
        history.preserve_runtime_evidence(files, archive_root=root, expected_identities=expected)
    assert_originals(files, contents)
    assert not root.exists()


@pytest.mark.parametrize("change", ["inode", "content"])
def test_source_replaced_after_first_inspection_is_refused(originals, monkeypatch, change):
    files, contents, root = originals
    real = history._evidence_file_identity
    once = []
    def inspect(path):
        result = real(path)
        if Path(path) == files[-1] and not once:
            once.append(True)
            if change == "inode":
                replacement = root.parent / "replacement"; replacement.write_bytes(contents[0]); replacement.replace(files[0])
            else:
                files[0].write_bytes(b"new writer content")
        return result
    monkeypatch.setattr(history, "_evidence_file_identity", inspect)
    with pytest.raises(RuntimeError, match="changed"):
        history.preserve_runtime_evidence(files, archive_root=root)
    assert files[0].read_bytes() == (contents[0] if change == "inode" else b"new writer content")
    assert files[1].read_bytes() == contents[1]


@pytest.mark.parametrize("failure_index", [1, 2, 3, 4, 5])
def test_durable_write_failures_leave_all_originals(originals, monkeypatch, failure_index):
    files, contents, root = originals
    real = os.fsync; count = []
    def fsync(fd):
        count.append(fd)
        if len(count) == failure_index: raise OSError("synthetic durability failure")
        return real(fd)
    monkeypatch.setattr(history.os, "fsync", fsync)
    with pytest.raises(OSError, match="durability failure"):
        history.preserve_runtime_evidence(files, archive_root=root)
    assert_originals(files, contents)


@pytest.mark.parametrize("corruption", ["copied_bytes", "manifest", "interrupt"])
def test_readback_and_interruption_never_destroy_originals(originals, monkeypatch, corruption):
    files, contents, root = originals
    if corruption == "manifest":
        real = Path.read_text
        def read(path, *args, **kwargs):
            return "{}" if path.name == "manifest.json" else real(path, *args, **kwargs)
        monkeypatch.setattr(Path, "read_text", read)
    else:
        real = history._verify_runtime_evidence_archive
        def verify(directory, manifest):
            if corruption == "interrupt": raise KeyboardInterrupt("synthetic interruption")
            (directory / manifest["originals"][0]["archive_file"]).write_bytes(b"corrupted copy")
            return real(directory, manifest)
        monkeypatch.setattr(history, "_verify_runtime_evidence_archive", verify)
    with pytest.raises((RuntimeError, KeyboardInterrupt)):
        history.preserve_runtime_evidence(files, archive_root=root)
    assert_originals(files, contents)
    assert not any(p.name[0] != "." for p in root.iterdir())


def test_repeated_preservation_keeps_all_originals_and_makes_no_recovery_incident(originals, monkeypatch):
    files, contents, root = originals
    monkeypatch.setattr(history, "write_incident_record", lambda *a, **k: pytest.fail("false recovery incident"))
    results = [history.preserve_runtime_evidence(files, archive_root=root) for _ in range(2)]
    assert results[0]["archive_path"] != results[1]["archive_path"]
    assert all(r["safe_to_reconcile"] is False for r in results)
    assert_originals(files, contents)


@pytest.mark.parametrize("mutation", ["grow", "truncate"])
def test_identity_read_is_bounded_and_rejects_concurrent_size_change(originals, monkeypatch, mutation):
    files, contents, root = originals
    real = os.read
    changed = []
    def read(fd, size):
        if not changed and Path(os.readlink(f"/proc/self/fd/{fd}")) == files[0]:
            changed.append(True)
            files[0].write_bytes(contents[0] + b"growth" if mutation == "grow" else b"")
        return real(fd, size)
    monkeypatch.setattr(history.os, "read", read)
    with pytest.raises(RuntimeError, match="changed during inspection"):
        history.preserve_runtime_evidence(files, archive_root=root)
    assert changed and not root.exists()
    assert files[1].read_bytes() == contents[1]
