from __future__ import annotations

"""Canonical provider bridge from semantic generation capabilities to local model roles."""

import hashlib
import json
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    context_tokens_for_jarvis_model,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    ExecutionReceipt,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    DAILY_CODER_MODEL_ID,
    PRIMARY_CONVERSATION_MODEL_ID,
    ollama_chat_once,
)


PROVIDER_ID = "existing_ollama_model_roles"
MODEL_ROLE_BINDINGS = {
    "code.proposal.generate": (DAILY_CODER_MODEL_ID, "generate_code_proposal"),
    "content.metadata.generate": (PRIMARY_CONVERSATION_MODEL_ID, "generate_content_metadata"),
    "content.shorts.generate": (PRIMARY_CONVERSATION_MODEL_ID, "generate_short_script"),
    "automation.build": (PRIMARY_CONVERSATION_MODEL_ID, "generate_workflow_spec"),
}


MODEL_ROLE_OPERATION_CONTRACTS = {
    "code.proposal.generate": ({
        "operation_id": "generate_code_proposal",
        "description": (
            "Generate a bounded code analysis or patch proposal from supplied task context. "
            "The semantic capability does not select or name a compute model."
        ),
        "required_parameters": ("task",), "evidence_kinds": ("code_proposal",),
        "effect_type": "OBSERVE", "target_scope": "provided_task_context",
        "semantic_owner_id": "code.proposal.generate", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },{
        "operation_id":"generate_codex_code_proposal",
        "description":"Use installed Codex as an ephemeral, tool-free bounded coding analysis/proposal worker. Read optional project path via the existing project reader; never apply edits.",
        "required_parameters":("task",), "optional_parameters":("path",),
        "parameter_schemas":{"path":{"type":"string","minLength":1,"maxLength":512,
            "description":"Optional existing source FILE path relative to the canonical project root, only when the request supplies that file. A project name is not a file path. Omit this parameter when no source file is specified."}},
        "evidence_kinds":("code_proposal",),"effect_type":"OBSERVE","target_scope":"provided_task_context",
        "semantic_owner_id":"code.proposal.generate","reversibility":"REVERSIBLE",
        "external_side_effect":False,"risk_class":"READ_ONLY",
    }),
    "content.metadata.generate": ({
        "operation_id": "generate_content_metadata",
        "description": (
            "Generate typed title, description and hashtag metadata from supplied source material using an "
            "available local text-compute provider. The semantic capability never names a model implementation."
        ),
        "required_parameters": ("task",), "evidence_kinds": ("content_metadata",),
        "effect_type": "OBSERVE", "target_scope": "provided_content_context",
        "semantic_owner_id": "content.metadata.generate", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "content.shorts.generate": ({
        "operation_id": "generate_short_script",
        "description": "Own a bounded request to create a short test video from supplied source material; prepare its typed script as the first production stage, with no publication or external action.",
        "required_parameters": ("task",), "evidence_kinds": ("content_script",),
        "effect_type": "EXECUTE", "target_scope": "provided_content_context",
        "semantic_owner_id": "content.shorts.generate", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "MUTATION",
    },),
}


class ExistingOllamaModelRoleAdapter:
    """One proposal-only boundary over the canonical Ollama transport."""

    provider_id = PROVIDER_ID

    def generate_bounded_text(self, task: str, *, operation: str = "generate_code_proposal") -> dict[str, Any]:
        """Canonical role-bound completion for bounded external providers."""
        binding = {op: (cap, model) for cap, (model, op) in MODEL_ROLE_BINDINGS.items()}.get(operation)
        if binding is None or not task.strip():
            return {"ok": False, "error": "unsupported_or_empty_role_request"}
        _capability_id, model_id = binding
        options = {"temperature": 0, "num_predict": 120, "num_ctx": context_tokens_for_jarvis_model(model_id)}
        if operation == "generate_workflow_spec":
            options.update({"num_predict": 1400, "num_ctx": 4096})
        return ollama_chat_once(
            task.strip(),
            "Return only the bounded answer requested. Do not claim external actions.",
            model_id=model_id,
            options=options,
        )

    def health(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE",
            "provider_roles": ("CODER", "CHAT"),
            "proposal_only": True,
            "filesystem_mutation_allowed": False,
            "tool_execution_allowed": False,
        }

    def collect_evidence(
        self,
        understanding: RequestUnderstanding,
        plan: ExecutionPlan,
        trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        binding_by_operation = {
            operation_id: (capability_id, model_id)
            for capability_id, (model_id, operation_id) in MODEL_ROLE_BINDINGS.items()
        }
        binding_by_operation['generate_codex_code_proposal']=('code.proposal.generate','codex_cli')
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            binding = binding_by_operation.get(step.operation)
            if binding is None or binding[0] != step.capability_id:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            task = dict(step.parameters).get("task", "").strip()
            if not task:
                errors.append(f"{step.operation}:missing_task")
                continue
            model_id = binding[1]
            metadata_generation = step.operation == "generate_content_metadata"
            script_generation = step.operation == "generate_short_script"
            if step.operation == 'generate_codex_code_proposal':
                from MAKSIMAR_SERVER.AI_ORCHESTRATION.external_agent_provider_adapter import run_bounded_codex_proposal
                result = run_bounded_codex_proposal(task,path=dict(step.parameters).get('path',''),
                    timeout=deadline.remaining() if deadline is not None else 90)
            else:
                result = ollama_chat_once(
                task,
                ((
                    "Return only one compact JSON object with exactly title (string), description (string), and "
                    "hashtags (array of strings). Ground every value in the supplied source material. Do not claim "
                    "publication or any external action. Do not expose private reasoning."
                ) if metadata_generation else ("Return only one compact JSON object with exactly title, hook, body, outro, and duration_seconds. Ground every value in the supplied source material. Do not claim publication or any external action." if script_generation else (
                    "Produce a bounded proposal only. Do not claim that files, tools, tests, commands, "
                    "or external actions were executed. Do not expose private reasoning."
                ))),
                model_id=model_id,
                options={
                    "temperature": 0,
                    "num_predict": 700,
                    "num_ctx": context_tokens_for_jarvis_model(model_id),
                },
                deadline_remaining_seconds=(deadline.remaining() if deadline is not None else None),
            )
            if result.get("ok") is not True:
                errors.append(f"{step.operation}:{result.get('error', 'model_call_failed')}")
                continue
            proposal = str(result.get("content", "")).strip()
            metadata: dict[str, Any] | None = None
            if metadata_generation:
                try:
                    parsed = json.loads(proposal)
                except (TypeError, ValueError):
                    errors.append(f"{step.operation}:invalid_typed_metadata")
                    continue
                if not isinstance(parsed, dict) or set(parsed) != {"title", "description", "hashtags"}:
                    errors.append(f"{step.operation}:invalid_typed_metadata")
                    continue
                if not isinstance(parsed["title"], str) or not isinstance(parsed["description"], str):
                    errors.append(f"{step.operation}:invalid_typed_metadata")
                    continue
                if not isinstance(parsed["hashtags"], list) or not all(isinstance(item, str) for item in parsed["hashtags"]):
                    errors.append(f"{step.operation}:invalid_typed_metadata")
                    continue
                metadata = parsed
            elif script_generation:
                try:
                    parsed = json.loads(proposal)
                except (TypeError, ValueError):
                    errors.append(f"{step.operation}:invalid_typed_script")
                    continue
                required = {"title", "hook", "body", "outro", "duration_seconds"}
                if (not isinstance(parsed, dict) or set(parsed) != required
                        or not all(isinstance(parsed[key], str) for key in required - {"duration_seconds"})
                        or not isinstance(parsed["duration_seconds"], (int, float))
                        or not 1 <= float(parsed["duration_seconds"]) <= 60):
                    errors.append(f"{step.operation}:invalid_typed_script")
                    continue
                metadata = parsed
                # The shorts capability owns the bounded local production slice:
                # script first, then canonical speech synthesis and deterministic
                # composition.  Provider-private asset mechanics stay below this
                # typed operation boundary.
                try:
                    from MAKSIMAR_SERVER.CONTENT_FACTORY.shorts_factory_runtime import (
                        ContentJob, compose_shorts_asset,
                    )
                    job = ContentJob(
                        job_id=f"content_job_{understanding.request_id.replace('-', '_')}",
                        request_id=understanding.request_id,
                        session_id=understanding.request_id,
                        content_goal=task,
                        format="shorts",
                        language="ru",
                        platform_targets=("local_preview",),
                        source_refs=(f"request:{understanding.request_id}",),
                        constraints=("no_publication", "local_assets_only"),
                    )
                    assets = compose_shorts_asset(job, parsed)
                    metadata = {**parsed, "asset_refs": tuple(asset.asset_id for asset in assets),
                                "asset_read_models": tuple(asset.to_read_model() for asset in assets)}
                except Exception as exc:
                    errors.append(f"{step.operation}:composition_failed:{type(exc).__name__}")
                    continue
            observation_payload = {
                "model_id": model_id,
                **({'compute_provider':'codex_cli','provider_readback':result['provider_readback']}
                   if step.operation=='generate_codex_code_proposal' else {}),
                **({"metadata": metadata, "provider_role": "CHAT"} if (metadata_generation or script_generation) else {
                    "proposal": proposal, "proposal_only": True, "provider_role": "CODER",
                }),
                "model_call": {
                    key: result.get(key)
                    for key in (
                        "done", "done_reason", "prompt_eval_count", "eval_count",
                        "load_duration", "prompt_eval_duration", "eval_duration",
                        "total_duration", "requested_num_ctx", "truncation",
                    )
                },
            }
            observation = json.dumps(observation_payload, ensure_ascii=False, sort_keys=True)
            digest = hashlib.sha256(observation.encode("utf-8")).hexdigest()
            items.append(EvidenceItem(
                kind="content_metadata" if metadata_generation else ("content_script" if script_generation else "code_proposal"),
                source=f"{self.provider_id}:{model_id}",
                observation=observation,
                scope="provided_content_context" if (metadata_generation or script_generation) else "provided_task_context",
                confidence=1.0,
                trace_id=trace_id,
                observed_at=utc_observed_at(),
                content_hash=f"sha256:{digest}",
                source_reference=f"codex://bounded/{trace_id}/{step.step_id}" if model_id=='codex_cli' else f"ollama://{model_id}",
                truncated=False,
                omitted_count=0,
                request_id=understanding.request_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}",
                request_id=understanding.request_id,
                trace_id=trace_id,
                step_id=step.step_id,
                capability_id=step.capability_id,
                operation_id=step.operation,
                provider_id=self.provider_id,
                status="COMPLETE",
                result=("available local text-compute provider generated typed content output"
                        if (metadata_generation or script_generation) else "installed proposal-only model role completed generation"),
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        capability_ids = tuple(dict.fromkeys(step.capability_id for step in plan.steps))
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=(capability_ids[0] if capability_ids else "code.proposal.generate"),
            trace_id=trace_id,
            status=status,
            items=tuple(items),
            limitations=(() if status == "COMPLETE" else ("model-role proposal generation incomplete",)),
            receipts=tuple(receipts),
            errors=tuple(errors),
            capability_ids=capability_ids,
        )


__all__ = [
    "ExistingOllamaModelRoleAdapter",
    "MODEL_ROLE_BINDINGS",
    "MODEL_ROLE_OPERATION_CONTRACTS",
    "PROVIDER_ID",
]
