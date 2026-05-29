# PHASE 6 Workflow Automation Registry Reconciliation v1

Scope: Product Roadmap PHASE 6 Workflow Automation / n8n Adapter.

This reconciliation registers PHASE 6 as active roadmap scope while preserving existing workflow surfaces. The active core surface is `MAKSIMAR_CORE_LIB/workflow_engine/`; PHASE 6 extends that package and does not create a second workflow core root.

## Registry Decision

PHASE 6 is registered as seven visible readiness batches:

- 6.0 PHASE 6 Registry Reconciliation / Mobile Local Workflow Correction
- 6.1 Workflow Graph Contracts
- 6.2 Workflow Governance Contracts
- 6.3 Server Workflow Runtime / n8n Adapter Boundary
- 6.4 Android/iOS Mobile Local Workflow Engine Boundary
- 6.5 Workflow Dashboard / Preview / Container Contract
- 6.6 PHASE 6 Acceptance

Batch 6.0 records the correction and must be ready immediately after reconciliation. Product batches 6.1 through 6.6 remain missing until their source, configuration, documentation, and tests are implemented.

## Existing Surfaces To Extend

- `MAKSIMAR_CORE_LIB/workflow_engine/`
- `ANDROID_SHELL/workflow_adapter/`
- `IOS_SHELL/workflow_adapter/`
- `tests/workflow_engine/`

## New Surfaces Reserved By PHASE 6

- `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/`
- `CONTAINER_DEPLOYMENT/cubes/workflow_automation/`
- `tools/workflow_status_preview.py`

## Architecture Boundaries

- mobile app = local-first JARVIS node
- server = optional senior/accelerator hub
- n8n = external server adapter/container/runtime, not immutable core
- Mobile Local Workflow Engine = first-class local mobile automation layer
- n8n-compatible graph semantics
- Android/iOS capability profiles modeled separately
- local AI workflow proposal is not execution authority
- no hidden remote control
- no direct phone control without explicit permission and approval
- no direct core/server canonical write
- dashboard/preview read-only
- OSS download/install only after vendor gate + sandbox boundary

- The mobile app is a local-first JARVIS node.
- The server is an optional senior or accelerator hub.
- n8n is an external server adapter, container, and runtime boundary.
- n8n is not immutable core and does not define workflow truth.
- Mobile Local Workflow Engine is a first-class local mobile automation layer.
- Mobile local workflow uses n8n-compatible graph semantics without embedding server n8n.
- Android and iOS capability profiles are modeled separately.
- Dashboard and preview surfaces are read-only.
- External open-source download or install is allowed only after vendor gate and sandbox boundary approval.

## Safety Invariants

- No hidden remote control channel.
- No direct phone control without explicit user permission and approval.
- No direct core write.
- No direct server canonical write.
- No network, socket, or tunnel opening from contracts or previews.
- No runtime mutation unless explicitly modeled, gated, and approved in a later runtime batch.
- No dashboard action execution.
- No Android or iOS platform API execution in contract batches.

## Reconciliation Outcome

The readiness registry must show batch 6.0 as ready after this reconciliation and batches 6.1 through 6.6 as active missing product scope. This prevents false ready reporting while preserving the existing PHASE 0 through PHASE 5 readiness history.
