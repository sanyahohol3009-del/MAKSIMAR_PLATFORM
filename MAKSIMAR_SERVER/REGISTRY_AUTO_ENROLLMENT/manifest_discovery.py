from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT.existing_domain_inventory import (
    ExistingDomainInventoryContract,
    build_existing_domain_inventory,
)


_SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class ManifestDiscoveryEntry:
    """Read-only manifest discovery entry for an existing project domain."""

    module_slug: str
    source_path: str
    manifest_path: str
    manifest_exists: bool
    discovery_ready: bool

    def __post_init__(self) -> None:
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        manifest_path = _ensure_non_empty_str(self.manifest_path, "manifest_path")

        if not _SLUG_PATTERN.fullmatch(module_slug):
            raise ValueError(f"Invalid module_slug: {module_slug}")
        if not isinstance(self.manifest_exists, bool):
            raise ValueError("manifest_exists must be bool")
        if not isinstance(self.discovery_ready, bool):
            raise ValueError("discovery_ready must be bool")
        if not self.discovery_ready:
            raise ValueError("discovery_ready must be True")

        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "manifest_path", manifest_path)


@dataclass(frozen=True, slots=True)
class ManifestDiscoveryContract:
    """Read-only manifest discovery contract."""

    total_entries: int
    existing_manifest_entries: int
    missing_manifest_entries: int
    entries: tuple[ManifestDiscoveryEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        existing_manifest_entries = _ensure_non_negative_int(
            self.existing_manifest_entries,
            "existing_manifest_entries",
        )
        missing_manifest_entries = _ensure_non_negative_int(
            self.missing_manifest_entries,
            "missing_manifest_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        computed_existing = sum(1 for entry in self.entries if entry.manifest_exists)
        computed_missing = sum(1 for entry in self.entries if not entry.manifest_exists)

        if existing_manifest_entries != computed_existing:
            raise ValueError("existing_manifest_entries must match computed count")
        if missing_manifest_entries != computed_missing:
            raise ValueError("missing_manifest_entries must match computed count")
        if total_entries != existing_manifest_entries + missing_manifest_entries:
            raise ValueError("manifest discovery counts must balance")

        module_slugs = tuple(entry.module_slug for entry in self.entries)
        if len(set(module_slugs)) != len(module_slugs):
            raise ValueError("Duplicate module_slug values detected")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "existing_manifest_entries", existing_manifest_entries)
        object.__setattr__(self, "missing_manifest_entries", missing_manifest_entries)


def build_manifest_discovery_contract(
    project_root: Path | None = None,
    inventory: ExistingDomainInventoryContract | None = None,
) -> ManifestDiscoveryContract:
    """Build read-only manifest discovery result.

    This function does not create, update or delete manifests.
    """
    root = project_root or Path.cwd()
    selected_inventory = inventory or build_existing_domain_inventory(root)

    entries = tuple(
        ManifestDiscoveryEntry(
            module_slug=entry.domain_slug,
            source_path=entry.source_path,
            manifest_path=(Path(entry.source_path) / "manifest.json").as_posix(),
            manifest_exists=(root / entry.source_path / "manifest.json").exists(),
            discovery_ready=True,
        )
        for entry in selected_inventory.entries
    )

    return ManifestDiscoveryContract(
        total_entries=len(entries),
        existing_manifest_entries=sum(1 for entry in entries if entry.manifest_exists),
        missing_manifest_entries=sum(1 for entry in entries if not entry.manifest_exists),
        entries=entries,
    )
