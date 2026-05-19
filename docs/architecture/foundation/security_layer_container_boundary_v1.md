# SECURITY_LAYER Container Boundary v1

## Boundary rule

SECURITY_LAYER is container-ready by architecture, but this phase does not deploy a container and does not move legacy runtime files.

## Allowed pattern

existing code
→ stable contract
→ adapter/facade
→ container-ready service boundary

## Forbidden pattern

- dashboard to execution;
- direct UI to security runtime;
- direct container write to immutable core;
- duplicated business logic across contract and runtime facade;
- moving legacy policy/governance/security files without correction pass;
- deleting legacy files during security foundation closure.

## Current implementation

- Core contracts live under `MAKSIMAR_CORE_LIB/security_layer`.
- Runtime facades live under `MAKSIMAR_SERVER/SECURITY_LAYER`.
- Adapter/facade boundary lives under `MAKSIMAR_SERVER/SECURITY_LAYER/adapters`.
- Surface and policy declarations live under `SECURITY_LAYER`.

## Dashboard rule

Dashboard reads telemetry and tracer read models only. It does not execute, mutate, approve, deploy, sign, unlock vault data or change policy.
