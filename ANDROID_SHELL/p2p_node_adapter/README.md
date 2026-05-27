# Android P2P Node Adapter — Phase 2 / Batch 2.8

This directory is an Android shell-side P2P node adapter surface.

It is not a real Android P2P runtime.
It does not perform peer discovery.
It does not open sockets.
It does not open ports.
It does not call Android system network APIs.
It does not create tunnels.
It does not execute floating-master election.
It does not mutate runtime state.

Source/projection layer:

- `shared_mobile_core/p2p_mesh_network/*`

Canonical policy remains in:

- `MAKSIMAR_CORE_LIB/network_security/*`

Server/dashboard observer remains in:

- `MAKSIMAR_SERVER/NETWORK_SECURITY_RUNTIME/p2p_mesh_observer_read_model_builder.py`
