from __future__ import annotations

import json
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    ModelUnderstandingPort, RequestDeadline, SOURCE_CANDIDATE_VERDICT_SCHEMA,
    validate_source_candidate_verdict,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_profiles,
    context_tokens_for_jarvis_model,
    resident_context_tokens_for_jarvis_model,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    HELPER_INPUT_CORRECTION_MODEL_ID,
    OLLAMA_CHAT_URL,
    OLLAMA_FAST_CHAT_THINK,
    OLLAMA_LIVE_MODEL_KEEP_ALIVE,
    PRIMARY_CONVERSATION_MODEL_ID,
    REQUEST_UNDERSTANDING_NUM_CTX,
    REQUEST_UNDERSTANDING_NUM_PREDICT,
    OPERATION_DISCOVERY_NUM_PREDICT,
    think_policy_for_model_id,
    model_role_for_model_id,
    build_model_call_timeout_truth,
    ollama_model_call_result,
    ollama_post_json,
    transport_clock_snapshot,
)
from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live.jarvis_live_observability_read_model import (
    trace_model_call_started, trace_model_call_completed, trace_stage,
)

try:
    import jsonschema as _jsonschema
except Exception:  # pragma: no cover - optional dependency fallback
    _jsonschema = None


def validate_structured_payload(content: Any, schema: dict[str, Any]) -> tuple[Any, bool, str]:
    """Parse + validate a structured model payload against its declared schema.

    Returns ``(parsed, valid, error)``. A model may violate a schema; the runtime must
    NEVER silently accept a malformed payload as valid. This shared validator enforces
    the full declared contract (type/required/enum/minItems/maxItems/additionalProperties
    and nested item schemas) using the shared jsonschema dependency, so no per-caller
    ``minItems`` hack is needed."""
    if _jsonschema is None:
        # Fail closed: we cannot verify the contract, so we must NOT declare it valid.
        if not isinstance(content, str):
            return None, False, "SCHEMA_VALIDATOR_UNAVAILABLE"
        try:
            parsed = json.loads(content)
        except Exception as exc:
            return None, False, f"json_parse_error:{type(exc).__name__}"
        return parsed, False, "SCHEMA_VALIDATOR_UNAVAILABLE"
    if not isinstance(content, str):
        return None, False, "content_not_string"
    try:
        parsed = json.loads(content)
    except Exception as exc:
        return None, False, f"json_parse_error:{type(exc).__name__}"
    try:
        _jsonschema.validate(instance=parsed, schema=schema)
    except _jsonschema.ValidationError as exc:
        return parsed, False, f"schema_validation_error:{exc.message}"
    return parsed, True, ""


HELPER_INPUT_CORRECTION_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": [
        "schema_version", "corrected_text", "ambiguity_candidates", "confidence",
        "reason_codes", "preserve_original", "no_change_needed",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": "helper_input_correction.v2"},
        "corrected_text": {"type": "string"},
        "ambiguity_candidates": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason_codes": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "preserve_original": {"type": "boolean", "const": True},
        "no_change_needed": {"type": "boolean"},
    },
}


def model_visible_structured_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Remove only predicates implied by an already validated exact const value.

    This is grammar serialization, not a new response schema: the SAME complete
    canonical schema remains the post-generation validator input on both attempts.
    Never traverse arbitrary instance values or reinterpret a selected value.
    """
    projected = json.loads(json.dumps(schema))
    if _jsonschema is None:
        return projected
    validator = _jsonschema.validators.validator_for(schema)(schema)

    def compact(node: Any) -> Any:
        if not isinstance(node, dict):
            return node
        if "const" in node:
            try:
                valid_const = validator.evolve(schema=node).is_valid(node["const"])
            except Exception:
                valid_const = False
            if valid_const:
                return {"const": node["const"]}
        for key in ("properties", "patternProperties", "$defs", "definitions", "dependentSchemas"):
            if isinstance(node.get(key), dict):
                node[key] = {name: compact(value) for name, value in node[key].items()}
        for key in ("items", "additionalProperties", "contains", "not", "if", "then", "else", "propertyNames"):
            if isinstance(node.get(key), dict):
                node[key] = compact(node[key])
        for key in ("anyOf", "oneOf", "allOf", "prefixItems"):
            if isinstance(node.get(key), list):
                node[key] = [compact(value) for value in node[key]]
        return node

    return compact(projected)


class ExistingOllamaModelUnderstandingAdapter(ModelUnderstandingPort):
    """Public semantic adapter over the existing local model transport and registry ID."""

    supports_call_scoped_understanding_schema = True

    def __init__(self, *, json_schema: dict[str, Any], candidate_json_schema: dict[str, Any] | None = None,
                 kind_json_schema: dict[str, Any] | None = None) -> None:
        self.json_schema = json_schema
        self.candidate_json_schema = candidate_json_schema
        self.kind_json_schema = kind_json_schema

    def discover_kinds(self, *, system_prompt: str, user_prompt: str, deadline: RequestDeadline,
                      output_schema: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._main_model_call(
            system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
            schema=output_schema or self.kind_json_schema, num_predict=256,
            # Compact discovery uses the canonical CHAT role context budget;
            # full understanding/repair retain the larger structured budget.
            num_ctx=resident_context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID),
            deadline_error="kind_discovery_deadline_exceeded",
        )

    def understand(self, *, system_prompt: str, user_prompt: str, deadline: RequestDeadline,
                   output_schema: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._main_model_call(
            system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
            schema=output_schema or self.json_schema, num_predict=REQUEST_UNDERSTANDING_NUM_PREDICT,
            num_ctx=REQUEST_UNDERSTANDING_NUM_CTX,
            deadline_error="understanding_deadline_exceeded",
        )

    def repair(self, *, system_prompt: str, user_prompt: str, deadline: RequestDeadline,
               output_schema: dict[str, Any] | None = None) -> dict[str, Any]:
        """The one allowed repair uses the same model, envelope, schema and transport."""
        return self._main_model_call(
            system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
            schema=output_schema or self.json_schema, num_predict=REQUEST_UNDERSTANDING_NUM_PREDICT,
            num_ctx=REQUEST_UNDERSTANDING_NUM_CTX,
            deadline_error="repair_deadline_exceeded",
        )

    def discover_candidates(self, *, system_prompt: str, user_prompt: str,
                            deadline: RequestDeadline,
                            output_schema: dict[str, Any] | None = None) -> dict[str, Any]:
        """Use the same main model for compact registry discovery, never the helper."""
        if self.candidate_json_schema is None:
            raise ValueError("candidate discovery schema unavailable")
        schema = output_schema or self.candidate_json_schema
        num_predict = OPERATION_DISCOVERY_NUM_PREDICT if "selection_justifications" in schema.get("properties", {}) else 256
        return self._main_model_call(
            system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
            schema=schema, num_predict=num_predict,
            num_ctx=resident_context_tokens_for_jarvis_model(PRIMARY_CONVERSATION_MODEL_ID),
            deadline_error="candidate_discovery_deadline_exceeded",
        )

    def verify_source_candidate(self, *, source_text: str, candidate: dict[str, Any],
                                deadline: RequestDeadline) -> dict[str, Any]:
        """Verification-only registered role through the SAME request call authority."""
        profile = next(p for p in build_jarvis_live_runtime_model_role_profiles()
                       if p.role_id == "heavy_reasoning_model")
        candidate_ids = tuple(
            ["goal:" + str(g.get("goal_id", "")) for g in candidate.get("goals", ())]
            + ["requirement:" + str(i) for i, _ in enumerate(candidate.get("response_requirements", ()))])
        system_prompt = (
            "Compare the original source independently with the proposed semantic candidate. "
            "Assess ALL requested outcomes, response facets, negations, dependencies and restrictions. "
            "The candidate does not define the expected source semantics. Do not infer completeness "
            "from copied source spans or candidate references. Detect omissions, duplicate facets, "
            "contradictions and unsupported additions. COMPLETE requires all source semantics represented "
            "faithfully exactly once. INCOMPLETE means missing source facets only; describe them in missing. "
            "Contradictions, duplicate semantic obligations and unsupported additions are INVALID. "
            "If not established use UNPROVEN. supported contains only supplied candidate reference IDs "
            "whose semantics are supported by the source. Do not author a replacement candidate, answer, "
            "capability, operation, policy or execution decision. Return the declared verdict JSON."
        )
        # Source is a separate immutable input, not regenerated from candidate.
        result = self._main_model_call(
            system_prompt=system_prompt,
            user_prompt=json.dumps({"source": source_text, "candidate": candidate,
                                    "candidate_references": candidate_ids}, ensure_ascii=False),
            deadline=deadline, schema=SOURCE_CANDIDATE_VERDICT_SCHEMA,
            num_predict=REQUEST_UNDERSTANDING_NUM_PREDICT,
            deadline_error="source_candidate_verification_deadline_exceeded", model_id=profile.model_id,
            keep_alive=0 if profile.load_policy == "load_on_demand" else None,
        )
        verdict = result.get("parsed")
        status = (validate_source_candidate_verdict(verdict, candidate_ids)
                  if result.get("ok") and result.get("final_valid") else "UNPROVEN")
        reason = (verdict.get("reason", "") if isinstance(verdict, dict) else "")
        if status == "UNPROVEN":
            reason = result.get("validation_error") or "semantic_source_coverage_not_proven"
        for attempt in result.get("model_attempts", ()):
            attempt.update(semantic_verdict=status if attempt.get("schema_valid") else "UNPROVEN",
                           semantic_reason=reason if attempt.get("schema_valid") else attempt.get("validation_error"),
                           repair_decision="ELIGIBLE_IF_SHARED_BUDGET" if status == "INCOMPLETE" else "NONE")
        return {"valid": status == "COMPLETE", "status": status, "reason": reason,
                "verdict": verdict, "model_call": result}

    def _single_model_call(
        self, *, system_prompt: str, user_prompt: str, deadline: RequestDeadline,
        schema: dict[str, Any], num_predict: int, deadline_error: str,
        model_id: str = PRIMARY_CONVERSATION_MODEL_ID,
        keep_alive: str | int | None = None,
        num_ctx: int | None = None,
    ) -> dict[str, Any]:
        deadline_remaining = deadline.remaining()
        timeout_truth = build_model_call_timeout_truth(
            model_id,
            deadline_remaining_seconds=deadline_remaining,
        )
        timeout = float(timeout_truth["effective_transport_timeout_seconds"])
        if timeout <= 0 or deadline.cancelled:
            raise TimeoutError(deadline_error)
        requested_num_ctx = int(num_ctx) if num_ctx is not None else context_tokens_for_jarvis_model(model_id)
        payload = {
            "model": model_id, "stream": False, "format": model_visible_structured_schema(schema),
            "think": think_policy_for_model_id(model_id),
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": user_prompt}],
            "options": {"temperature": 0, "num_predict": num_predict, "num_ctx": requested_num_ctx},
            "keep_alive": keep_alive if keep_alive is not None else OLLAMA_LIVE_MODEL_KEEP_ALIVE,
        }
        trace_id, model_ordinal, model_started = trace_model_call_started(
            purpose=deadline_error.removesuffix("_deadline_exceeded"),
            caller=f"{type(self).__name__}._single_model_call",
            model_role=model_role_for_model_id(model_id),
            model_id=model_id, prompt_chars=len(system_prompt) + len(user_prompt),
            num_predict=num_predict, deadline_remaining=deadline_remaining,
        )
        deadline.reserve_understanding_model_attempt()
        started_at, started_clock = transport_clock_snapshot()
        try:
            result = ollama_post_json(OLLAMA_CHAT_URL, payload, timeout_seconds=timeout)
            finished_at, finished_clock = transport_clock_snapshot()
            envelope = ollama_model_call_result(
                result, expected_model_id=model_id,
                requested_num_ctx=requested_num_ctx, transport_attempted=True,
                timeout_truth=timeout_truth, transport_started_at=started_at,
                transport_finished_at=finished_at,
                transport_duration_seconds=finished_clock - started_clock,
            )
            if deadline.cancelled:
                failure = TimeoutError(deadline_error)
                failure.model_call_result = envelope
                raise failure
        except Exception as exc:
            trace_model_call_completed(
                trace_id=trace_id, ordinal=model_ordinal, started=model_started,
                status="FAILED", deadline_remaining=deadline.remaining(),
                error_class=type(exc).__name__,
            )
            raise
        trace_model_call_completed(
            trace_id=trace_id, ordinal=model_ordinal, started=model_started,
            status="COMPLETED" if result.get("ok", True) else "FAILED",
            deadline_remaining=deadline.remaining(),
        )
        return envelope

    def _main_model_call(
        self, *, system_prompt: str, user_prompt: str, deadline: RequestDeadline,
        schema: dict[str, Any], num_predict: int, deadline_error: str,
        model_id: str = PRIMARY_CONVERSATION_MODEL_ID,
        keep_alive: str | int | None = None,
        num_ctx: int | None = None,
    ) -> dict[str, Any]:
        """Structured semantic call with host-side schema validation + ONE bounded retry.

        Invariant: a returned structured success MUST be schema-valid. A model may
        violate a schema; the runtime rejects it after at most one bounded retry, never
        silently normalizing malformed output into valid data. This retry applies only
        to typed semantic inference, never to Final Brain dialogue."""
        attempts = []
        policy = deadline.understanding_attempt_policy
        for index in range(policy.schema_max_attempts):
            if not deadline.understanding_attempt_available():
                if attempts:
                    break
                return {"ok": False, "content": "", "parsed": None, "final_valid": False,
                        "validation_error": "understanding_model_attempt_budget_exhausted",
                        "model_attempts": [], "retry_used": False}
            before = deadline.understanding_model_attempt_count
            try:
                envelope = self._single_model_call(
                    system_prompt=system_prompt, user_prompt=user_prompt, deadline=deadline,
                    schema=schema, num_predict=num_predict, deadline_error=deadline_error,
                    model_id=model_id, keep_alive=keep_alive, num_ctx=num_ctx,
                )
            except Exception as exc:
                if deadline.understanding_model_attempt_count > before:
                    from datetime import datetime, timezone
                    received = getattr(exc, "model_call_result", None)
                    failure = {"attempt_index": index, "request_model_attempt": deadline.understanding_model_attempt_count,
                               "model": model_id, "model_role": model_role_for_model_id(model_id), "timestamp": datetime.now(timezone.utc).isoformat(),
                               "raw_response": received.get("content") if received is not None else None,
                               "response_received": received is not None, "schema_valid": False,
                               "validation_error": type(exc).__name__, "retry_decision": False,
                               "retry_reason": "cancelled_after_response" if received is not None else "transport_exception_no_response",
                               "diagnostic_only": True,
                               "user_memory": False, "training_eligible": False}
                    deadline.understanding_model_attempts.append(failure)
                    trace_stage("UNDERSTANDING_ATTEMPT", "FAILED", model_id=model_id,
                                safe_structure={k: v for k, v in failure.items() if k != "raw_response"})
                raise
            parsed, valid, verr = validate_structured_payload(envelope.get("content"), schema)
            retry = bool(not valid and envelope.get("ok") and index + 1 < policy.schema_max_attempts
                         and deadline.understanding_attempt_available() and not deadline.cancelled)
            reason = ("schema_invalid_bounded_retry" if retry else "schema_valid" if valid else
                      "transport_failed" if not envelope.get("ok") else "attempt_budget_exhausted")
            from datetime import datetime, timezone
            attempt = {"attempt_index": index, "request_model_attempt": deadline.understanding_model_attempt_count,
                       "model": model_id, "model_role": model_role_for_model_id(model_id), "timestamp": datetime.now(timezone.utc).isoformat(),
                       "raw_response": envelope.get("content"), "schema_valid": valid,
                       "validation_error": verr, "retry_decision": retry, "retry_reason": reason,
                       "diagnostic_only": True, "user_memory": False, "training_eligible": False}
            attempts.append(attempt)
            deadline.understanding_model_attempts.append(attempt)
            trace_stage("UNDERSTANDING_ATTEMPT", "COMPLETED" if valid else "FAILED",
                        model_id=model_id, safe_structure={k: v for k, v in attempt.items() if k != "raw_response"})
            envelope.update(parsed=parsed, first_attempt_valid=attempts[0]["schema_valid"],
                            retry_used=len(attempts) > 1, final_valid=valid, validation_error=verr,
                            model_attempts=list(attempts),
                            understanding_model_attempt_count=deadline.understanding_model_attempt_count)
            if not retry:
                return envelope
        return envelope

    def correct_input(self, *, original_text: str, safe_normalized_text: str,
                      input_channel: str, input_quality_metadata: dict[str, Any],
                      deadline: RequestDeadline) -> dict[str, Any]:
        return self._correct_input(
            original_text=original_text, safe_normalized_text=safe_normalized_text,
            input_channel=input_channel, input_quality_metadata=input_quality_metadata,
            deadline=deadline, quality_review=False, prior_correction=None,
        )

    def review_input_correction(
        self, *, original_text: str, safe_normalized_text: str,
        input_channel: str, input_quality_metadata: dict[str, Any],
        prior_correction: dict[str, Any], deadline: RequestDeadline,
        validation_error: str = "",
    ) -> dict[str, Any]:
        """One correction-only quality review through the same helper model and transport."""
        return self._correct_input(
            original_text=original_text, safe_normalized_text=safe_normalized_text,
            input_channel=input_channel, input_quality_metadata=input_quality_metadata,
            deadline=deadline, quality_review=True, prior_correction=prior_correction,
            validation_error=validation_error,
        )

    def _correct_input(
        self, *, original_text: str, safe_normalized_text: str,
        input_channel: str, input_quality_metadata: dict[str, Any],
        deadline: RequestDeadline, quality_review: bool,
        prior_correction: dict[str, Any] | None,
        validation_error: str = "",
    ) -> dict[str, Any]:
        deadline_remaining = deadline.remaining()
        timeout_truth = build_model_call_timeout_truth(
            HELPER_INPUT_CORRECTION_MODEL_ID,
            deadline_remaining_seconds=deadline_remaining,
        )
        timeout = float(timeout_truth["effective_transport_timeout_seconds"])
        if timeout <= 0 or deadline.cancelled:
            raise TimeoutError("helper_input_correction_deadline_exceeded")
        system_prompt = (
            "Repair probable spelling, typing, grammar, transcription or STT corruption and expose ambiguity evidence "
            "only. Preserve the user's meaning, names, technical identifiers, requested effects and negations. "
            "Return corrected_text as the "
            "complete corrected input, not an explanation. Set no_change_needed=true when safe_normalized_text needs no "
            "change, and keep corrected_text equal to safe_normalized_text in that case. If corrected_text differs from "
            "safe_normalized_text, no_change_needed must be false and reason_codes must describe the correction. "
            "preserve_original must be true: "
            "the caller retains original_text outside this output. Do not select capability, operation, provider, model "
            "role, tool, policy, action, risk authorization, or answer. Return exactly the correction JSON schema."
        )
        if quality_review:
            system_prompt += (
                " This is the single correction-quality review. The first complete helper payload either reported no "
                "change although typed channel metadata requested correction, or failed the strict correction truth "
                "contract. Reassess transcription, orthography, grammar, and the supplied validation error. Return one "
                "complete replacement payload whose corrected_text, no_change_needed, and reason_codes agree. Do not "
                "copy contradictory flags from the rejected payload. Compare the replacement corrected_text with "
                "safe_normalized_text: if they differ, no_change_needed MUST be false and reason_codes MUST describe "
                "the actual correction; if they are identical, no_change_needed MUST be true. Never use "
                "no_change_needed as a reason code when corrected_text differs. Do not change meaning merely to force "
                "a correction; no_change_needed may remain true when justified."
            )
        user_prompt = {
            "original_text": original_text, "safe_normalized_text": safe_normalized_text,
            "input_channel": input_channel, "input_quality_metadata": input_quality_metadata,
        }
        if quality_review:
            user_prompt["prior_correction"] = dict(prior_correction or {})
            user_prompt["prior_validation_error"] = str(validation_error)
        payload = {
            "model": HELPER_INPUT_CORRECTION_MODEL_ID, "stream": False,
            "format": HELPER_INPUT_CORRECTION_SCHEMA, "think": OLLAMA_FAST_CHAT_THINK,
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)}],
            "options": {"temperature": 0, "num_predict": 350,
                        "num_ctx": context_tokens_for_jarvis_model(HELPER_INPUT_CORRECTION_MODEL_ID)},
            "keep_alive": OLLAMA_LIVE_MODEL_KEEP_ALIVE,
        }
        started_at, started_clock = transport_clock_snapshot()
        result = ollama_post_json(OLLAMA_CHAT_URL, payload, timeout_seconds=timeout)
        finished_at, finished_clock = transport_clock_snapshot()
        requested_num_ctx = int(payload["options"]["num_ctx"])
        envelope = ollama_model_call_result(
            result, expected_model_id=HELPER_INPUT_CORRECTION_MODEL_ID,
            requested_num_ctx=requested_num_ctx, transport_attempted=True,
            timeout_truth=timeout_truth, transport_started_at=started_at,
            transport_finished_at=finished_at,
            transport_duration_seconds=finished_clock - started_clock,
        )
        if deadline.cancelled:
            failure = TimeoutError("helper_input_correction_deadline_exceeded")
            failure.model_call_result = envelope
            raise failure
        parsed, valid, validation_error = validate_structured_payload(envelope.get("content"), HELPER_INPUT_CORRECTION_SCHEMA)
        envelope.update(parsed=parsed, final_valid=valid, validation_error=validation_error)
        return envelope
