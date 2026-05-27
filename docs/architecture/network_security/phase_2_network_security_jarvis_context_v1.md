# PHASE 2 — Network Security / VPN / P2P Base — JARVIS Context v1

Purpose:
This document explains PHASE 2 for future JARVIS/operator reasoning.
It is not a blocking policy gate.
It is not a deployment approval.
It is not a restriction against future optimization.
It is an architectural context map for maintenance, extension, debugging and product evolution.

## What PHASE 2 added

PHASE 2 built the base network-security foundation for:
- network backend adapter boundaries;
- VPN profile/session/egress contracts;
- server-side VPN runtime read models;
- dashboard-safe VPN status preview;
- Android VPN shell integration;
- iOS VPN shell integration;
- shared P2P Mesh / Floating Master contracts;
- Android/iOS P2P node shell adapters;
- network-security cube container readiness.

## Main source-of-truth areas

Canonical network security contracts:
- `MAKSIMAR_CORE_LIB/network_security/`

Server runtime/read-model layer:
- `MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/`

Shared mobile P2P/Floating Master projection:
- `shared_mobile_core/p2p_mesh_network/`

Android shell surfaces:
- `ANDROID_SHELL/network_vpn/`
- `ANDROID_SHELL/p2p_node_adapter/`

iOS shell surfaces:
- `IOS_SHELL/network_vpn/`
- `IOS_SHELL/p2p_node_adapter/`

Network security container readiness:
- `CONTAINER_DEPLOYMENT/cubes/network_security/`

Global container/deployment source:
- `CONTAINER_DEPLOYMENT/`

## What JARVIS should understand

The network-security layer is currently a safe foundation, not a live VPN/P2P deployment.

It exposes:
- state contracts;
- read-only dashboard models;
- mobile shell projections;
- P2P/Floating Master candidate state;
- container-readiness metadata.

It does not yet execute:
- real VPN tunnels;
- real P2P networking;
- peer discovery;
- socket operations;
- Android/iOS system VPN/network APIs;
- floating-master election;
- Docker/Compose deployment.

## How layers connect

`MAKSIMAR_CORE_LIB/network_security` defines the canonical policy and adapter contracts.

`MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME` reads those contracts and exposes server-side read models.

`shared_mobile_core/p2p_mesh_network` provides shared P2P/Floating Master projections for both Android and iOS.

`ANDROID_SHELL/*` and `IOS_SHELL/*` expose platform shell state without becoming source-of-truth.

`CONTAINER_DEPLOYMENT/cubes/network_security` describes container readiness for this cube while reusing the global container deployment layer.

## Dashboard meaning

Dashboard surfaces may show:
- VPN disabled/enabled policy state;
- egress policy state;
- server network posture;
- P2P mesh disabled state;
- Floating Master candidate state;
- Android/iOS shell readiness;
- container readiness.

Dashboard surfaces are read-only at this phase.

## Future development directions

Future JARVIS/operator work may extend this phase by adding:
- real VPN adapter implementation behind approval gates;
- real tunnel lifecycle manager;
- real P2P discovery implementation;
- real Floating Master election with audit and rollback;
- mobile platform permission flows;
- dashboard control-plane handoff;
- container runtime integration;
- telemetry and observability;
- policy-bound deployment path.

Any future implementation should preserve the source-of-truth separation and use explicit approval/deployment gates.

## Optimization notes

Potential optimization areas:
- reduce repeated safety invariant fields through shared helper models;
- add a unified network-security read-model summary;
- add dashboard grouping for VPN, P2P, mobile shell and container readiness;
- add generated documentation from contract metadata;
- add stronger trace/correlation IDs for network state changes;
- add future simulation mode before live network execution.

## Context status

This document is a JARVIS-readable explanation map.
Acceptance and safety invariants remain in:
- `docs/architecture/network_security/phase_2_network_security_acceptance_v1.md`
- tests under `tests/network_security/`, `tests/mobile_network/`, `tests/mobile_p2p/`, `tests/container_readiness/`
