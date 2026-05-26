# Existing Scanner Discovery v1

Status: PHASE 0 / Batch 0.1 acceptance document.

## Purpose

This document records the scanner/vendor-gate discovery result for Roadmap v4.2 + v4.2.1.

The purpose of this batch is not to create a second scanner. The purpose is to discover the existing scanner/security/vendor-gate surfaces and bind future repository scanning work to the existing canonical scanner path.

## Decision

Decision: EXTEND existing scanner/vendor gate.

No duplicate scanner root is allowed.

## Existing canonical scanner surface

The existing canonical scanner surface is:

- `tools/vendor_security_gate.py`

## Existing vendor/security tests

Existing vendor security tests:

- `tests/vendor_security_gate/test_vendor_security_gate_tool_smoke.py`
- `tests/vendor_security_gate/test_vendor_security_gate_report_shape_smoke.py`
- `tests/vendor_security_gate/test_vendor_security_gate_mempalace_smoke.py`

## Existing server security adapter

Existing server-side adapter surface:

- `MAKSIMAR_SERVER/SECURITY_LAYER/adapters/security_vendor_gate_adapter.py`

## Existing security layer surfaces

Existing security runtime / contract surfaces include:

- `MAKSIMAR_CORE_LIB/security_layer/`
- `MAKSIMAR_SERVER/SECURITY_LAYER/`
- `docs/security_governance/`
- `EXTERNAL_BACKENDS/mempalace/security_reports/`

## Required rule

Future repository scanner work must extend the existing vendor/security gate and must not create a parallel scanner root.

Allowed:

- discovery wrapper
- read-only scanner inventory
- adapter binding to existing vendor gate
- risk summary model connected to existing security layer

Forbidden:

- creating a second independent scanner engine
- duplicating vendor gate semantics
- moving or deleting existing scanner/security files
- importing external open-source repositories directly into immutable core
- treating external backend reports as canonical MAKSIMAR truth

## Batch 0.1 target files

Production / documentation files:

- `docs/architecture/open_source_integration/existing_scanner_discovery_v1.md`
- `tools/project_readiness_control/scanner_discovery.py`

Tests:

- `tests/vendor_security_gate/test_existing_repo_scanner_discovery_smoke.py`
- `tests/vendor_security_gate/test_existing_scanner_extend_not_duplicate_smoke.py`

## Acceptance

Batch 0.1 is accepted when:

1. The discovery tool reports the existing canonical scanner surface.
2. The discovery tool reports the existing vendor security tests.
3. The discovery tool reports the existing server security adapter.
4. The discovery decision is `EXTEND_EXISTING`.
5. Tests prove that no duplicate scanner root is required.
