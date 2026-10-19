from __future__ import annotations

from typing import Any, Dict
from datetime import datetime
from collections import Counter
import math

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_builders import (
    build_minimal_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.jarvis_history_query_models import (
    JarvisHistoryQuery,
)


def run_jarvis_history_query(
    query: JarvisHistoryQuery, records: tuple[dict[str, Any], ...] = (),
) -> Dict[str, object]:
    """Read supplied canonical durable projections; never use a fixture as live truth.

    The existing server owner supplies records across the core dependency boundary.
    No core-to-server import, second store, or independent index is introduced.
    """
    query_terms = _lexical_terms(query.query_text)
    matches: list[dict[str, Any]] = []
    unknown_time = 0
    for record in records:
        is_experience = bool(record.get("experience_id"))
        if query.query_kind != "HISTORY" and not is_experience:
            continue
        if query.query_kind in {"VERIFIED_EXPERIENCE", "VERIFIED_SIMULATION"} and (
            record.get("verification_status") != "VERIFIED"
            or record.get("review_status") not in {"REVIEWED", "EXECUTION_RECEIPTS_VERIFIED"}
        ):
            continue
        if query.query_kind == "VERIFIED_SIMULATION" and record.get("review_status") != "REVIEWED":
            continue
        if query.query_kind == "VERIFIED_SIMULATION" and record.get("artifact_kind") != "simulation_experience":
            continue
        if query.time_basis != "ANY_TIME":
            value = record.get("observed_at") or record.get("created_at") or ((record.get("timestamp") or record.get("persisted_at")) if not is_experience else "")
            try:
                stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    raise ValueError("unknown timezone")
            except ValueError:
                unknown_time += 1
                continue
            start, end = query.bounds()
            if not start <= stamp < end:
                continue
        searchable = " ".join(str(record.get(k, "")) for k in (
            "experience_id", "trace_id", "session_id", "user_text", "assistant_text", "topic", "task_ref", "experience_kind", "evidence_refs", "provenance_refs",
        ))
        matched_terms = tuple(sorted(query_terms.intersection(_lexical_terms(searchable))))
        if query.query_kind == "HISTORY" and not matched_terms:
            continue
        matches.append({**record, "memory_id": record.get("experience_id") or record.get("trace_id", ""),
                        "title": record.get("task_ref") or record.get("topic", ""), "matched_terms": matched_terms})
    content_scores = _qualified_content_scores(query.query_text, matches) if query.query_kind != "HISTORY" else {}
    # Retrieval ranking within already typed/qualified candidates is not intent
    # routing. Explicit identities rank first; ties prefer genuine source dates.
    def rank(item):
        try:
            stamp = datetime.fromisoformat(str(item.get("observed_at") or item.get("created_at") or item.get("timestamp") or (item.get("persisted_at") if not item.get("experience_id") else "") or "").replace("Z", "+00:00"))
            actual_time = stamp.timestamp() if stamp.tzinfo is not None else float("-inf")
        except (ValueError, OverflowError):
            actual_time = float("-inf")
        if query.query_kind == "HISTORY":
            return len(item["matched_terms"]), actual_time
        identity_match = any(str(item.get(key, "")).casefold() in query_terms
            for key in ("experience_id", "trace_id", "session_id") if item.get(key))
        return identity_match, content_scores.get(item["memory_id"], 0.0), len(item["matched_terms"]), actual_time
    matches.sort(key=rank, reverse=True)
    return {
        "query_text": query.query_text,
        "query_scope": query.query_scope,
        "matched_memory_ids": tuple(item["memory_id"] for item in matches),
        "matched_titles": tuple(item["title"] for item in matches),
        "matches": tuple(matches),
        "match_count": len(matches),
        "readable_by_jarvis": True,
        "retrieval_basis": "existing_canonical_durable_memory_projection",
        "query_kind": query.query_kind, "time_basis": query.time_basis,
        "time_start": query.time_start, "time_end": query.time_end, "time_zone": "UTC",
        "unknown_timestamp_records_excluded": unknown_time,
    }


def _qualified_content_scores(query_text: str, matches: list[dict[str, Any]]) -> dict[str, float]:
    """Rank already qualified records by corpus-weighted text overlap.

    Character features tolerate inflection without language-specific roots or
    command-word rules. This ephemeral calculation selects no capability,
    operation, provider or policy and creates no index or persistence world.
    Task descriptions carry content; receipt IDs cannot swamp their relevance.
    """
    def features(value: str) -> set[str]:
        normalized = " ".join("".join(c if c.isalnum() else " " for c in value.casefold()).split())
        return {normalized[i:i + size] for size in (3, 4, 5)
            for i in range(len(normalized) - size + 1) if " " not in normalized[i:i + size]}

    vectors = [features(str(item.get("task_ref") or item.get("topic") or item.get("user_text") or ""))
        for item in matches]
    frequencies = Counter(feature for vector in vectors for feature in vector)
    weights = {feature: math.log((1 + len(vectors)) / (1 + count)) + 1
        for feature, count in frequencies.items()}
    query = features(query_text)
    query_norm = math.sqrt(sum(weights.get(feature, 1.0) ** 2 for feature in query))
    scores = {}
    for item, vector in zip(matches, vectors):
        norm = math.sqrt(sum(weights[feature] ** 2 for feature in vector))
        overlap = sum(weights[feature] ** 2 for feature in query.intersection(vector))
        scores[item["memory_id"]] = overlap / (query_norm * norm) if query_norm and norm else 0.0
    return scores


def _lexical_terms(value: str) -> set[str]:
    normalized = "".join(character if character.isalnum() else " " for character in value.casefold())
    return {term for term in normalized.split() if len(term) >= 3}


def build_jarvis_history_query_preview() -> Dict[str, object]:
    query = JarvisHistoryQuery(
        query_text="runtime truth path",
        query_scope="project_history",
        query_ready=True,
    )
    # Explicit readiness preview only. This fixture is never the default live input.
    fixture = build_minimal_memory_object()
    result = run_jarvis_history_query(query, ({"trace_id": fixture.memory_id, "topic": fixture.title,
        "user_text": fixture.one_line_summary, "task_ref": fixture.title},))
    return {
        "query_text": result["query_text"],
        "query_scope": result["query_scope"],
        "match_count": int(result["match_count"]),
        "first_match_id": result["matched_memory_ids"][0],
        "readable_by_jarvis": result["readable_by_jarvis"],
    }
