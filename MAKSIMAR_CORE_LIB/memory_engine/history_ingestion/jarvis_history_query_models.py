from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from datetime import datetime, timezone, timedelta


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class JarvisHistoryQuery:
    query_text: str
    query_scope: str
    query_ready: bool
    query_kind: str = "HISTORY"
    time_basis: str = "ANY_TIME"
    time_start: str = ""
    time_end: str = ""

    def __post_init__(self) -> None:
        query_text = _ensure_non_empty_str(self.query_text, "query_text")
        query_scope = _ensure_non_empty_str(self.query_scope, "query_scope")
        if not self.query_ready:
            raise ValueError("query_ready must be True")

        object.__setattr__(self, "query_text", query_text)
        object.__setattr__(self, "query_scope", query_scope)
        if self.query_kind not in {"HISTORY", "VERIFIED_EXPERIENCE", "VERIFIED_SIMULATION", "PROVENANCE", "REVIEW_STATUS"}:
            raise ValueError("unsupported memory query kind")
        if self.time_basis not in {"ANY_TIME", "TODAY_UTC", "EXPLICIT_RANGE"}:
            raise ValueError("unsupported memory time basis")
        if self.time_basis == "TODAY_UTC":
            start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            object.__setattr__(self, "time_start", start.isoformat())
            object.__setattr__(self, "time_end", (start + timedelta(days=1)).isoformat())
        if self.time_basis == "ANY_TIME" and (self.time_start or self.time_end):
            raise ValueError("ANY_TIME cannot carry bounds")
        if self.time_basis != "ANY_TIME":
            start, end = self.bounds()
            if start >= end:
                raise ValueError("memory time range must be increasing")

    def bounds(self) -> tuple[datetime, datetime]:
        values = tuple(datetime.fromisoformat(v.replace("Z", "+00:00")) for v in (self.time_start, self.time_end))
        if any(v.tzinfo is None for v in values):
            raise ValueError("memory time bounds must include timezone")
        return values


MEMORY_FILTER_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["query_kind", "time_basis", "time_start", "time_end"],
    "properties": {
        "query_kind": {"type": "string", "enum": ["HISTORY", "VERIFIED_EXPERIENCE", "VERIFIED_SIMULATION", "PROVENANCE", "REVIEW_STATUS"],
                       "description": "Requested memory object: HISTORY=user/assistant utterances; VERIFIED_EXPERIENCE=actually completed work qualified by execution evidence and review; VERIFIED_SIMULATION=qualified simulation; PROVENANCE=experience origin including pending; REVIEW_STATUS=experience review including pending. A conversation mentioning work is not proof of completed work."},
        "time_basis": {"type": "string", "enum": ["ANY_TIME", "TODAY_UTC", "EXPLICIT_RANGE"],
                       "description": "Semantic time restriction. TODAY_UTC is normalized by the platform UTC clock; never invent dates."},
        "time_start": {"type": "string", "description": "Timezone-aware ISO date for EXPLICIT_RANGE only; otherwise empty."},
        "time_end": {"type": "string", "description": "Exclusive timezone-aware ISO end for EXPLICIT_RANGE only; otherwise empty."},
    },
}


# Separate input contracts for two existing owners, within the same role schema.
HISTORY_MEMORY_FILTER_SCHEMA = deepcopy(MEMORY_FILTER_SCHEMA)
SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA = deepcopy(MEMORY_FILTER_SCHEMA)
SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA["properties"]["query_kind"] = {"type": "string", "const": "SOURCE_DOCUMENT"}
SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA["properties"]["time_basis"] = {"type": "string", "const": "ANY_TIME"}
for field in ("time_start", "time_end"):
    SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA["properties"][field] = {"type": "string", "const": ""}
MEMORY_FILTER_SCHEMA["properties"]["query_kind"]["enum"].append("SOURCE_DOCUMENT")
MEMORY_FILTER_SCHEMA["properties"]["query_kind"]["description"] += (
    " SOURCE_DOCUMENT=actual indexed document/source knowledge with source/index provenance, not a prior completed task."
)
MEMORY_FILTER_SCHEMA["anyOf"] = [HISTORY_MEMORY_FILTER_SCHEMA, SOURCE_DOCUMENT_MEMORY_FILTER_SCHEMA]


def validate_memory_filter(value: object) -> dict[str, str]:
    """Validate semantic role/time fields without inventing event timestamps."""
    if not isinstance(value, dict) or set(value) != set(MEMORY_FILTER_SCHEMA["required"]):
        raise ValueError("memory_filter_fields_invalid")
    if not all(isinstance(item, str) for item in value.values()):
        raise ValueError("memory_filter_field_type_invalid")
    if value["time_basis"] != "EXPLICIT_RANGE" and (value["time_start"] or value["time_end"]):
        raise ValueError("memory_filter_non_range_has_bounds")
    if value["query_kind"] == "SOURCE_DOCUMENT":
        if value["time_basis"] != "ANY_TIME" or value["time_start"] or value["time_end"]:
            raise ValueError("source_document_temporal_filter_not_supported")
        return dict(value)
    JarvisHistoryQuery(query_text="semantic filter validation", query_scope="local_project_history",
                       query_ready=True, **value)
    return dict(value)
