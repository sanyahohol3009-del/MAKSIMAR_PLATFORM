# PHASE 2 — Network Security / VPN / P2P Base Acceptance v1

Status: acceptance-ready.

Phase scope:
- Network backend adapter boundary.
- VPN profile / session / egress contracts.
- Server VPN runtime / read models.
- VPN dashboard read models / preview.
- Android VPN shell integration.
- iOS VPN shell integration.
- P2P Mesh / Floating Master shared contracts.
- Android/iOS P2P node shell adapters.
- Network security cube container readiness.

Accepted batches:
- 2.1 — Network Backend Adapter Contract.
- 2.2 — VPN Profile / Session / Egress Contracts.
- 2.3 — Server VPN Runtime / Read Model.
- 2.4 — VPN Dashboard Read Models / Preview.
- 2.5 — Android VPN Integration.
- 2.6 — iOS VPN Integration.
- 2.7 — P2P Mesh / Floating Master.
- 2.8 — Android/iOS P2P Node Adapters.
- 2.9 — Network Container Readiness.
- 2.10 — PHASE 2 Acceptance.

Canonical source boundaries:
- Network security policy and adapter boundary remains in `MAKSIMAR_CORE_LIB/network_security`.
- Server read models remain in `MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME`.
- Shared P2P/Floating Master projection remains in `shared_mobile_core/p2p_mesh_network`.
- Android shell surfaces remain in `ANDROID_SHELL/network_vpn` and `ANDROID_SHELL/p2p_node_adapter`.
- iOS shell surfaces remain in `IOS_SHELL/network_vpn` and `IOS_SHELL/p2p_node_adapter`.
- Container readiness remains cube-specific under `CONTAINER_DEPLOYMENT/cubes/network_security`.
- Global container source remains `CONTAINER_DEPLOYMENT/*`.

Acceptance invariants:
- No real VPN tunnel creation.
- No real P2P networking.
- No peer discovery.
- No sockets opened.
- No ports opened.
- No external network access enabled.
- No Android/iOS system network API execution.
- No floating-master election execution.
- No role election commit.
- No runtime mutation.
- No core write.
- No canonical write.
- No source-of-truth override.
- No direct core authority.
- No active Docker deployment.
- No active Compose deployment.
- No production deployment.
- No privileged container mode.
- No host network.
- No host PID.
- Read-only dashboard/read-model visibility is allowed.
- Control-plane handoff is required.
- Operator approval is required.
- Containerization readiness is declared as readiness-only.

Acceptance result:
PHASE 2 is accepted only when all batch files 2.1 through 2.10 are present, target smoke tests pass, readiness map reports 2.10 READY, and the full-platform auto pytest run passes before commit/push.


JARVIS context document:
- `docs/architecture/network_security/phase_2_network_security_jarvis_context_v1.md`

This context document is explanatory only. It helps future JARVIS/operator reasoning, maintenance and optimization.
It is not a blocking policy gate and does not prevent future platform development.
