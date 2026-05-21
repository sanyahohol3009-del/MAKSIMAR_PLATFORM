# AI_ORCHESTRATION Container Boundary v1

## Scope

This document defines the container and runtime boundary for PHASE 5 / BATCH 5.5.

AI_ORCHESTRATION is an orchestration and acceptance layer. It is not a deployment layer.

## Container rules

- No production deployment.
- No active Docker deployment.
- No active Compose deployment.
- No public exposure.
- No runtime network mutation.
- No direct model runtime execution.
- No direct ACTION_LIBRARY execution.
- No direct WORKFLOW_ENGINE execution.

## Adapter boundary

Runtime adapters may point to existing services:

- AI_SERVICES
- MAKSIMAR_SERVER/WORKERS
- CONTROL_PLANE ai router binding

Runtime adapters must remain:

- read-only;
- dashboard-safe;
- proposal-only;
- non-mutating;
- non-deploying.

## Safety state

container_boundary_ready: true  
runtime_mutation_allowed: false  
deployment_allowed: false  
public_exposure_allowed: false  
dashboard_safe: true
