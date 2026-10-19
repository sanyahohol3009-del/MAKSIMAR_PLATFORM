from __future__ import annotations

import hashlib
import json
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    ConversationPort,
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    IdentityContext,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)


class ExistingConversationEvidenceAdapter(ConversationPort):
    """Server-owned evidence adapter for conversation on the canonical semantic spine."""

    provider_id = "existing_jarvis_final_brain"
    evidence_collector_id = "existing_conversation_evidence_adapter"

    def health(self) -> dict[str, Any]:
        return {"provider_id": self.provider_id, "status": "AVAILABLE", "project_tools_used": False}

    def collect_evidence(
        self,
        understanding: RequestUnderstanding,
        plan: ExecutionPlan,
        trace_id: str,
        identity: IdentityContext,
        session_context: dict[str, Any],
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        if deadline is not None and deadline.cancelled:
            return EvidenceBundle(
                request_id=understanding.request_id, capability_id="conversation.respond", trace_id=trace_id,
                status="UNAVAILABLE", items=(), limitations=("request deadline exceeded",),
                receipts=(), errors=("conversation_context:total_deadline",),
            )
        identity_facts = {
            "identity_id": identity.identity_id,
            "display_name": identity.display_name,
            "profile_type": identity.profile_type,
            "verified": identity.trusted,
            "assistant_identity": identity.assistant_identity,
            "grounding_rule": "use_only_supplied_identity_facts",
        }
        observations = (
            ("identity_facts", identity_facts, "identity://resolved-context"),
            ("bounded_session_context", session_context, "session://bounded-relevant-turns"),
        )
        items = []
        for kind, payload, source_reference in observations:
            serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
            items.append(EvidenceItem(
                kind=kind, source=f"{self.evidence_collector_id}:{kind}", observation=serialized,
                scope="conversation", confidence=1.0, trace_id=trace_id, observed_at=utc_observed_at(),
                content_hash=f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}",
                source_reference=source_reference, truncated=bool(session_context.get("truncated", False)),
                omitted_count=int(session_context.get("omitted_turn_count", 0)) if kind == "bounded_session_context" else 0,
                request_id=understanding.request_id,
                step_id=plan.steps[0].step_id, capability_id="conversation.respond",
                operation_id=plan.steps[0].operation, provider_id=self.evidence_collector_id,
            ))
        context_truncated = bool(session_context.get("truncated", False))
        omitted_turn_count = int(session_context.get("omitted_turn_count", 0))
        limitations = (
            ("conversation context truncated to bounded recent turns",)
            if context_truncated or omitted_turn_count > 0 else ()
        )
        return EvidenceBundle(
            request_id=understanding.request_id, capability_id="conversation.respond", trace_id=trace_id,
            status="COMPLETE", items=tuple(items), limitations=limitations,
            receipts=(), errors=(),
        )
