from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


class AtomicIOError(RuntimeError):
    """Raised when atomic I/O operation fails."""


def _ensure_parent_directory(path: Path) -> None:
    """Ensure target parent directory exists.

    Args:
        path: Target file path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Atomically write text file.

    Write process:
    1. create temp file in target directory
    2. write content
    3. flush + fsync
    4. replace target file

    Args:
        path: Final destination file path.
        content: Text content.
        encoding: File encoding.

    Raises:
        AtomicIOError: If write fails.
    """
    _ensure_parent_directory(path)

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            dir=path.parent,
            prefix=f"{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_path = Path(temp_file.name)

        os.replace(temp_path, path)
    except OSError as exc:
        raise AtomicIOError(f"Atomic text write failed for: {path}") from exc
    finally:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def atomic_write_json(path: Path, payload: dict[str, Any], *, indent: int = 2) -> None:
    """Atomically write JSON object.

    Args:
        path: Final destination path.
        payload: JSON-serializable mapping.
        indent: JSON indentation.
    """
    serialized = json.dumps(payload, ensure_ascii=False, indent=indent, sort_keys=False)
    atomic_write_text(path, serialized + "\n")


def atomic_write_yaml(path: Path, payload: dict[str, Any]) -> None:
    """Atomically write YAML object.

    Args:
        path: Final destination path.
        payload: YAML-serializable mapping.
    """
    serialized = yaml.safe_dump(
        payload,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    atomic_write_text(path, serialized)


def safe_read_text(path: Path, encoding: str = "utf-8") -> str:
    """Safely read text file.

    Args:
        path: File path.
        encoding: File encoding.

    Returns:
        File content.

    Raises:
        AtomicIOError: If file cannot be read.
    """
    try:
        return path.read_text(encoding=encoding)
    except OSError as exc:
        raise AtomicIOError(f"Failed to read text file: {path}") from exc


def safe_read_json(path: Path) -> dict[str, Any]:
    """Safely read JSON object.

    Args:
        path: JSON file path.

    Returns:
        Parsed mapping.

    Raises:
        AtomicIOError: If file cannot be read or parsed.
    """
    raw = safe_read_text(path)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AtomicIOError(f"Invalid JSON file: {path}") from exc

    if not isinstance(parsed, dict):
        raise AtomicIOError(f"Expected JSON object at: {path}")

    return parsed


def safe_read_yaml(path: Path) -> dict[str, Any]:
    """Safely read YAML object.

    Args:
        path: YAML file path.

    Returns:
        Parsed mapping.

    Raises:
        AtomicIOError: If file cannot be read or parsed.
    """
    raw = safe_read_text(path)
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise AtomicIOError(f"Invalid YAML file: {path}") from exc

    if not isinstance(parsed, dict):
        raise AtomicIOError(f"Expected YAML mapping at: {path}")

    return parsed
