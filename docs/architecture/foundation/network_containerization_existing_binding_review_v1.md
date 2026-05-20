# NETWORK_CONTAINERIZATION Existing Binding Review v1

## Purpose

This review records existing surfaces that NETWORK_CONTAINERIZATION must reference without replacing.

## Existing bindings

- NETWORK_SEGMENTATION/network_segments.yaml
- NETWORK_SEGMENTATION/container_network_rules.yaml
- NETWORK_SEGMENTATION/boundaries/container_adapter_boundary.yaml
- CONTAINER_DEPLOYMENT/container_deployment_blueprint.yaml
- CONTAINER_DEPLOYMENT/container_contract.schema.yaml
- CONTAINER_DEPLOYMENT/deployment_gates/security_required_gate.yaml
- CONTAINER_DEPLOYMENT/no_production_deploy_until_foundation_green.yaml
- DATA_PLANE/container_contract.yaml
- UPDATE_RECOVERY/container_contract.yaml
- MAKSIMAR_CORE/contracts/vpn/
- MAKSIMAR_CORE_LIB/network_containerization/network_trust_boundary_binding_models.py

## Binding rule

NETWORK_CONTAINERIZATION preview reads and reports these surfaces.

It does not move, delete, migrate, override or activate them.

## Review result

The preview layer is accepted as a read-only visibility layer for blocked deployment edges and missing contracts.
