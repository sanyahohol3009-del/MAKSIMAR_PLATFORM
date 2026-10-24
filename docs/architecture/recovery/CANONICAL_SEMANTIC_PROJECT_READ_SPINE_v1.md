# Canonical Semantic Project-Read Spine v1

Status: Phase 1 pre-implementation architecture truth.

## Current `/jarvis-live/hot` path

`CONTROL_PLANE/api_server.py::jarvis_live_hot` calls
`tools/jarvis_live_runtime/live_intent_policy.py::handle_hot_request` directly.
That function normalizes text, calls `live_semantic_intent.classify_semantic_intent`,
branches before capability discovery, and only afterwards annotates the result with
`direct_capability_dispatcher.select_capability_for_text`. Ordinary dialogue calls
`hot_dialog.run_hot_dialog`, which calls Ollama without the grounded project context.

The older `jarvis_live_brain_loop` remains reachable through the server adapter,
health/status/project endpoints and terminal surfaces. `/jarvis-live/command` and
`/jarvis-live/chat/stream` are disabled and point callers to `/jarvis-live/hot`.

## Existing semantic routers

- `live_semantic_intent.py`: token-root scores, substring phrases and fixed routes.
- `live_intent_policy.py`: marker branches and canned project/memory responses.
- `direct_capability_dispatcher.py`: marker matchers mapped to capability IDs.
- `read_only_tool_router.py`: fixed intent families and marker predicates.
- `helper_model_orchestration_probe.py`: model classifier, followed by marker-based
  normalization and tool-first decisions.
- `jarvis_live_brain_loop.py`: request planner plus deterministic guarded branches.

None of those mechanisms may decide whether the new Phase 1 request needs
`project.read`. They remain rollback-only for requests outside this slice.

## Existing project-read providers

The reusable implementation is `project_workspace_tools.py`, exposing public,
read-only Git status, tree, file list, search, snippets, outlines and import graph.
`codegraph_readonly_adapter.py`, `project_readonly_analyzer.py`,
`wsl_project_operator.py`, coverage/test audit readers and architecture radar add
specialized evidence. The Phase 1 adapter will aggregate only bounded operations
selected by the model plan; it will not return a prepared answer.

## Existing capability registries and catalogs

- Canonical registry contract: `MAKSIMAR_CORE_LIB/capability_registry` and
  `canonical_capability_registry_v1.yaml`.
- Runtime projection: `existing_capability_inventory.py`.
- Parallel catalogs retained only for compatibility: direct dispatcher catalog,
  JARVIS tool catalog, external adapter registry, model profile registry.

Phase 1 extends discovery over the canonical registry contract. It does not create
another registry. `project.read` is a public requirement ID resolved to a provider
binding backed by existing project tools.

## Final Brain and evidence today

The strongest grounded Final Brain assembly is in
`jarvis_live_brain_loop._build_grounded_answer_prompt` followed by model streaming.
Evidence is currently assembled into mutable tool plans and formatted observation
text by `jarvis_live_project_answer_engine`; several providers return canned answers.
Phase 1 exposes a public grounded Final Brain facade and replaces mutable observation
text on the new path with a typed `EvidenceBundle`.

## Private helper leakage

Current cross-module uses include `_asks_*`, `_load_session_state`,
`_save_session_state`, `_retrieve_history_snippets`, `_empty_session_state`, and
private Final Brain prompt helpers. The new orchestrator imports no underscore
helper from another module.

## Reuse decisions

Reuse: Ollama transport, model profile registry, canonical capability registry,
public project workspace tools, session context read model, grounded Final Brain
policy and `/jarvis-live/hot` response envelope.

Do not reuse in the canonical decision: phrase matchers, marker maps, token-root
scores, deterministic intent families, canned project answers, or tool-first helper
decisions.

## Future slice dependency direction

`MAKSIMAR_CORE_LIB` owns only versioned contracts and the
`ProjectUnderstandingPort`. A project adapter implements that port using existing
public read-only tools. `CONTROL_PLANE` is the composition root that injects the
adapter, canonical registry discovery and existing model/Final Brain facades into
one orchestrator. Core imports neither tools, server internals nor Ollama.

## Rollback

If understanding is unavailable, invalid, low-confidence, unsafe or requests no
`project.read`, the API invokes the existing `handle_hot_request` and records
`orchestration_path=legacy_rollback` plus a machine-readable reason. Removing the
composition-root call restores the previous endpoint without deleting the old brain.

## Planned changed files

- `MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py`
- `MAKSIMAR_CORE_LIB/capability_registry/capability_registry_loader.py`
- `tools/jarvis_live_runtime/project_workspace_tools.py`
- `tools/jarvis_live_runtime/jarvis_live_brain_loop.py`
- `CONTROL_PLANE/api_server.py`
- new focused Phase 1 adapter/orchestrator and tests under existing package roots
- Phase 1 recovery and audit documents

## Current memory reconciliation — 2026-10-11

The sections above preserve the Phase 1 pre-implementation snapshot. Current
execution uses `CONTROL_PLANE/canonical_semantic_spine.py` with typed discovery,
per-step policy and grounded Final Brain; this historical map does not authorize
the old phrase routers or a legacy fallback.

`CanonicalSessionContextStore` remains the owner of the existing append-only
session JSONL. History, qualified developer experience, LearningBundle references,
execution receipts and retrieval traces are projections of that same store.
Restart restoration is bounded by exact identity/session; cached enablement flags
remain descriptive settings rather than host authorization.

The native Mempalace palace is a child source-document archive, not a replacement
for that owner or for original files. `ExistingMemoryRetrievalAdapter` exposes
`search_mempalace` as OBSERVE/READ_ONLY and `refresh_mempalace_source` as
MUTATE/MUTATION under the existing per-step owner policy. Refresh delegates to
the installed native `process_file`, accepts one already indexed project document,
and verifies indexed SHA against current source bytes. It does not enroll a new
corpus, modify the original document, or create another store/runtime.

The existing Final Memory Map consumes the same live federation projection as
JARVIS. Registered views are distinguished from physical stores, and historical
blueprint readiness does not prove populated live memory. Current acceptance and
remaining work are recorded in
`RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011/MASTER_MEMORY_FEDERATION_PROGRESS.md`.

Native writer execution was verified through `/jarvis-live/hot` on 2026-10-11:
the changed source was reindexed in the same palace and current/indexed SHA
matched with zero duplicate chunks. This proves that bounded writer operation;
it does not close the full memory federation or platform acceptance contract.

