from __future__ import annotations

"""Bounded external-framework providers using the canonical EvidenceBundle port.

Frameworks are provider identities below the semantic capability registry. The
small resolver is host-owned; unsupported/model-backed runtimes fail closed.
"""

import hashlib
import json
import subprocess
from pathlib import Path

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionPlan, ExecutionReceipt,
    RequestDeadline, RequestUnderstanding, utc_observed_at,
)

PROVIDER_ID = "external_langgraph_provider"
RUNTIME_PYTHON = Path(__file__).resolve().parents[2] / "EXTERNAL_BACKENDS/agent_tooling/venv/bin/python"
PROVIDER_CLASSIFICATIONS = {
    "external_adapter:langgraph": "AVAILABLE_PROVIDER",
    "external_adapter:smolagents": "AVAILABLE_PROVIDER",
    "external_adapter:autogen_agentchat": "PRECONDITION_REQUIRED",
    "external_adapter:autogen_ext": "PRECONDITION_REQUIRED",
    "external_adapter:openai_agents_sdk": "PRECONDITION_REQUIRED",
    "external_adapter:mcp_python_sdk": "AVAILABLE_PROVIDER",
}


def run_bounded_codex_proposal(task: str, *, path: str = '', timeout: float = 90) -> dict[str, object]:
    """Codex is a tool-free, ephemeral compute worker below the existing coding owner."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import PROJECT_ROOT, read_file_snippet
    candidates = tuple(Path('/mnt/c/Users/Александр/AppData/Local/OpenAI/Codex/bin').glob('*/codex.exe'))
    if not candidates:
        return {'ok':False,'error':'codex_executable_unavailable'}
    executable = max(candidates,key=lambda p:p.stat().st_mtime)
    source = None
    source_hash = ''
    if path:
        snippet = read_file_snippet(path)
        if snippet.get('allowed') is not True:
            return {'ok':False,'error':'codex_source_path_denied'}
        source = (PROJECT_ROOT/path).resolve()
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        task += '\nCanonical read-only source evidence:\n' + json.dumps(snippet,ensure_ascii=False)
    args = [str(executable),'exec','--ignore-user-config','--ephemeral','--sandbox','read-only',
            '--json','--skip-git-repo-check','--disable','shell_tool','--disable','shell_snapshot',
            '--disable','hooks','--disable','plugins','--disable','tool_suggest',
            '-c','web_search="disabled"','-']
    try:
        completed = subprocess.run(args,input='Bounded proposal-only worker. Use only supplied context. '
            'No tools, no writes, no execution, no private reasoning. Return a concise analysis/proposal.\n'+task,
            capture_output=True,text=True,timeout=max(0.1,min(90,timeout)),check=False)
        events = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    except (OSError,subprocess.SubprocessError,ValueError) as exc:
        return {'ok':False,'error':'codex_transport_'+type(exc).__name__}
    messages=[]; completed_turn=False; usage={}
    for event in events:
        if event.get('type')=='item.completed':
            item=event.get('item') or {}
            if item.get('type') not in ('agent_message','reasoning'):
                return {'ok':False,'error':'codex_unexpected_tool_activity'}
            if item.get('type')=='agent_message': messages.append(str(item.get('text','')))
        if event.get('type')=='turn.completed': completed_turn=True; usage=event.get('usage') or {}
    content='\n'.join(messages).strip()
    try:
        unchanged = source is None or hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
    except OSError:
        unchanged = False
    if completed.returncode or not completed_turn or not content or len(content)>6000 or not unchanged:
        return {'ok':False,'error':'codex_incomplete_or_source_changed'}
    return {'ok':True,'content':content,'done':True,'done_reason':'stop',
            'compute_provider':'codex_cli','provider_readback':{'executable':str(executable),
            'returncode':completed.returncode,'turn_completed':completed_turn,'usage':usage,
            'tools_enabled':False,'source_path':path,'source_sha256':source_hash,
            'source_unchanged':unchanged,'stdout_sha256':hashlib.sha256(completed.stdout.encode()).hexdigest(),
            'ephemeral':True,'sandbox':'read-only'}}


class ExistingExternalAgentProviderAdapter:
    provider_id = PROVIDER_ID

    def health(self) -> dict[str, object]:
        return {"provider_id": self.provider_id, "status": "AVAILABLE", "runtime_python": str(RUNTIME_PYTHON)}

    def collect_evidence(
        self, understanding: RequestUnderstanding, plan: ExecutionPlan,
        trace_id: str, deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                continue
            if step.operation not in {"run_local_graph", "run_local_smolagent", "run_local_mcp"}:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            if step.operation == "run_local_mcp":
                server_path = Path(__file__).resolve().parents[2] / "RUNTIME/agent_tooling/mcp_local_add_server.py"
                script = ("import asyncio\nfrom mcp import ClientSession\nfrom mcp.client.stdio import stdio_client, StdioServerParameters\n"
                          "async def main():\n"
                          f" p=StdioServerParameters(command={str(RUNTIME_PYTHON)!r}, args={[str(server_path)]!r})\n"
                          " async with stdio_client(p) as (r,w):\n  async with ClientSession(r,w) as c:\n"
                          "   await c.initialize(); x=await c.call_tool('add',{'a':40,'b':2}); print(x.content[0].text)\n"
                          "asyncio.run(main())\n")
            elif step.operation == "run_local_smolagent":
                script = (
                    "import hashlib, json\n"
                    "from smolagents import CodeAgent, Model, ChatMessage\n"
                    "from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import ExistingOllamaModelRoleAdapter\n"
                    "response_meta={}\n"
                    "class CanonicalRoleModel(Model):\n"
                    " def generate(self,messages,**kwargs):\n"
                    "  response=ExistingOllamaModelRoleAdapter().generate_bounded_text('Return only Python code in a fenced block that prints integer 42. No prose.')\n"
                    "  text=str(response.get('content','')).strip() if isinstance(response,dict) else ''\n"
                    "  if response.get('ok') is not True or not text: raise RuntimeError('canonical_model_response_missing')\n"
                    "  response_meta.update({'sha256':hashlib.sha256(text.encode()).hexdigest(),'chars':len(text),'model_role':response.get('model_role','')})\n"
                    "  return ChatMessage(role='assistant', content=text)\n"
                    "result=CodeAgent(tools=[], model=CanonicalRoleModel(), max_steps=1).run('Compute a bounded deterministic result.')\n"
                    "print('SMOLAGENTS_PROOF='+json.dumps({'agent_result':str(result),'model_response':response_meta},sort_keys=True))\n"
                )
            else:
                script = (
                    "from typing import TypedDict\n"
                    "from langgraph.graph import StateGraph, START, END\n"
                    "class S(TypedDict): value: int\n"
                    "def add(state): return {'value': state['value'] + 2}\n"
                    "g=StateGraph(S); g.add_node('add', add); g.add_edge(START, 'add'); g.add_edge('add', END)\n"
                    "print(g.compile().invoke({'value': 40})['value'])\n"
                )
            try:
                child_env = dict(__import__('os').environ)
                child_env['PYTHONPATH'] = str(Path(__file__).resolve().parents[2])
                component_timeout = 45.0
                if step.operation == "run_local_smolagent":
                    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import MODEL_TIMEOUT_POLICY
                    component_timeout = MODEL_TIMEOUT_POLICY["daily_coder_model"]["total_request_timeout_seconds"]
                effective_timeout = deadline.remaining(component_timeout) if deadline is not None else component_timeout
                if effective_timeout <= 0:
                    errors.append(f"{step.operation}:total_deadline")
                    continue
                completed = subprocess.run(
                    [str(RUNTIME_PYTHON), "-c", script], check=False,
                    capture_output=True, text=True, timeout=effective_timeout, env=child_env,
                )
                if completed.returncode != 0:
                    raise RuntimeError(completed.stderr.strip() or f"returncode:{completed.returncode}")
                if step.operation == "run_local_mcp":
                    result = {"value": int(completed.stdout.strip()), "transport": "stdio"}
                elif step.operation == "run_local_smolagent":
                    markers = [line for line in completed.stdout.splitlines()
                               if line.startswith("SMOLAGENTS_PROOF=")]
                    if len(markers) != 1:
                        raise RuntimeError("smolagents_bounded_proof_missing_or_ambiguous")
                    proof_text = markers[0].split("=", 1)[1]
                    result = json.loads(proof_text)
                    # The current child produces exactly this structured proof.
                    # Reject duplicate JSON keys rather than silently taking the last value.
                    pending = [json.loads(proof_text, object_pairs_hook=tuple)]
                    while pending:
                        value = pending.pop()
                        if isinstance(value, tuple):
                            keys = [key for key, _ in value]
                            if len(keys) != len(set(keys)):
                                raise RuntimeError("smolagents_bounded_proof_duplicate_key")
                            pending.extend(item for _, item in value)
                        elif isinstance(value, list):
                            pending.extend(value)
                    if (not isinstance(result, dict)
                            or set(result) != {"agent_result", "model_response"}
                            or result.get("agent_result") != "42"):
                        raise RuntimeError("smolagents_bounded_result_invalid")
                    proof = result["model_response"]
                    if not isinstance(proof, dict) or set(proof) != {"sha256", "chars", "model_role"}:
                        raise RuntimeError("smolagents_model_proof_invalid")
                    digest, chars, role = proof["sha256"], proof["chars"], proof["model_role"]
                    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import MODEL_ROLE_BINDINGS
                    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import model_role_for_model_id
                    expected_model = {operation: model for model, operation in MODEL_ROLE_BINDINGS.values()}[
                        "generate_code_proposal"
                    ]
                    expected_role = model_role_for_model_id(expected_model)
                    if (not isinstance(digest, str) or len(digest) != 64
                            or any(char not in "0123456789abcdefABCDEF" for char in digest)
                            or not isinstance(chars, int) or isinstance(chars, bool) or chars <= 0
                            or not isinstance(role, str) or expected_role == "unknown" or role != expected_role):
                        raise RuntimeError("smolagents_model_proof_invalid")
                    # Structure is verified, not independent attestation of model execution.
                    if deadline is not None:
                        deadline.check()
                else:
                    result = {"value": int(completed.stdout.strip())}
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{step.operation}:{type(exc).__name__}:{exc}")
                continue
            observation = json.dumps(result, sort_keys=True)
            digest = hashlib.sha256(observation.encode()).hexdigest()
            items.append(EvidenceItem(
                kind="external_provider_result", source=f"{self.provider_id}:{step.operation.removeprefix('run_local_')}",
                observation=observation, scope="local_external_agent_runtime", confidence=1.0,
                trace_id=trace_id, observed_at=utc_observed_at(), content_hash=f"sha256:{digest}",
                source_reference=str(RUNTIME_PYTHON), request_id=understanding.request_id,
                step_id=step.step_id, capability_id=step.capability_id,
                operation_id=step.operation, provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                operation_id=step.operation, provider_id=self.provider_id, status="COMPLETE",
                result=f"deterministic {step.operation.removeprefix('run_local_')} invocation completed in isolated provider runtime",
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        capability_ids = tuple(dict.fromkeys(step.capability_id for step in plan.steps))
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=capability_ids[0], trace_id=trace_id, status=status,
            items=tuple(items), limitations=(() if status == "COMPLETE" else ("external provider execution incomplete",)),
            receipts=tuple(receipts), errors=tuple(errors), capability_ids=capability_ids,
        )


def resolve_external_provider(provider_identity: str) -> ExistingExternalAgentProviderAdapter:
    """Resolve only an explicitly registered provider identity.

    This is deliberately not semantic routing: callers must already have a
    HOST-authorized provider identity. Unknown or gated providers fail closed.
    """
    if provider_identity not in {"external_adapter:langgraph", "external_adapter:smolagents", "external_adapter:mcp_python_sdk"}:
        raise ValueError(
            f"provider_not_runtime_executable:{provider_identity}:"
            f"{PROVIDER_CLASSIFICATIONS.get(provider_identity, 'UNAVAILABLE')}"
        )
    adapter = ExistingExternalAgentProviderAdapter()
    adapter.provider_id = {
        "external_adapter:langgraph": "external_langgraph_provider",
        "external_adapter:smolagents": "external_smolagents_provider",
        "external_adapter:mcp_python_sdk": "external_mcp_provider",
    }[provider_identity]
    return adapter


__all__ = ["ExistingExternalAgentProviderAdapter", "PROVIDER_ID", "PROVIDER_CLASSIFICATIONS", "resolve_external_provider"]
