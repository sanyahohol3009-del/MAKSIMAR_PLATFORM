# UPDATE_RECOVERY Container Boundary v1

## Boundary type

UPDATE_RECOVERY is container-ready as a wrapper/facade boundary.

The boundary is not a replacement of existing secure update or recovery manager sources.

## Allowed

- wrapper services;
- read models;
- dashboard-safe previews;
- adapters for existing foundations;
- E2E tracer for unsigned update rejection;
- health/readiness outputs.

## Forbidden

- direct update apply;
- direct canonical write;
- dashboard execution;
- replacing secure_sync_update_transport;
- moving RUNTIME/recovery_manager.py;
- deleting existing recovery sources;
- migration without explicit correction pass.

## Container extraction rule

If UPDATE_RECOVERY is extracted as a service/container under an approved containerization batch, it must keep stable adapters around existing source surfaces.

The container may expose read-only readiness, preview and health outputs.

The container must not become the source of truth for canonical update execution.

## Network note

Network segmentation and trust boundaries are separate engineering layers.

UPDATE_RECOVERY container boundary does not define public exposure, ports, firewall policy or network segmentation. Those belong to NETWORK_CONTAINERIZATION / security boundary work.
