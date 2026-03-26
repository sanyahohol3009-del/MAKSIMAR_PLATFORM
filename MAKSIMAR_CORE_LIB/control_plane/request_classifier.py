from __future__ import annotations

import re

from MAKSIMAR_CORE_LIB.control_plane.router_models import (
    IncomingRequest,
    RouteDecision,
)


def _extract_words(text: str) -> set[str]:
    """Extract normalized words from request text."""
    return set(re.findall(r"[a-zA-Z_]+", text.lower()))


def classify_request(request: IncomingRequest) -> RouteDecision:
    """Classify incoming request into routing target."""
    words = _extract_words(request.query_text)

    # AI service
    if words & {"analyze", "explain", "generate", "ai"}:
        return RouteDecision(
            target="ai_service",
            confidence=0.9,
            reason="matched_ai_keywords",
        )

    # voice
    if words & {"voice", "speak", "say", "audio"}:
        return RouteDecision(
            target="voice",
            confidence=0.9,
            reason="matched_voice_keywords",
        )

    # workflow
    if words & {"process", "workflow", "steps", "pipeline"}:
        return RouteDecision(
            target="workflow",
            confidence=0.85,
            reason="matched_workflow_keywords",
        )

    # action
    if words & {"run", "execute", "do", "start"}:
        return RouteDecision(
            target="action",
            confidence=0.85,
            reason="matched_action_keywords",
        )

    return RouteDecision(
        target="unknown",
        confidence=0.0,
        reason="no_match",
    )
