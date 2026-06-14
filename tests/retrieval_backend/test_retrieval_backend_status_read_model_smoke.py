from __future__ import annotations

import importlib
import json

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalBackendStatusReadModel,
    build_retrieval_backend_status_read_model,
    build_retrieval_backend_status_read_model_json,
)


def test_retrieval_backend_status_read_model_is_deterministic() -> None:
    first = build_retrieval_backend_status_read_model()
    second = build_retrieval_backend_status_read_model()

    assert first.to_read_model() == second.to_read_model()
    assert first.to_json() == second.to_json()
    assert first.to_json() == build_retrieval_backend_status_read_model_json()

    payload = json.loads(first.to_json())
    assert list(payload) == sorted(payload)
    assert payload["configured_backend_kinds"] == ["mgrep", "sqlite_vec", "qdrant"]
    assert [adapter["backend_kind"] for adapter in payload["adapter_statuses"]] == [
        "mgrep",
        "sqlite_vec",
        "qdrant",
    ]


def test_retrieval_backend_status_read_model_reports_all_required_flags() -> None:
    read_model = build_retrieval_backend_status_read_model().to_read_model()

    assert read_model["mode"] == "read_model_preview_only"
    assert read_model["source_of_truth"] is False
    assert read_model["output_requires_normalization"] is True
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["execution_allowed_now"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_canonical_write_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["preview_read_only"] is True

    by_kind = {adapter["backend_kind"]: adapter for adapter in read_model["adapter_statuses"]}
    assert set(by_kind) == {"mgrep", "sqlite_vec", "qdrant"}
    assert by_kind["qdrant"]["network_service_adapter_candidate"] is True
    assert by_kind["qdrant"]["runtime_container_required_now"] is False
    assert by_kind["qdrant"]["qdrant_server_required_now"] is False

    for adapter in by_kind.values():
        assert adapter["source_of_truth"] is False
        assert adapter["output_requires_normalization"] is True
        assert adapter["source_ref_required"] is True
        assert adapter["evidence_binding_required"] is True
        assert adapter["execution_allowed_now"] is False
        assert adapter["runtime_mutation_allowed"] is False
        assert adapter["direct_canonical_write_allowed"] is False
        assert adapter["direct_execution_allowed"] is False
        assert adapter["network_allowed_by_default"] is False


def test_retrieval_backend_status_read_model_rejects_runtime_enabled_state() -> None:
    current = build_retrieval_backend_status_read_model()

    with pytest.raises(ValueError, match="execution_allowed_now"):
        RetrievalBackendStatusReadModel(
            read_model_id=current.read_model_id,
            mode=current.mode,
            adapter_statuses=current.adapter_statuses,
            execution_allowed_now=True,
        )


def test_retrieval_backend_status_preview_is_read_only(monkeypatch, capsys) -> None:
    subprocess_module = importlib.import_module("subprocess")
    socket_module = importlib.import_module("socket")

    def forbidden_call(*args: object, **kwargs: object) -> None:
        raise AssertionError("preview must not execute processes or open sockets")

    monkeypatch.setattr(subprocess_module, "run", forbidden_call)
    monkeypatch.setattr(subprocess_module, "Popen", forbidden_call)
    monkeypatch.setattr(socket_module.socket, "connect", forbidden_call, raising=False)

    from tools import retrieval_backend_status_preview

    assert retrieval_backend_status_preview.main() == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload == json.loads(build_retrieval_backend_status_read_model_json())
    assert payload["execution_allowed_now"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["direct_canonical_write_allowed"] is False
    assert payload["network_allowed_by_default"] is False
