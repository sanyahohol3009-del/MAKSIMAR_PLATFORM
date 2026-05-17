# SECURITY_LAYER

## Status

PHASE 1 / BATCH 1.1 — Security Layer Surface.

This layer is the official security foundation surface for MAKSIMAR/JARVIS.

## Purpose

SECURITY_LAYER defines the future hardened boundary for:

- RBAC
- policy enforcement
- approval service
- execution bundle verification
- voice identity checks
- vault boundary
- signature verification
- USB guard
- media quarantine
- security telemetry

## Current batch scope

BATCH 1.1 creates only the official surface, manifest, container boundary, policy config, and references to existing security-related sources.

It does not implement runtime authorization yet.

## Non-negotiable rules

1. No runtime mutation.
2. No canonical write.
3. No UI-to-execution path.
4. No dashboard mutation.
5. No direct import from future container service into legacy runtime.
6. No movement of existing policy/governance/security files.
7. Existing working files stay in place.
8. New container-ready paths must use adapter/facade boundaries.

## Dashboard output

The layer may expose read-only status fields later:

- security layer surface ready
- manifest present
- container boundary present
- existing bindings present
- runtime mutation allowed
- canonical write allowed
- direct execution allowed
- dashboard safe
- next action

Dashboard must not execute security decisions.
