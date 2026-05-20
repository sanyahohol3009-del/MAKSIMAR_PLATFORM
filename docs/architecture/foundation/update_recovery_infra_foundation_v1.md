# UPDATE_RECOVERY_INFRA Foundation v1

## Scope

UPDATE_RECOVERY_INFRA Foundation v1 defines the foundation layer for safe update and recovery handling.

The phase covers:

- update/recovery surface and existing source binding;
- update package and update-specific signature verification;
- snapshot, rollback and recovery readiness contracts;
- offline import gate;
- runtime wrapper services and dashboard-safe previews;
- E2E tracer proving unsigned update rejection.

## Foundation acceptance

BATCH 3.5 closes the foundation through an E2E tracer with these required facts:

- unsigned update is rejected;
- no update apply is performed;
- secure_sync_update_transport is preserved;
- runtime_recovery_manager remains wrapped;
- manifest is present;
- source-of-truth check is required;
- version-control check is required;
- Drift Guard is required;
- X-Ray non-regression is required;
- full pytest is required.

## Safety boundaries

UPDATE_RECOVERY_INFRA does not directly mutate canonical truth.

UPDATE_RECOVERY_INFRA does not execute dashboard actions.

UPDATE_RECOVERY_INFRA does not replace secure_sync_update_transport.

UPDATE_RECOVERY_INFRA does not move or replace RUNTIME/recovery_manager.py.

Runtime services created in BATCH 3.4 are wrapper/read-model surfaces only. They expose dashboard-safe status and readiness outputs, but they do not apply updates.

## Dashboard output

The foundation exposes dashboard-safe read models:

- UpdateSignatureDecisionReadModel
- UpdateRecoveryReadinessReadModel
- SecureSyncUpdateFacadeReadModel
- UpdateRecoveryRuntimeReadModel
- UpdateTracerResultReadModel

Dashboard consumers may read these models. They must not execute updates, mutate canonical state, or bypass control-plane/security gates.

## Closure rule

Foundation v1 is considered closed only when:

- BATCH 3.5 required files exist;
- E2E tracer proves unsigned update rejection;
- no apply is performed;
- existing transport and recovery manager remain preserved;
- Roadmap CI passes with required files;
- Architecture Drift Guard passes;
- X-Ray non-regression passes;
- full pytest passes.
