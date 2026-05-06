from __future__ import annotations

from typing import Final, Literal, Tuple


ArchiveSourceType = Literal[
    "html",
    "pdf",
    "txt",
    "md",
    "json",
]

SUPPORTED_ARCHIVE_SOURCE_TYPES: Final[Tuple[ArchiveSourceType, ...]] = (
    "html",
    "pdf",
    "txt",
    "md",
    "json",
)
