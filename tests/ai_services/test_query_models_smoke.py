from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.ai_services.query_models import AIServiceQuery
from MAKSIMAR_CORE_LIB.ai_services.service_models import AIServiceDefinition
from MAKSIMAR_CORE_LIB.ai_services.service_summary import build_service_summary


def test_build_service_summary_matches_service_ids() -> None:
    """Retrieval summary should match by service_id substring."""
    definitions = [
        AIServiceDefinition(
            service_id="qwen_service",
            version="qwen_service.v1",
            file_path=Path("qwen_service.yaml"),
            payload={},
        ),
        AIServiceDefinition(
            service_id="glm_service",
            version="glm_service.v1",
            file_path=Path("glm_service.yaml"),
            payload={},
        ),
    ]

    query = AIServiceQuery(query_text="qwen", limit=10)
    summary = build_service_summary(query, definitions)

    assert summary.total_matches == 1
    assert len(summary.returned_items) == 1
    assert summary.returned_items[0].service_id == "qwen_service"


def test_build_service_summary_respects_limit() -> None:
    """Retrieval summary should respect query limit."""
    definitions = [
        AIServiceDefinition(
            service_id="qwen_service",
            version="qwen_service.v1",
            file_path=Path("qwen_service.yaml"),
            payload={},
        ),
        AIServiceDefinition(
            service_id="glm_service",
            version="glm_service.v1",
            file_path=Path("glm_service.yaml"),
            payload={},
        ),
    ]

    query = AIServiceQuery(query_text="service", limit=1)
    summary = build_service_summary(query, definitions)

    assert summary.total_matches == 2
    assert len(summary.returned_items) == 1
