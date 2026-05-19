# UPDATE_RECOVERY BATCH 3.2 Roadmap Reconciliation v1

## Batch

BATCH 3.2 — Update Package + Signature Gate

## Required files from printed roadmap

- update_package_models.py
- update_signature_verifier_contract.py
- signed_update_service_contract.py
- update_recovery_policy.py

Canonical paths:

- MAKSIMAR_CORE_LIB/update_recovery/update_package_models.py
- MAKSIMAR_CORE_LIB/update_recovery/update_signature_verifier_contract.py
- MAKSIMAR_CORE_LIB/update_recovery/signed_update_service_contract.py
- MAKSIMAR_CORE_LIB/update_recovery/update_recovery_policy.py

## Required tests from printed roadmap

- tests/update_recovery/test_update_package_models_smoke.py
- tests/update_recovery/test_update_signature_verifier_contract_smoke.py
- tests/update_recovery/test_signed_update_service_contract_smoke.py
- tests/update_recovery/test_update_recovery_policy_smoke.py

## Dashboard / read model

- UpdateSignatureDecisionReadModel

## Critical correction

Do not create:

- MAKSIMAR_CORE_LIB/update_recovery/signature_verifier_contract.py

Reason:

- general signature decision remains in SECURITY_LAYER;
- update-specific verifier is separate;
- update-specific verifier must live in update_signature_verifier_contract.py.

## Implementation mode

- CREATE ONLY.
- No move.
- No delete.
- No migration.
- No replacement of SECURITY_LAYER signature verifier.
- No direct runtime update apply.
- No unsigned update acceptance.
- No dashboard execution.
