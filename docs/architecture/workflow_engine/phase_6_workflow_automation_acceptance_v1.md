# PHASE 6 — Workflow Automation Acceptance v1

## Status

PHASE 6 closes the workflow automation foundation as a controlled, local-first, policy-gated workflow layer.

This document is a JARVIS-readable acceptance map for the workflow automation phase. It explains what was added, where the source-of-truth files live, what is intentionally read-only, what is intentionally disabled, and which extension points remain batch-controlled.

## Accepted scope

PHASE 6 contains these closed batches:

- BATCH 6.0 — PHASE 6 Registry Reconciliation / Mobile Local Workflow Correction.
- BATCH 6.1 — Workflow Graph Contracts.
- BATCH 6.2 — Workflow Governance Contracts.
- BATCH 6.3 — Server Workflow Runtime / n8n Adapter Boundary.
- BATCH 6.4 — Android/iOS Mobile Local Workflow Engine Boundary.
- BATCH 6.5 — Workflow Dashboard / Preview / Container Contract.
- BATCH 6.6 — PHASE 6 Acceptance.

## Source-of-truth surfaces

### Registry and semantic correction

- `docs/architecture/workflow_engine/phase_6_workflow_automation_registry_reconciliation_v1.md`
- `docs/architecture/workflow_engine/phase_6_mobile_local_workflow_semantic_decision_v1.md`
- `tests/workflow_engine/test_phase_6_registry_reconciliation_smoke.py`
- `tests/workflow_engine/test_phase_6_mobile_local_workflow_semantic_decision_smoke.py`

These files define the corrected meaning of PHASE 6: workflow automation must be local-first for mobile, server-optional, approval-gated, and external-adapter-bound for n8n.

### Workflow graph contracts

- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_graph_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_node_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_edge_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/local_workflow_scope_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/n8n_graph_compatibility_contract.py`

These files define graph, node, edge, local scope, execution tier, and n8n compatibility semantics. They extend the existing `MAKSIMAR_CORE_LIB/workflow_engine/` layer and do not create a parallel workflow core.

### Workflow governance contracts

- `MAKSIMAR_CORE_LIB/workflow_engine/local_ai_workflow_proposal_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/mobile_workflow_permission_profile.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_approval_gate_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_audit_contract.py`
- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_safety_policy_contract.py`

These files define proposal, permission, approval, audit, and safety-policy gates. A proposal is not execution authority. A workflow intent requires explicit permission, device-owner confirmation where applicable, approval, audit, and safety-policy acceptance.

### Server workflow runtime boundary

- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/__init__.py`
- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_adapter_contract.py`
- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/workflow_runtime_policy.py`
- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/workflow_execution_intent_runtime.py`
- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_vendor_gate_runtime.py`

These files define server-side runtime boundary contracts. The server is an optional accelerator and control-plane participant, not a bypass around mobile-local permission and approval.

n8n is accepted only as an external server adapter/container/runtime boundary. It is not embedded into immutable core and is not canonical workflow truth.

### Android/iOS mobile-local workflow boundary

- `ANDROID_SHELL/workflow_adapter/android_local_workflow_intent_client.py`
- `ANDROID_SHELL/workflow_adapter/android_workflow_permission_bridge.py`
- `ANDROID_SHELL/workflow_adapter/android_workflow_capability_limits.py`
- `IOS_SHELL/workflow_adapter/ios_local_workflow_intent_client.py`
- `IOS_SHELL/workflow_adapter/ios_workflow_permission_bridge.py`
- `IOS_SHELL/workflow_adapter/ios_workflow_capability_limits.py`

These files define mobile-local workflow intent clients, permission bridges, and capability limits for Android and iOS. Mobile remains a local-first JARVIS node. Server participation is optional and must not override local permission, local approval, local audit, or safety policy.

### Dashboard, preview, and container boundary

- `MAKSIMAR_CORE_LIB/workflow_engine/workflow_status_bridge.py`
- `tools/workflow_status_preview.py`
- `CONTAINER_DEPLOYMENT/cubes/workflow_automation/container_contract.yaml`
- `CONTAINER_DEPLOYMENT/cubes/workflow_automation/runtime_profile.yaml`
- `CONTAINER_DEPLOYMENT/cubes/workflow_automation/network_policy.yaml`

These files expose workflow automation status to dashboard/preview as read-only data. The container contract declares workflow automation as an external-adapter-bound cube. The runtime profile keeps the phase in intent-metadata-only mode. The network policy disables network/socket/tunnel by default.

## Accepted guarantees

PHASE 6 accepts the following guarantees:

- Workflow graph structure exists and is n8n-compatible without making n8n core truth.
- Local workflow scope exists for `mobile_local`, `server_local`, `hybrid`, and `cloud_optional` routing semantics.
- Local AI workflow proposal exists, but proposal is not execution authority.
- Mobile permission profile requires explicit user permission and device owner confirmation.
- Approval gate blocks direct phone control and hidden remote control.
- Audit contract records workflow events without granting execution authority.
- Safety policy blocks critical risk, missing permission, missing approval, unsafe flags, direct core write, direct server canonical write, hidden remote control, direct phone control, dashboard execution, runtime mutation, network/socket/tunnel by default, and platform API bypass.
- Server runtime creates policy-gated intent metadata only.
- n8n adapter boundary is external, sandbox-gated, vendor-gated, and not production-enabled.
- Android/iOS workflow clients create metadata-only local intent decisions.
- Android/iOS permission bridges reuse existing `MobileWorkflowPermissionProfile`.
- Android/iOS capability limits are local-first and server-optional.
- Workflow dashboard and preview surfaces are read-only.
- Workflow container contract, runtime profile, and network policy are declared.
- n8n download, install, and production runtime are disabled by default.
- Network, socket, tunnel, inbound connections, outbound connections, and external internet are disabled by default for workflow automation.
- No duplicate workflow root was created.
- No parallel mobile workflow world was created.
- No dashboard-to-execution path was created.
- No direct phone control path was created.
- No hidden remote control path was created.
- No direct write path into immutable core was created.
- No direct write path into server canonical state was created.

## Explicitly not accepted as implemented runtime

The following capabilities are not accepted as active runtime in PHASE 6:

- Real n8n download.
- Real n8n install.
- Real n8n production runtime.
- Real workflow execution.
- Real phone control.
- Hidden remote control.
- Dashboard-triggered workflow execution.
- Preview-triggered workflow execution.
- Network/tunnel/socket activation.
- Direct filesystem mutation outside approved contracts.
- Direct core mutation.
- Direct server canonical mutation.
- Platform API call execution from mobile workflow clients.

These capabilities require separate batch-controlled design, explicit operator approval, vendor/security gate where applicable, sandbox preview, tests, container boundary, network exception policy, and audit.

## Dashboard and preview meaning

The workflow dashboard surface is a read-model surface only. It may show:

- graph contract readiness;
- governance contract readiness;
- server n8n adapter boundary readiness;
- Android/iOS mobile-local workflow boundary readiness;
- workflow automation container contract status;
- runtime profile status;
- network policy status;
- disabled runtime and network state.

It must not execute workflow actions.

The preview tool `tools/workflow_status_preview.py` produces deterministic JSON. It is read-only and must not mutate runtime, core, server state, mobile state, filesystem state, network state, or container state.

## Container and network meaning

The workflow automation container contract declares the boundary for future containerized adapter runtime.

The runtime profile declares the current runtime mode as `intent_metadata_only`.

The network policy declares default disabled network posture:

- no network by default;
- no socket by default;
- no tunnel by default;
- no inbound connections by default;
- no outbound connections by default;
- no external internet by default;
- no service discovery by default.

Any network exception must be explicit, policy-controlled, operator-approved, security-scanned, container-bound, and audited.

## JARVIS reasoning map

When future JARVIS reasoning touches workflow automation, it must treat these surfaces as canonical for PHASE 6:

1. Graph model: `MAKSIMAR_CORE_LIB/workflow_engine/*graph*`, `*node*`, `*edge*`, `local_workflow_scope_contract.py`.
2. Governance model: proposal, permission, approval, audit, safety policy.
3. Server adapter boundary: `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/`.
4. Mobile local boundary: `ANDROID_SHELL/workflow_adapter/` and `IOS_SHELL/workflow_adapter/`.
5. Dashboard/preview boundary: `workflow_status_bridge.py` and `tools/workflow_status_preview.py`.
6. Container/network boundary: `CONTAINER_DEPLOYMENT/cubes/workflow_automation/`.

Future expansion must extend these layers instead of creating a second workflow engine, second mobile workflow stack, second dashboard root, or direct n8n core integration.

## Acceptance test map

- `tests/workflow_engine/test_phase_6_workflow_engine_acceptance_smoke.py`
- `tests/workflow_engine/test_phase_6_mobile_local_workflow_acceptance_smoke.py`
- `tests/workflow_engine/test_phase_6_n8n_adapter_boundary_acceptance_smoke.py`

These tests verify that PHASE 6 surfaces exist, are importable where appropriate, keep mobile local workflow policy-gated, keep n8n external, keep dashboard read-only, keep runtime metadata-only, and keep network/socket/tunnel disabled by default.

## Final acceptance statement

PHASE 6 is accepted when:

- batches 6.0 through 6.6 are READY in the roadmap file readiness map;
- target acceptance tests pass;
- workflow dashboard/preview remains read-only;
- mobile workflow remains local-first and explicit-permission-gated;
- n8n remains external, vendor-gated, sandbox-gated, and disabled by default;
- workflow automation network policy remains disabled by default;
- roadmap post-step drift check passes;
- unrelated dirty or untracked surfaces remain excluded from PHASE 6 commits.
