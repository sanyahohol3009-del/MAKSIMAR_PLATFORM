# Repository Scan Models Semantic Duplicate Review v1

Status: PHASE 0 / Batch 0.2 pre-implementation semantic review.

## Purpose

Batch 0.2 must not create a second scanner, second vendor gate, second runtime risk engine or duplicate external backend scanner.

This review records the existing semantic candidates found before implementing repository scan models.

## Existing canonical scanner / vendor gate

Existing canonical scanner surface:

- `tools/vendor_security_gate.py`

Relevant existing semantics:

- `VendorGateReport`
- optional scanners: bandit, pip-audit, clamscan, detect-secrets, semgrep, gitleaks, trufflehog, osv-scanner, syft, grype
- `build_vendor_gate_report(...)`

## Existing server adapter

Existing server adapter:

- `MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_vendor_gate_adapter.py`

Relevant existing semantics:

- `VendorGateSecuritySignal`
- `VendorGateAdapterDecision`
- `evaluate_vendor_gate_signal(...)`

## Existing runtime security gate

Existing runtime gate:

- `MAKSIMAR_SERVER/SECURITY_LAYER/security_gate.py`

Relevant existing semantics:

- `SecurityRuntimeGateEvaluation`
- existing runtime security gate consumes `VendorGateAdapterDecision`
- runtime gate must not execute scanner logic

## Existing quarantine pattern

Existing quarantine pattern:

- `MAKSIMAR_CORE_LIB/security_layer/media_quarantine_contract.py`

Relevant existing semantics:

- immutable dataclass contract
- explicit status enum
- no runtime mutation
- no canonical write

## Existing risk summary pattern

Existing risk summary pattern:

- `MAKSIMAR_CORE_LIB/oob_dashboard/risk_summary_models.py`
- `MAKSIMAR_CORE_LIB/oob_dashboard/risk_summary_contract.py`

This is dashboard/operator risk summary, not repository scan model. Batch 0.2 must not duplicate dashboard risk summary, but can follow the same invariant discipline.

## External non-canonical scanner

External backend scanner candidates:

- `EXTERNAL_BACKENDS/mempalace/source/mempalace/project_scanner.py`
- `EXTERNAL_BACKENDS/mempalace/source/mempalace/convo_scanner.py`

Decision:

- do not import external backend scanner into core
- do not copy external scanner logic
- treat external backend reports as evidence/source artifacts only
- canonical MAKSIMAR model remains in `MAKSIMAR_CORE_LIB/security_layer`

## Batch 0.2 decision

Decision: CREATE canonical repository scan contract models, but BIND semantically to existing vendor gate.

Batch 0.2 creates:

- `MAKSIMAR_CORE_LIB/security_layer/repository_scan_models.py`
- `MAKSIMAR_CORE_LIB/security_layer/repository_risk_summary_builder.py`
- `MAKSIMAR_CORE_LIB/security_layer/repository_quarantine_policy.py`

Batch 0.2 does not create:

- scanner runtime
- subprocess execution
- network access
- new vendor gate
- second runtime security gate
- direct MemPalace dependency
- dashboard mutation
- canonical write

## Required invariants

All repository scan models must be:

- immutable dataclasses
- validated in `__post_init__`
- deterministic
- read-only
- evidence-bound
- compatible with existing vendor gate semantics
- safe for dashboard/read-model use
