from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_readonly_tool_route,
    build_retrieval_runtime_readonly_availability,
    inspect_mgrep_readonly_availability,
    inspect_qdrant_readonly_availability,
    inspect_sqlite_vec_readonly_availability,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_retrieval_runtime_readonly_availability_is_source_bound_and_read_only() -> None:
    availability = build_retrieval_runtime_readonly_availability(PROJECT_ROOT)
    read_model = [item.to_read_model() for item in availability]

    assert [item["backend_kind"] for item in read_model] == ["mgrep", "sqlite_vec", "qdrant"]
    assert all(item["source_present"] is True for item in read_model)
    assert all(item["read_only"] is True for item in read_model)
    assert all(item["direct_execution_allowed"] is False for item in read_model)
    assert all(item["canonical_write_allowed"] is False for item in read_model)
    assert all(item["runtime_mutation_allowed"] is False for item in read_model)
    assert all(item["network_allowed_by_default"] is False for item in read_model)
    assert all(item["docker_required_now"] is False for item in read_model)


def test_mgrep_readonly_fails_closed_without_built_executable() -> None:
    status = inspect_mgrep_readonly_availability(PROJECT_ROOT).to_read_model()

    assert status["source_present"] is True
    assert status["selected_tool"] in {"mgrep_readonly", "repo_search"}
    if status["usable_now"] is False:
        assert status["selected_tool"] == "repo_search"
        assert "dist/index.js" in str(status["unavailable_reason"])


def test_sqlite_vec_readonly_falls_back_without_local_extension() -> None:
    status = inspect_sqlite_vec_readonly_availability(PROJECT_ROOT).to_read_model()

    assert status["source_present"] is True
    assert status["selected_tool"] in {"sqlite_vec_readonly", "repo_search"}
    if status["usable_now"] is False:
        assert status["selected_tool"] == "repo_search"
        assert "loadable extension" in str(status["unavailable_reason"])


def test_qdrant_readonly_is_status_only_until_runtime_batch() -> None:
    status = inspect_qdrant_readonly_availability(PROJECT_ROOT).to_read_model()

    assert status["source_present"] is True
    assert status["usable_now"] is False
    assert status["selected_tool"] == "qdrant_readonly_status"
    assert status["fallback_tool"] == "retrieval_backend_status_read_model"
    assert status["qdrant_server_start_allowed"] is False


def test_readonly_tool_router_builds_deterministic_fallback_chains() -> None:
    search_route = build_retrieval_readonly_tool_route(
        "PROJECT_SEARCH",
        ("mgrep_readonly", "repo_search", "read_file_snippet"),
        PROJECT_ROOT,
    ).to_read_model()
    similar_route = build_retrieval_readonly_tool_route(
        "SEMANTIC_SIMILARITY",
        ("sqlite_vec_readonly", "repo_search", "qdrant_readonly"),
        PROJECT_ROOT,
    ).to_read_model()
    qdrant_route = build_retrieval_readonly_tool_route(
        "RETRIEVAL_BACKEND_STATUS",
        ("qdrant_readonly_status", "retrieval_backend_status_read_model"),
        PROJECT_ROOT,
    ).to_read_model()

    assert search_route["selected_tool_chain"][0] == "mgrep_readonly"
    assert search_route["effective_tool"] in search_route["selected_tool_chain"]
    assert similar_route["selected_tool_chain"][0] == "sqlite_vec_readonly"
    assert similar_route["effective_tool"] in similar_route["selected_tool_chain"]
    assert qdrant_route["primary_tool"] == "qdrant_readonly_status"
    assert qdrant_route["effective_tool"] == "qdrant_readonly_status"
    assert all(route["read_only"] is True for route in (search_route, similar_route, qdrant_route))
    assert all(route["direct_execution_allowed"] is False for route in (search_route, similar_route, qdrant_route))
