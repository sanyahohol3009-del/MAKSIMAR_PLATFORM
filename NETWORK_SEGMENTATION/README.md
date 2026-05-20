# NETWORK_SEGMENTATION

## Purpose

NETWORK_SEGMENTATION is the blueprint/read-model surface for network segmentation and container network rules.

It is not the source of truth for trust-boundary authority.

Canonical trust-boundary authority remains in:

- MAKSIMAR_CORE_LIB/network_trust_boundaries/network_trust_boundaries_contract.py
- docs/security_governance/TRUST_BOUNDARIES_v1.md

## BATCH 4.1 mode

BATCH 4.1 is blueprint/read-model only.

Allowed:

- define network segment names;
- define container network rule intent;
- bind to existing network_trust_boundaries;
- expose dashboard-safe read models;
- document no public exposure by default.

Forbidden:

- production deployment;
- public exposure;
- runtime network mutation;
- replacing network_trust_boundaries;
- moving network_trust_boundaries;
- deleting network_trust_boundaries;
- migrating network_trust_boundaries;
- Docker/Compose activation.

## X-Ray markers

This surface declares the following blueprint markers:

- net_core_safety
- net_control
- net_security
- net_governance
- net_data
- net_ai
- net_products
- net_observability
- net_update
- healthcheck
- restart_policy
- no_public_exposure
