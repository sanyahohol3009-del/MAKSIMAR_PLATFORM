"""Canonical n8n workflow-automation provider adapter (REUSE existing adapter pattern).

n8n is a provider/organ BELOW semantic understanding. This adapter exposes the
canonical automation operations (create / inspect / execute workflow) and talks to
the real local n8n runtime (HTTP public API + CLI execution). Node/operation truth
comes from the version-pinned LOCAL catalog (n8n_local_catalog.py), never internet.
"""
from __future__ import annotations

import hashlib
from dataclasses import replace
import json
import os
import re
import signal
import sqlite3
import time
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionPlan,
    ExecutionReceipt,
    PermissionDecision,
    RequestDeadline,
    RequestUnderstanding,
    utc_observed_at,
)
from tools.jarvis_live_runtime.jarvis_skill_visibility import (
    load_automation_n8n_private_skill_context,
    select_skills_for_tools,
)

PROVIDER_ID = "existing_n8n_workflow_automation"

N8N_BASE_URL = "http://127.0.0.1:5678"
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_N8N_ROOT = _PROJECT_ROOT / "EXTERNAL_BACKENDS/vendor_quarantine/n8n-2.42.6-candidate"
_N8N_CLI = _N8N_ROOT / "node_modules/n8n/bin/n8n"
_CANONICAL_RUNTIME_ROOT = Path("/home/aleksandr/MAKSIMAR_RUNTIME/n8n/canonical")
_CANONICAL_DATA_ROOT = _CANONICAL_RUNTIME_ROOT / ".n8n"
_API_KEY_PATH = _CANONICAL_DATA_ROOT / "jarvis_api_key"
_NODE24 = Path.home() / ".nvm/versions/node/v24.19.0/bin/node"
_RUNNER_TOKEN_PATH = _PROJECT_ROOT / "RUNTIME/n8n/config/task-runner-auth-token"


def _canonical_user_folder() -> Path:
    """Return the explicit, stable owner of the canonical n8n data.

    Migration-stage directories are preserved as rollback evidence, but are
    deliberately never discovered or selected by production code.
    """
    return _CANONICAL_RUNTIME_ROOT


def _docker_deployment() -> dict[str, Any] | None:
    path = _PROJECT_ROOT / "RUNTIME/n8n/canonical-deployment.json"
    if not path.is_file():
        return None
    value = json.loads(path.read_text())
    if value.get("canonical_data_root") != str(_CANONICAL_DATA_ROOT) or not \
            str(value.get("image", "")).startswith("sha256:"):
        raise ValueError("n8n_docker_deployment_owner_mismatch")
    return value


def _canonical_container(*, cli: bool = False) -> dict[str, Any] | None:
    deployment = _docker_deployment()
    if deployment is None:
        return None
    name = deployment["container"] + ("-cli" if cli else "")
    probe = subprocess.run(["docker", "container", "inspect", name],
                           capture_output=True, text=True, timeout=10, check=False)
    if probe.returncode:
        if "No such" in probe.stderr:
            return None
        raise ValueError("n8n_docker_ownership_unavailable")
    value = json.loads(probe.stdout)[0]
    mounts = value.get("Mounts", ())
    owned = any(m.get("Source") == str(_CANONICAL_DATA_ROOT) and
                m.get("Destination") == "/home/node/.n8n" for m in mounts)
    labels = value.get("Config", {}).get("Labels") or {}
    if not owned or value.get("Image") != deployment["image"] or \
            labels.get("maksimar.canonical-owner") != "existing_n8n_workflow_automation":
        raise ValueError("n8n_container_is_not_canonical_owner")
    return {"name": name, "running": value["State"]["Running"]}


def _api_key() -> str:
    if _API_KEY_PATH.exists():
        return _API_KEY_PATH.read_text(encoding="utf-8").strip()
    return os.environ.get("N8N_API_KEY", "")


N8N_CAPABILITY_OPERATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "workflow_automation:n8n": (
        {
            "operation_id": "build_workflow",
            "description": "Design a bounded declarative local automation from the user's goal, validate it, and create a draft workflow.",
            "required_parameters": ("task",), "evidence_kinds": ("n8n_workflow", "automation_spec"),
            "effect_type": "MUTATE", "target_scope": "local_workflow_automation",
            "semantic_owner_id": "automation.build", "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "MUTATION",
        },
        {
            "operation_id": "create_workflow",
            "description": "Create a real local n8n workflow from validated installed node contracts.",
            "required_parameters": ("logical_spec",),
            "evidence_kinds": ("n8n_workflow",),
            "effect_type": "MUTATE", "target_scope": "local_workflow_automation",
            "semantic_owner_id": "automation.create",
            "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "MUTATION",
        },
        {
            "operation_id": "inspect_workflow",
            "description": "Read back a real local n8n workflow graph and its installed nodes.",
            "required_parameters": (),
            "optional_parameters": ("workflow_id",),
            "parameter_schemas": {"workflow_id": {"type": "string", "description": "Exact existing workflow ID from the request or prior authoritative result; omit when created in this same plan."}},
            "evidence_kinds": ("n8n_workflow",),
            "effect_type": "OBSERVE", "target_scope": "local_workflow_automation",
            "semantic_owner_id": "automation.inspect",
            "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
        },
        {
            "operation_id": "execute_workflow",
            "description": "Execute a real local n8n workflow and capture the authoritative execution result.",
            "required_parameters": (),
            "optional_parameters": ("workflow_id",),
            "parameter_schemas": {"workflow_id": {"type": "string", "description": "Exact existing workflow ID from the request or prior authoritative result; omit when created in this same plan."}},
            "evidence_kinds": ("n8n_execution",),
            "effect_type": "EXECUTE", "target_scope": "local_workflow_automation",
            "semantic_owner_id": "automation.run",
            # Stored graph effects are provider-observed before canonical policy.
            "reversibility": "UNKNOWN", "external_side_effect": True, "risk_class": "UNKNOWN",
        },
        {
            "operation_id": "modify_workflow",
            "description": "Modify a real local n8n workflow graph and read back the stored change.",
            "required_parameters": ("value",),
            "optional_parameters": ("workflow_id",),
            "parameter_schemas": {"workflow_id": {"type": "string", "description": "Exact existing workflow ID; omit when created in this same plan."}},
            "evidence_kinds": ("n8n_workflow",),
            "effect_type": "MUTATE", "target_scope": "local_workflow_automation",
            "semantic_owner_id": "automation.modify",
            "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "MUTATION",
        },
    ),
}


def _n8n_request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = N8N_BASE_URL + path
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("X-N8N-API-KEY", _api_key())
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"error": f"http_{exc.code}", "detail": exc.read().decode("utf-8", "replace")[:300]}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"error": type(exc).__name__}


_LOGICAL_ACTIONS = {"set_field", "transform", "condition", "route", "parallel", "merge", "subworkflow"}


def _validate_logical_spec(spec: dict[str, Any]) -> None:
    """Strict HOST validation for the provider-neutral workflow language."""
    if not isinstance(spec.get("name", "workflow"), str) or not 1 <= len(str(spec.get("name", "workflow"))) <= 96:
        raise ValueError("logical_spec_invalid_name")
    steps = spec.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 24:
        raise ValueError("logical_spec_invalid_step_count")
    if any(isinstance(step, dict) and "next_step_ids" in step for step in steps):
        # Admit the existing canonical flat DAG contract rather than translating
        # it into the old nested mini-language. Compilation still owns installed
        # provider binding, topology, credentials and source-grounding checks.
        from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import _LOGICAL_SPEC_PARAMETER_SCHEMA
        from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import validate_structured_payload
        schema = _LOGICAL_SPEC_PARAMETER_SCHEMA["properties"]
        for value, contract in ((spec.get("trigger", "manual"), schema["trigger"]),
                                (spec.get("constraints", []), schema["constraints"]),
                                *((step, schema["steps"]["items"]) for step in steps)):
            _, valid, error = validate_structured_payload(json.dumps(value), contract)
            if not valid:
                raise ValueError("logical_spec_canonical_dag_invalid:" + error)
        # Schema admission does not expand the existing declarative code policy.
        if any(step["action"] == "transform" and "code" in step for step in steps):
            raise ValueError("logical_spec_transform_must_be_declarative")
        return
    if spec.get("trigger", "manual") not in {"manual", "schedule", "webhook"}:
        raise ValueError("logical_spec_invalid_trigger")
    def visit(seq: Any, depth: int = 0) -> None:
        if not isinstance(seq, list) or depth > 4 or len(seq) > 12:
            raise ValueError("logical_spec_bounds_exceeded")
        for step in seq:
            if not isinstance(step, dict) or set(step) - {"step_id", "action", "field", "value", "code", "kind", "key", "branches", "true_steps", "false_steps", "default_steps", "steps", "value", "operation", "workflow_id"}:
                raise ValueError("logical_spec_unknown_field")
            action = step.get("action")
            if action not in _LOGICAL_ACTIONS:
                raise ValueError("logical_spec_unknown_action")
            if action == "transform" and ("code" in step or step.get("kind") not in {"aggregate", "deduplicate", "normalize"}):
                raise ValueError("logical_spec_transform_must_be_declarative")
            if action in {"parallel", "route"}:
                branches = step.get("branches")
                if not isinstance(branches, list) or not 1 <= len(branches) <= 4:
                    raise ValueError("logical_spec_invalid_branch_count")
                for branch in branches:
                    if not isinstance(branch, dict) or set(branch) - {"label", "value", "steps"}:
                        raise ValueError("logical_spec_unknown_branch_field")
                    visit(branch.get("steps"), depth + 1)
            visit(step.get("true_steps"), depth + 1) if "true_steps" in step else None
            visit(step.get("false_steps"), depth + 1) if "false_steps" in step else None
            visit(step.get("default_steps"), depth + 1) if "default_steps" in step else None
    visit(steps)


def _validate_compiled_workflow(workflow: dict[str, Any]) -> None:
    """Final HOST-side check that compiler output stays within the local contract."""
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler as compiler
    nodes = workflow.get("nodes")
    if not isinstance(nodes, list) or not nodes or len(nodes) > 48:
        raise ValueError("compiled_workflow_bounds_exceeded")
    for node in nodes:
        if not isinstance(node, dict) or compiler._installed(node.get("type")) is None:
            raise ValueError("compiled_workflow_unknown_node")
        # This caller compiles an already-validated declarative spec. Its typed
        # action/free-code contract was checked before compilation; literal
        # assignment values do not become a second authorization policy.


def _compiled_workflow_spec(
    params: dict[str, Any], *, source_text: str | None = None,
    allowed_jarvis_capability_ids: frozenset[str] = frozenset(),
) -> tuple[dict[str, Any] | None, str | None]:
    """Compile a logical automation spec (or validate a raw graph) to a provider graph.

    The model supplies a provider-neutral LOGICAL spec (trigger + steps + constraints);
    the HOST compiles it to exact installed n8n contracts via the local catalog.
    A raw graph is also accepted but every node type is validated against the catalog.
    Returns (graph, error). Fails closed on any gap.
    """
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_logical_compiler as compiler

    raw = params.get("logical_spec")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (ValueError, TypeError):
            raw = None
    if isinstance(raw, dict) and raw.get("steps"):
        try:
            _validate_logical_spec(raw)
            compiled = compiler.compile_logical_automation_spec(
                raw, source_text=source_text,
                allowed_jarvis_capability_ids=allowed_jarvis_capability_ids,
            )
            _validate_compiled_workflow(compiled)
            return compiled, None
        except compiler.LogicalSpecCompileError as exc:
            return None, str(exc)

    workflow = params.get("workflow")
    if isinstance(workflow, str):
        try:
            workflow = json.loads(workflow)
        except (ValueError, TypeError):
            workflow = None
    if not isinstance(workflow, dict):
        return None, "missing_workflow_spec"
    if not workflow.get("nodes") or not workflow.get("connections"):
        return None, "missing_nodes_or_connections"
    if (not isinstance(workflow["nodes"], list) or len(workflow["nodes"]) > 48
            or not isinstance(workflow["connections"], dict)):
        return None, "workflow_graph_shape_invalid"
    for node in workflow["nodes"]:
        if not isinstance(node, dict):
            return None, "workflow_node_shape_invalid"
        ntype = node.get("type")
        if not ntype or compiler._installed(ntype) is None:
            return None, f"node_not_installed:{ntype}"
    return workflow, None


def _architect_logical_spec(task: str) -> dict[str, Any]:
    """Generate declarative workflow intent with the existing local model only."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_role_adapter import ExistingOllamaModelRoleAdapter
    prompt = ("Return JSON only for a bounded local automation. Use manual trigger and only actions "
              "set_field, transform, condition, route, parallel, merge. Maximum 24 steps. No credentials, "
              "shell, Docker, network, publication, provider names, or code. Include name, trigger, steps, "
              "constraints. Goal: " + task)
    result = ExistingOllamaModelRoleAdapter().generate_bounded_text(prompt, operation="generate_workflow_spec")
    if result.get("ok") is not True:
        raise ValueError("automation_architect_unavailable")
    spec = json.loads(str(result.get("content", "")))
    if not isinstance(spec, dict) or not isinstance(spec.get("steps"), list) or not spec["steps"] or len(spec["steps"]) > 24:
        raise ValueError("invalid_logical_automation_spec")
    # The existing declarative contract owns structural admissibility. Literal
    # data values never grant or deny an action; unknown actions/free code fail
    # that same validator before compilation.
    _validate_logical_spec(spec)
    return spec


def _read_execution_result(execution_id: str) -> dict[str, Any]:
    """Read bounded actual last-node output; never expose the resume token/graph."""
    try:
        with sqlite3.connect(f"file:{_CANONICAL_DATA_ROOT / 'database.sqlite'}?mode=ro", uri=True) as db:
            row = db.execute("SELECT data FROM execution_data WHERE executionId=?", (execution_id,)).fetchone()
        if not row:
            return {"readback_status": "UNAVAILABLE"}
        source = """const fs=require('fs'),f=require('/usr/local/lib/node_modules/n8n/node_modules/flatted');
const r=f.parse(fs.readFileSync(0,'utf8')),n=r.resultData.lastNodeExecuted;
const runs=r.resultData.runData[n]||[],items=runs.at(-1)?.data?.main?.[0]||[];let omitted=0;
function bound(v,d=0){if(d>2){omitted++;return null;}
if(typeof v==='string'){if(v.length>160)omitted++;return v.slice(0,160);}
if(Array.isArray(v)){omitted+=Math.max(0,v.length-3);return v.slice(0,3).map(x=>bound(x,d+1));}
if(v&&typeof v==='object'){let es=Object.entries(v);omitted+=Math.max(0,es.length-8);return Object.fromEntries(es.slice(0,8).map(([k,x])=>[k,bound(x,d+1)]));}return v;}
let out={readback_status:'COMPLETE',last_node:n,item_count:items.length,items:items.slice(0,3).map(x=>bound(x.json)),omitted_count:Math.max(0,items.length-3)+omitted};
while(JSON.stringify(out).length>3500&&out.items.length){out.items.pop();out.omitted_count++;}
console.log(JSON.stringify(out));"""
        deployment = _docker_deployment()
        command = ["docker", "run", "--rm", "--read-only", "--network", "none", "-i",
                   "--entrypoint", "node", deployment["image"], "-e", source] if deployment else \
                  [str(_NODE24), "-e", source.replace("/usr/local/lib/node_modules/n8n/node_modules/flatted", "flatted")]
        completed = subprocess.run(command, input=row[0], text=True,
                                   capture_output=True, cwd=_N8N_ROOT, timeout=10, check=False)
        if completed.returncode:
            return {"readback_status": "UNAVAILABLE"}
        return json.loads(completed.stdout)
    except (OSError, sqlite3.Error, subprocess.SubprocessError, json.JSONDecodeError):
        return {"readback_status": "UNAVAILABLE"}


def _read_stored_workflow(workflow_id: str) -> dict[str, Any]:
    """Read the same canonical database used by CLI execution; never a draft."""
    with sqlite3.connect(f"file:{_CANONICAL_DATA_ROOT / 'database.sqlite'}?mode=ro", uri=True) as db:
        row = db.execute("SELECT id,nodes,connections,settings FROM workflow_entity WHERE id=?",
                         (workflow_id,)).fetchone()
    if row is None:
        raise ValueError("stored_workflow_missing")
    graph = {"id": str(row[0]), "nodes": json.loads(row[1]),
             "connections": json.loads(row[2]), "settings": json.loads(row[3] or "{}")}
    if not isinstance(graph["nodes"], list) or not graph["nodes"] or not isinstance(graph["connections"], dict):
        raise ValueError("stored_workflow_graph_invalid")
    return graph


def _stored_workflow_hash(graph: dict[str, Any]) -> str:
    # Names/layout are included in nodes too: approval never follows a changed graph.
    material = {key: graph.get(key) for key in ("id", "nodes", "connections", "settings")}
    return hashlib.sha256(json.dumps(material, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest()


def _stored_workflow_has_literal_intrinsic_effects(graph: dict[str, Any]) -> bool:
    """Prove the small existing manual/literal-assignment primitive contract.

    This reports effects, not permission. All other nodes/expressions/settings
    remain UNKNOWN for the existing canonical policy evaluator to decide.
    """
    settings = graph.get("settings")
    if not isinstance(settings, dict) or set(settings) - {"executionOrder"}:
        return False
    nodes = graph.get("nodes")
    if not isinstance(nodes, list) or not nodes or len(nodes) > 48:
        return False
    names = []
    for node in nodes:
        if not isinstance(node, dict) or node.get("credentials"):
            return False
        names.append(node.get("name"))
        params = node.get("parameters")
        if node.get("type") == "n8n-nodes-base.manualTrigger" and node.get("typeVersion") == 1:
            if params != {}:
                return False
        elif node.get("type") == "n8n-nodes-base.set" and node.get("typeVersion") == 3.4:
            if not isinstance(params, dict) or set(params) != {"assignments"}:
                return False
            assignments = params["assignments"]
            if not isinstance(assignments, dict) or set(assignments) != {"assignments"}:
                return False
            entries = assignments["assignments"]
            if not isinstance(entries, list) or not entries:
                return False
            for item in entries:
                if not isinstance(item, dict) or set(item) != {"id", "name", "value", "type"} or item["type"] != "string":
                    return False
                if any(not isinstance(item[key], str) or item[key].startswith("=") for key in ("id", "name", "value")):
                    return False
        else:
            return False
    if any(not isinstance(name, str) or not name for name in names) or len(set(names)) != len(names):
        return False
    connections = graph.get("connections")
    if not isinstance(connections, dict):
        return False
    for source, outputs in connections.items():
        if source not in names or not isinstance(outputs, dict) or set(outputs) != {"main"}:
            return False
        if not isinstance(outputs["main"], list):
            return False
        for output in outputs["main"]:
            if not isinstance(output, list):
                return False
            for edge in output:
                if not isinstance(edge, dict) or edge.get("node") not in names or edge.get("type") != "main" or edge.get("index") != 0:
                    return False
    return True


def _execute_cli_in_canonical_data_root(workflow_id: str) -> dict[str, Any]:
    with sqlite3.connect(f"file:{_CANONICAL_DATA_ROOT / 'database.sqlite'}?mode=ro", uri=True) as db:
        watermark = db.execute("SELECT COALESCE(MAX(id),0) FROM execution_entity").fetchone()[0]
    env = dict(os.environ)
    env["N8N_RUNNERS_BROKER_PORT"] = "5689"
    env["N8N_RUNNERS_BROKER_LISTEN_ADDRESS"] = "0.0.0.0"
    env["N8N_RUNNERS_MODE"] = "external"
    env["N8N_USER_FOLDER"] = str(_canonical_user_folder())
    env["EXECUTIONS_DATA_PRUNE"] = "false"
    if _RUNNER_TOKEN_PATH.is_file():
        env["N8N_RUNNERS_AUTH_TOKEN"] = _RUNNER_TOKEN_PATH.read_text(encoding="utf-8").strip()
    try:
        command = [str(_N8N_CLI), "execute", "--id", workflow_id]
        if _NODE24.is_file():
            command = [str(_NODE24), str(_N8N_CLI), "execute", "--id", workflow_id]
        deployment = _docker_deployment()
        if deployment:
            command = ["docker", "run", "--rm", "--name", deployment["container"] + "-cli",
                       "--label", "maksimar.canonical-owner=existing_n8n_workflow_automation",
                       "--network", deployment["network"], "--publish", "5689:5689",
                       "--mount", f"type=bind,src={_CANONICAL_DATA_ROOT},dst=/home/node/.n8n",
                       "--env", "N8N_USER_FOLDER=/home/node", "--env", "N8N_RUNNERS_MODE=external",
                       "--env", "N8N_RUNNERS_BROKER_LISTEN_ADDRESS=0.0.0.0",
                       "--env", "N8N_RUNNERS_BROKER_PORT=5689", "--env", "N8N_RUNNERS_AUTH_TOKEN",
                       "--env", "EXECUTIONS_DATA_PRUNE=false",
                       "--env", "N8N_DISABLED_MODULES=instance-ai", "--entrypoint", "n8n",
                       deployment["image"], "execute", "--id", workflow_id]
        completed = subprocess.run(
            command,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=90.0, env=env, check=False,
            cwd=str(_N8N_ROOT),
        )
    except (subprocess.SubprocessError, TimeoutError, OSError) as exc:
        if _docker_deployment():
            cli = _canonical_container(cli=True)
            if cli and cli["running"]:
                subprocess.run(["docker", "stop", "--time", "10", cli["name"]],
                               capture_output=True, timeout=20, check=False)
        return {"error": type(exc).__name__}
    text = (completed.stdout or "") + "\n" + (completed.stderr or "")
    text = re.sub(r'("resumeToken"\s*:\s*")[^"]+(\")', r'\1[REDACTED]\2', text)
    # Graph node IDs are not execution IDs. Read the newly created execution
    # from the same canonical database under the exclusive CLI handoff lock.
    with sqlite3.connect(f"file:{_CANONICAL_DATA_ROOT / 'database.sqlite'}?mode=ro", uri=True) as db:
        row = db.execute("SELECT id,status FROM execution_entity WHERE workflowId=? AND id>? ORDER BY id DESC LIMIT 1",
                         (workflow_id, watermark)).fetchone()
    return {
        "returncode": completed.returncode,
        "output": text[-4000:],
        "execution_id": str(row[0]) if row else "",
        "execution_status": row[1] if row else "UNKNOWN",
        "execution_result": _read_execution_result(str(row[0])) if row else {"readback_status": "UNAVAILABLE"},
    }


def _canonical_server_pid() -> int | None:
    """Resolve only our exact installed CLI/data owner, never an arbitrary listener."""
    probe = subprocess.run(["ss", "-H", "-ltnp", "sport = :5678"], capture_output=True,
                           text=True, timeout=5, check=False)
    matches = re.findall(r"pid=(\d+)", probe.stdout)
    if not matches:
        return None
    pids = set(map(int, matches))
    if len(pids) != 1:
        raise ValueError("n8n_listener_ownership_ambiguous")
    pid = pids.pop()
    args = (Path("/proc") / str(pid) / "cmdline").read_bytes().decode().split("\0")
    env = (Path("/proc") / str(pid) / "environ").read_bytes().decode().split("\0")
    cwd = (Path("/proc") / str(pid) / "cwd").resolve()
    script_matches = len(args) > 1 and (cwd / args[1]).resolve() == _N8N_CLI.resolve()
    # n8n sets process.title, replacing Linux argv with 'n8n start'. Validate
    # the executable, cwd, UID and explicit data root as well as that title.
    titled_owner = " ".join(args).strip() == "n8n start" and cwd == _N8N_ROOT.resolve()
    executable_matches = (Path("/proc") / str(pid) / "exe").resolve() == _NODE24.resolve()
    same_uid = (Path("/proc") / str(pid)).stat().st_uid == os.getuid()
    if not (script_matches or titled_owner) or not executable_matches or not same_uid or \
            f"N8N_USER_FOLDER={_canonical_user_folder()}" not in env:
        raise ValueError("n8n_listener_is_not_canonical_owner")
    return pid


def _run_cli_execute(workflow_id: str, *, expected_graph_hash: str = "") -> dict[str, Any]:
    """Reuse the canonical CLI with an exclusive, reversible server/CLI handoff.

    CLI execute owns a broker too. It cannot coexist with the native server on
    the same broker. Never interrupt scheduled workflows or in-flight runs; keep
    external runners and the same database/token, and restore the same launcher.
    """
    import fcntl
    if not expected_graph_hash:
        return {"error": "stored_graph_permission_not_bound"}
    if not (_CANONICAL_DATA_ROOT / "database.sqlite").is_file():
        return {"error": "canonical_n8n_database_missing"}
    with (_CANONICAL_RUNTIME_ROOT / "execution.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"error": "canonical_n8n_execution_busy"}
        stopped = False
        container = None
        result: dict[str, Any] = {}
        try:
            container = _canonical_container()
            pid = None if container and container["running"] else _canonical_server_pid()
            if pid is not None or (container and container["running"]):
                state = _n8n_request("GET", "/api/v1/workflows?active=true&limit=1")
                if state.get("error") or not isinstance(state.get("data"), list):
                    return {"error": "n8n_quiescence_unproved"}
                # The existing key deliberately need not acquire execution-read
                # permission. The CLI already owns this same local database.
                with sqlite3.connect(f"file:{_CANONICAL_DATA_ROOT / 'database.sqlite'}?mode=ro", uri=True) as db:
                    pending = db.execute("SELECT COUNT(*) FROM execution_entity WHERE status IN ('new','running','waiting')").fetchone()[0]
                if state["data"] or pending:
                    return {"error": "n8n_active_work_requires_server_side_execution"}
                if container and container["running"]:
                    subprocess.run(["docker", "stop", "--time", "20", container["name"]],
                                   capture_output=True, timeout=30, check=True)
                else:
                    os.kill(pid, signal.SIGTERM)
                stopped = True
                for _ in range(200):
                    if container or _canonical_server_pid() is None:
                        break
                    time.sleep(0.1)
                else:
                    raise ValueError("n8n_canonical_server_stop_timeout")
            # Recheck under the existing exclusive handoff, after the canonical
            # server is stopped. The same CLI/database is the only canonical writer.
            if _stored_workflow_hash(_read_stored_workflow(workflow_id)) != expected_graph_hash:
                result = {"error": "stored_graph_changed_after_policy"}
            else:
                result = _execute_cli_in_canonical_data_root(workflow_id)
        except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
            result = {"error": str(exc) if isinstance(exc, ValueError) else type(exc).__name__}
        finally:
            if stopped:
                if container:
                    try:
                        subprocess.run(["docker", "start", container["name"]], capture_output=True,
                                       timeout=30, check=True)
                    except subprocess.SubprocessError:
                        result["error"] = "n8n_canonical_server_restore_failed"
                else:
                    log_path = _PROJECT_ROOT / "RUNTIME/n8n/logs/canonical-execution-handoff.log"
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    with log_path.open("a") as log:
                        subprocess.Popen(["bash", str(_PROJECT_ROOT / "RUNTIME/n8n/start-canonical-external.sh")],
                                         cwd=_PROJECT_ROOT, stdout=log, stderr=subprocess.STDOUT,
                                         start_new_session=True)
                restored = False
                for _ in range(60):
                    if _n8n_request("GET", "/healthz").get("status") == "ok":
                        ready = _n8n_request("GET", "/api/v1/workflows?limit=1")
                        if not ready.get("error") and isinstance(ready.get("data"), list):
                            restored = True
                            break
                    time.sleep(1)
                result["canonical_server_restored"] = restored
                if not restored:
                    result["error"] = "n8n_canonical_server_restore_failed"
        return result


class ExistingN8nAdapter:
    provider_id = PROVIDER_ID

    def __init__(self) -> None:
        self._policy_graphs: dict[tuple[str, str], tuple[Any, str]] = {}
        self._approved_graphs: dict[tuple[str, str], tuple[Any, str]] = {}

    def prepare_plan_for_policy(self, *, plan: ExecutionPlan, trace_id: str) -> ExecutionPlan:
        """Observe effects below the existing policy owner; model flags are not truth."""
        steps = []
        for step in plan.steps:
            if step.operation != "execute_workflow":
                steps.append(step)
                continue
            key = (trace_id, step.step_id)
            self._policy_graphs.pop(key, None)
            self._approved_graphs.pop(key, None)
            wid = dict(step.parameters).get("workflow_id", "")
            graph = None
            if wid:
                try:
                    graph = _read_stored_workflow(wid)
                except (OSError, ValueError, TypeError, sqlite3.Error):
                    graph = None
            literal = graph is not None and _stored_workflow_has_literal_intrinsic_effects(graph)
            prepared = replace(step, effect_type="EXECUTE", risk_class="MUTATION" if literal else "UNKNOWN",
                               reversibility="REVERSIBLE" if literal else "UNKNOWN", external_side_effect=not literal)
            if graph is not None and str(graph.get("id")) == wid:
                self._policy_graphs[key] = (prepared, _stored_workflow_hash(graph))
            steps.append(prepared)
        return replace(plan, steps=tuple(steps))

    def bind_host_permission(self, *, permissions: tuple[PermissionDecision, ...],
                             plan: ExecutionPlan, trace_id: str) -> None:
        for step in plan.steps:
            key = (trace_id, step.step_id)
            self._approved_graphs.pop(key, None)
            binding = self._policy_graphs.get(key)
            if binding is None or binding[0] != step:
                continue
            if any(decision.granted and not decision.approval_required
                   and decision.trace_id == trace_id and decision.step_id == step.step_id
                   and decision.operation_id == step.operation and decision.capability_id == step.capability_id
                   for decision in permissions):
                self._approved_graphs[key] = binding

    def health(self) -> dict[str, Any]:
        result = _n8n_request("GET", "/healthz")
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE" if result.get("status") == "ok" else "UNAVAILABLE",
            "base_url": N8N_BASE_URL,
            "catalog": "local n8n 2.42.6 node catalog (offline)",
            "network_required": False,
            "external_side_effect": False,
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
        allowed = {c["operation_id"] for cs in N8N_CAPABILITY_OPERATION_CONTRACTS.values() for c in cs}
        state: dict[str, Any] = {}

        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            if step.operation not in allowed:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            params = dict(step.parameters)
            if step.operation == "build_workflow":
                try:
                    params = {**params, "logical_spec": _architect_logical_spec(str(params.get("task") or ""))}
                except (ValueError, TypeError, json.JSONDecodeError) as exc:
                    errors.append(f"build_workflow:{str(exc)}")
                    continue
            if step.operation in {"create_workflow", "build_workflow"}:
                # The logical automation spec is model-supplied; the HOST compiles it to exact
                # installed n8n contracts. Fails closed without a valid compiled graph.
                try:
                    workflow, compile_error = _compiled_workflow_spec(
                        params, source_text=understanding.original_text,
                        allowed_jarvis_capability_ids=frozenset(
                            requirement.capability_id for requirement in understanding.required_capabilities
                            if requirement.required and requirement.capability_id != "workflow_automation:n8n"
                        ),
                    )
                except (ValueError, TypeError) as exc:
                    # Preserve the existing typed validator rejection at this
                    # provider boundary; do not turn invalid authoring into an
                    # unhandled runtime exception or a provider write.
                    errors.append(f"create_workflow:{str(exc)}")
                    continue
                if workflow is None:
                    errors.append(f"create_workflow:{compile_error or 'missing_or_invalid_workflow_spec'}")
                    continue
                # Consume bounded Automation Organ authoring context at the
                # canonical provider boundary; skills can advise compilation
                # but cannot execute, authorize, or emit evidence.
                skill_context = load_automation_n8n_private_skill_context(
                    tuple(skill for skill in select_skills_for_tools(("workflow_automation:n8n",), ())
                          if skill != "automation_n8n")
                    or ("using-n8n-skills-official", "n8n-node-configuration-official")
                )
                binding_report = tuple(workflow.pop("_jarvis_binding_report", ()))
                created = _n8n_request("POST", "/api/v1/workflows", workflow)
                if created.get("error") or not created.get("id"):
                    errors.append(f"create_workflow:{created.get('error', 'no_id')}")
                    continue
                state["workflow_id"] = created["id"]
                dispositions = tuple(dict.fromkeys(
                    str(item.get("disposition")) for item in binding_report if item.get("disposition")
                ))
                observation = json.dumps({
                    "workflow_id": created["id"], "name": created.get("name"), "active": bool(created.get("active", False)),
                    "binding_dispositions": dispositions, "binding_report": binding_report,
                    "authoring_skill_ids": skill_context["skill_ids"],
                }, ensure_ascii=False)
                items.append(EvidenceItem(
                    kind="n8n_workflow", source=f"{self.provider_id}:create_workflow",
                    observation=observation, scope="local_workflow_automation", confidence=1.0,
                    trace_id=trace_id, observed_at=utc_observed_at(),
                    content_hash=f"sha256:{hashlib.sha256(observation.encode('utf-8')).hexdigest()}",
                    source_reference=created["id"], truncated=False, omitted_count=0,
                    request_id=understanding.request_id, step_id=step.step_id,
                    capability_id=step.capability_id, operation_id=step.operation, provider_id=self.provider_id,
                ))
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                    trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                    operation_id=step.operation, provider_id=self.provider_id,
                    status="COMPLETE", result=f"created real n8n workflow {created['id']}",
                ))
            elif step.operation == "inspect_workflow":
                wid = str(state.get("workflow_id") or params.get("workflow_id") or "")
                if not wid:
                    errors.append("inspect_workflow:missing_workflow_id")
                    continue
                inspected = _n8n_request("GET", f"/api/v1/workflows/{wid}")
                if inspected.get("error") or not inspected.get("id"):
                    errors.append(f"inspect_workflow:{inspected.get('error', 'no_id')}")
                    continue
                node_types = [n.get("type") for n in inspected.get("nodes", [])]
                observation = json.dumps({"workflow_id": inspected["id"], "name": inspected.get("name"), "node_types": node_types}, ensure_ascii=False)
                items.append(EvidenceItem(
                    kind="n8n_workflow", source=f"{self.provider_id}:inspect_workflow",
                    observation=observation, scope="local_workflow_automation", confidence=1.0,
                    trace_id=trace_id, observed_at=utc_observed_at(),
                    content_hash=f"sha256:{hashlib.sha256(observation.encode('utf-8')).hexdigest()}",
                    source_reference=inspected["id"], truncated=False, omitted_count=0,
                    request_id=understanding.request_id, step_id=step.step_id,
                    capability_id=step.capability_id, operation_id=step.operation, provider_id=self.provider_id,
                ))
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                    trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                    operation_id=step.operation, provider_id=self.provider_id,
                    status="COMPLETE", result=f"read back n8n workflow {inspected['id']} with {len(node_types)} nodes",
                ))
            elif step.operation == "execute_workflow":
                wid = str(state.get("workflow_id") or params.get("workflow_id") or "")
                if not wid:
                    errors.append("execute_workflow:missing_workflow_id")
                    continue
                binding = self._approved_graphs.pop((trace_id, step.step_id), None)
                self._policy_graphs.pop((trace_id, step.step_id), None)
                if binding is None or binding[0] != step:
                    errors.append("execute_workflow:stored_graph_permission_not_bound")
                    continue
                exec_result = _run_cli_execute(wid, expected_graph_hash=binding[1])
                success = exec_result.get("returncode") == 0 and exec_result.get("execution_status") == "success" and exec_result.get("canonical_server_restored", True)
                observation = json.dumps({
                    "workflow_id": wid, "stored_graph_sha256": binding[1], "returncode": exec_result.get("returncode"),
                    "status": "success" if success else "failed",
                    "execution_id": exec_result.get("execution_id", ""),
                    "execution_result": exec_result.get("execution_result", {"readback_status": "UNAVAILABLE"}),
                }, ensure_ascii=False)
                if not success:
                    errors.append("execute_workflow:non_success_status")
                items.append(EvidenceItem(
                    kind="n8n_execution", source=f"{self.provider_id}:execute_workflow",
                    observation=observation, scope="local_workflow_automation",
                    confidence=1.0 if success else 0.0,
                    trace_id=trace_id, observed_at=utc_observed_at(),
                    content_hash=f"sha256:{hashlib.sha256(observation.encode('utf-8')).hexdigest()}",
                    source_reference=wid, truncated=False, omitted_count=0,
                    request_id=understanding.request_id, step_id=step.step_id,
                    capability_id=step.capability_id, operation_id=step.operation, provider_id=self.provider_id,
                ))
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                    trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                    operation_id=step.operation, provider_id=self.provider_id,
                    status="COMPLETE" if success else "FAILED",
                    result=f"executed n8n workflow {wid}; status={'success' if success else 'failed'}",
                ))
            elif step.operation == "modify_workflow":
                wid = str(state.get("workflow_id") or params.get("workflow_id") or "")
                new_value = str(params.get("value") or "")
                if not wid:
                    errors.append("modify_workflow:missing_workflow_id")
                    continue
                if not new_value:
                    errors.append("modify_workflow:missing_value")
                    continue
                current = _n8n_request("GET", f"/api/v1/workflows/{wid}")
                if current.get("error") or not current.get("nodes"):
                    errors.append(f"modify_workflow:{current.get('error', 'no_nodes')}")
                    continue
                # mutate the Set node's fixed value in the stored graph
                modified = False
                for node in current["nodes"]:
                    assignments = node.get("parameters", {}).get("assignments", {}).get("assignments")
                    if isinstance(assignments, list):
                        for a in assignments:
                            if a.get("name") == "value":
                                a["value"] = new_value
                                modified = True
                if not modified:
                    errors.append("modify_workflow:no_mutable_value_field")
                    continue
                body = {"name": current.get("name", "jarvis_local_automation"), "nodes": current["nodes"],
                        "connections": current.get("connections", {}), "settings": current.get("settings", {"executionOrder": "v1"})}
                updated = _n8n_request("PUT", f"/api/v1/workflows/{wid}", body)
                if updated.get("error"):
                    errors.append(f"modify_workflow:{updated.get('error', 'put_failed')}")
                    continue
                # A PUT acknowledgement proves request acceptance, not stored state.
                # Reuse the same provider read boundary and check each modified field
                # against its actual workflow/node identity before issuing COMPLETE.
                stored = _n8n_request("GET", f"/api/v1/workflows/{wid}")
                stored_nodes = stored.get("nodes") if isinstance(stored, dict) else None
                readback_error = ""
                if not isinstance(stored, dict) or stored.get("error"):
                    readback_error = "stored_readback_unavailable"
                elif str(stored.get("id", "")) != wid or not isinstance(stored_nodes, list):
                    readback_error = "stored_readback_identity_invalid"
                else:
                    for requested_node in body["nodes"]:
                        requested_assignments = requested_node.get("parameters", {}).get("assignments", {}).get("assignments")
                        if not isinstance(requested_assignments, list):
                            continue
                        targets = [a for a in requested_assignments if a.get("name") == "value"]
                        if not targets:
                            continue
                        identity_key = "id" if requested_node.get("id") else "name"
                        node_identity = requested_node.get(identity_key)
                        matches = [n for n in stored_nodes if isinstance(n, dict)
                            and node_identity and n.get(identity_key) == node_identity]
                        if len(matches) != 1:
                            readback_error = "stored_readback_node_identity_invalid"
                            break
                        assignments = matches[0].get("parameters", {}).get("assignments", {}).get("assignments")
                        for target in targets:
                            field_key = "id" if target.get("id") else "name"
                            fields = [a for a in (assignments if isinstance(assignments, list) else [])
                                if isinstance(a, dict) and a.get(field_key) == target.get(field_key)]
                            if len(fields) != 1 or fields[0].get("value") != new_value:
                                readback_error = "stored_readback_value_mismatch"
                                break
                        if readback_error:
                            break
                if readback_error:
                    errors.append(f"modify_workflow:{readback_error}")
                    receipts.append(ExecutionReceipt(
                        receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                        trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                        operation_id=step.operation, provider_id=self.provider_id, status="FAILED",
                        result=f"n8n workflow {wid} PUT acknowledged; stored change unverified: {readback_error}",
                    ))
                    continue
                observation = json.dumps({"workflow_id": wid, "new_value": new_value, "modified": modified}, ensure_ascii=False)
                items.append(EvidenceItem(
                    kind="n8n_workflow", source=f"{self.provider_id}:modify_workflow",
                    observation=observation, scope="local_workflow_automation", confidence=1.0,
                    trace_id=trace_id, observed_at=utc_observed_at(),
                    content_hash=f"sha256:{hashlib.sha256(observation.encode('utf-8')).hexdigest()}",
                    source_reference=wid, truncated=False, omitted_count=0,
                    request_id=understanding.request_id, step_id=step.step_id,
                    capability_id=step.capability_id, operation_id=step.operation, provider_id=self.provider_id,
                ))
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                    trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                    operation_id=step.operation, provider_id=self.provider_id,
                    status="COMPLETE", result=f"modified n8n workflow {wid} value -> {new_value}",
                ))

        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        capability_ids = tuple(dict.fromkeys(step.capability_id for step in plan.steps))
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=(capability_ids[0] if capability_ids else "workflow_automation:n8n"),
            trace_id=trace_id,
            status=status,
            items=tuple(items),
            limitations=(() if status == "COMPLETE" else ("n8n automation execution incomplete",)),
            receipts=tuple(receipts),
            errors=tuple(errors),
            capability_ids=capability_ids,
        )


__all__ = [
    "ExistingN8nAdapter",
    "N8N_CAPABILITY_OPERATION_CONTRACTS",
    "PROVIDER_ID",
]
