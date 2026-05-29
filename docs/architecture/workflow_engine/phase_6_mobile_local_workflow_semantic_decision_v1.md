# PHASE 6 Mobile Local Workflow Semantic Decision v1

Scope: semantic boundary for mobile local workflow automation in Product Roadmap PHASE 6.

## Decision

mobile app = local-first JARVIS node
server = optional senior/accelerator hub
n8n = external server adapter/container/runtime, not immutable core
Mobile Local Workflow Engine = first-class local mobile automation layer
n8n-compatible graph semantics
Android/iOS capability profiles modeled separately
local AI workflow proposal is not execution authority
no hidden remote control
no direct phone control without explicit permission and approval
no direct core/server canonical write
dashboard/preview read-only
OSS download/install only after vendor gate + sandbox boundary

Mobile local workflow automation is a first-class local mobile automation layer. It is separate from the server n8n adapter and from any screen observer or remote assistance surface.

The mobile app acts as a local-first JARVIS node. It may propose safe app or device workflows, but execution intent is valid only when explicit user permission and approval are present. The server acts as an optional senior or accelerator hub. n8n remains an external server adapter, container, and runtime.

## Required Contracts

PHASE 6 must include contract coverage for:

- local workflow scope
- local AI workflow proposal
- mobile workflow permission profile
- Android local workflow intent client
- iOS local workflow intent client
- workflow status bridge

## Local Workflow Scope

Local workflow scope defines which app-local workflow actions may be proposed. It must distinguish app-local automation from direct phone control. It must make local-only, permission-gated, approval-gated, audit-visible, and dashboard-visible state explicit.

## Local AI Workflow Proposal

The local AI proposal contract describes a proposed workflow graph and its safety classification. A proposal is not execution authority. It cannot write core, write server canonical state, open network connections, mutate runtime state, or bypass user approval.

## Mobile Workflow Permission Profile

The permission profile is the gate between proposal and execution intent. It must model explicit user permission, user approval, capability limits, audit requirements, and revocation. Permission must be visible and cannot be implied by dashboard state.

## Android And iOS Boundaries

Android and iOS capability limits must be modeled separately because the platforms expose different permission and background execution rules. Platform clients in PHASE 6 are intent clients and bridges only. They must not call real platform APIs in contract batches.

## n8n Boundary

n8n compatibility means graph semantics can map to n8n-like nodes, edges, triggers, actions, and execution metadata. It does not mean mobile embeds n8n or that n8n becomes core. Server-side n8n integration must stay inside `MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/` and container surfaces.

## Forbidden Behavior

- hidden remote control
- direct phone control without explicit user permission and approval
- direct core write
- direct server canonical write
- network, socket, or tunnel opening from contracts
- runtime mutation from dashboard or preview
- external open-source download or install before vendor gate and sandbox boundary

## Implementation Rule

PHASE 6 implementation must extend existing workflow surfaces and keep mobile local workflow separate from server n8n runtime. Any future runtime execution must be explicitly modeled, policy-gated, approval-gated, audit-visible, and tested.
