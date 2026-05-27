# iOS VPN Integration — Phase 2 / Batch 2.6

This directory is an iOS shell-side VPN integration surface.

It is not a real iOS VPN implementation.
It does not call NetworkExtension.
It does not call NEVPN APIs.
It does not create tunnels.
It does not execute permission prompts.
It does not store secrets or credentials.
It does not enable external network access.

Source of truth remains in:

- `MAKSIMAR_CORE_LIB/network_security/*`
- `MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/*`

This layer only exposes iOS VPN profile, permission, state, sync and policy-binding read models.

Hard rules:

- no real iOS NetworkExtension call
- no NEVPN API call
- no tunnel creation
- no permission prompt execution
- no secret material
- no credential material
- no external network access
- no ports opened
- no containers started
- no active deployment
- no runtime mutation
- no source-of-truth override
- no direct core authority
- dashboard/read-model visibility only
- control-plane handoff required
- operator approval required before any future real runtime
