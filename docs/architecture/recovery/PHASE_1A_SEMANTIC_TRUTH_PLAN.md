# Phase 1A Semantic Truth Plan

Status: mandatory pre-implementation architecture and acceptance plan.

## Current facts

1. Model understanding is invoked from `CONTROL_PLANE/api_server.py::_model_request_understanding`.
   That function currently builds an Ollama `/api/chat` payload itself and calls the shared transport.
   `CONTROL_PLANE/canonical_project_read_spine.py::run_canonical_semantic_project_read` builds the
   semantic prompt, invokes that callback and validates its output.
2. `RequestUnderstanding` is a versioned Core contract in
   `MAKSIMAR_CORE_LIB/ai_orchestration/semantic_intent_contract.py`; strict construction from model
   JSON is performed by `helper_model_decision_parser.py::parse_request_understanding_payload`.
3. Marker-based routing remains reachable only through the `/hot` rollback call to
   `tools/jarvis_live_runtime/live_intent_policy.py::handle_hot_request`. Its collaborators
   `live_semantic_intent.py`, `direct_capability_dispatcher.py` and `read_only_tool_router.py`
   contain phrases, token roots and deterministic intent families. None may select `project.read`
   on the Phase 1A canonical path.
4. The existing 25 paraphrase cases inject model JSON that already contains `project.read`.
   They prove parser/orchestrator plumbing, not that a real model inferred the capability.
5. Acceptance is split into four layers: deterministic unit plumbing tests; malformed/valid model
   parser tests; a separately reported real-local-model harness over 20 positive, 12 mutation and
   6 multi-goal requests; and HTTP/lifecycle probes over the composed runtime. Model prose is never
   compared exactly.
6. `capability_registry_loader.py::discover_capability_providers` currently special-cases
   `project.read` and maps it to `cap_module_manifest_surface`. This is a temporary bridge, not a
   real capability manifest.
7. `canonical_project_read_spine.py` constructs `CapabilityCandidate` with
   `permissions_granted=True`; no policy decision or identity source is recorded.
8. `api_server.py::jarvis_live_hot` currently evaluates
   `payload.get("owner_voice_gate_open", True)`, so a missing HTTP field is treated as owner access.
   The new semantic boundary must fail closed. Existing PC Control implementation is out of scope.
9. Provider-unavailable and failed/empty Final Brain results can produce `response_text=""`.
   The HTTP envelope then reports failure without a useful bounded response.
10. Understanding, provider collection and Final Brain calls are synchronous. Understanding has a
    transport timeout, Final Brain uses 180 seconds, and the canonical orchestrator has no shared
    total deadline or cancellation propagation.
11. `project_understanding_adapter.py::collect_evidence` serializes arbitrary payloads and applies
    `[:12000]`, which can cut JSON mid-token and loses omitted-item metadata and references.

## Phase 1A implementation boundary

The slice will change only the existing semantic project-read composition and its contracts:

- extend the existing semantic contract with deadline/cancellation, identity, permission decision,
  model-understanding and Final-Brain public ports, plus bounded evidence metadata;
- add one real `project.read.v1` manifest to the existing canonical registry and make discovery
  generic and schema-driven;
- reuse the existing Ollama transport behind one model adapter injected by Control Plane;
- implement a minimal project-read permission evaluator over existing owner/family identity
  contracts, defaulting unknown HTTP identity to non-owner and granting only configured read access;
- bound every project operation independently and allow partial evidence;
- place the existing dynamic Final Brain bridge behind one explicitly registered
  `TEMPORARY_COMPATIBILITY_SHIM`, with no new string-import sites;
- normalize every canonical result to non-empty honest text and preserve one trace/deadline;
- centralize architecture-radar exclusions for archives/generated evidence without suppressing real
  Core/Server/tools or private-import violations;
- add focused tests and the real-model/HTTP acceptance harnesses. Acceptance phrases live only in
  test/audit data, never production routing or manifests.

Planned production files are the existing Phase 1 files above, the canonical capability registry
package/YAML surface, one manifest beneath that same registry root, the existing project adapter,
the existing server adapter plus its single named compatibility shim, and architecture-radar
configuration. Planned tests remain under existing `tests/` roots. No PC, voice, memory-write,
agent-chat, device, container or legacy-loop implementation is changed.

## Dependency direction

```text
MAKSIMAR_CORE_LIB contracts and ports
                ^
existing model/project/final-brain adapters
                ^
CONTROL_PLANE composition root
```

Core imports no Ollama, tools or server implementation. Capability requirements precede manifest
discovery, permission, health and provider selection. The composition root may instantiate existing
adapters. The compatibility shim is a declared temporary exception at the server/tools boundary,
not a hidden import from orchestration.

## Measurement and budgets

Before final budget values are claimed, the real harness will record understanding, provider,
Final Brain and total latency samples and calculate p50/p95. Defaults will be derived from those
measurements with a documented bounded margin and remain environment-configurable. If staging is
unavailable or too few valid samples exist, the phase exit gate stays failed and conservative
temporary test budgets are labelled provisional rather than measured defaults.

## Rollback

Stop through `tools/rest`; remove only the Phase 1A composition additions listed in the audit
changed-file allowlist; restore the Phase 1 model callback, registry bridge, adapter and Final Brain
adapter from `tracked_diff_before.patch` plus the preserved untracked allowlist; then run compileall
and Phase 1 focused tests. Never reset, clean, checkout, restore or delete unrelated untracked data.
Per request, invalid understanding or a non-project capability continues to use explicit
`legacy_rollback`; provider/Final-Brain failure returns bounded degradation without mutation.
