# NETWORK_CONTAINERIZATION Blueprint v1

## Scope

NETWORK_CONTAINERIZATION defines read-only network segmentation, container deployment blueprint, deployment gates, model contracts and preview visibility.

## Source surfaces

- NETWORK_SEGMENTATION/
- CONTAINER_DEPLOYMENT/
- MAKSIMAR_CORE_LIB/network_containerization/
- DATA_PLANE/container_contract.yaml
- UPDATE_RECOVERY/container_contract.yaml
- MAKSIMAR_CORE/contracts/vpn/

## Preview surfaces

- tools/monitor/runtime_input/network_containerization_terminal_preview.py
- tools/monitor/runtime_input/network_containerization_web_preview.py

## Read model

- NetworkContainerizationPreviewReadModel

## Required visibility

The preview must show:

- blocked deployment edges;
- missing contract paths;
- public exposure state;
- runtime network mutation state;
- X-Ray layer id;
- drift guard requirement.

## Hard boundaries

- No production deployment.
- No active Docker deployment.
- No active Compose deployment.
- No public exposure.
- No runtime network mutation.
- No dashboard execution.
- No canonical write.
