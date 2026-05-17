# Root Artifact Hygiene Location Matrix v1

## Status

Canonical location matrix for PHASE 0 / BATCH 0.4.

## Purpose

This matrix defines how root artifact hygiene classifies observed project paths and how those classifications are exposed to previews and future dashboard read-only panels.

This is not a migration plan. It is a read-only classification matrix.

## Matrix

| Observed artifact | Classification | Expected location | Status | Action |
|---|---|---|---|---|
| `README.md` | `source_candidate` | project root | `correct_location` | `use_in_place` |
| `pytest.ini` | `source_candidate` | project root | `correct_location` | `use_in_place` |
| `MAKSIMAR_CORE_LIB/**` | `source_candidate` | canonical core-lib layer | `correct_location` | `use_in_place` |
| `MAKSIMAR_SERVER/**` | `source_candidate` | server layer | `correct_location` | `use_in_place` |
| `CORE_ROOT/**` | `source_candidate` | immutable core layer | `correct_location` | `use_in_place` |
| `CONTROL_PLANE/**` | `source_candidate` | control-plane layer | `correct_location` | `use_in_place` |
| `RUNTIME/state/**` | `generated_candidate` or runtime state | runtime state area | `temporary_generated` | `ignore_generated` |
| `.pytest_cache/**` | `generated_candidate` | generated cache | `temporary_generated` | `ignore_generated` |
| `project_audit/**` | `generated_candidate` | generated audit area | `temporary_generated` | `ignore_generated` |
| `*.bak*` | `backup_candidate` | `docs/archive/backups` later | `backup` | `archive_later_with_approval` |
| `audit_*.txt` | `audit_candidate` | `docs/archive/audits` later | `audit_report` | `archive_later_with_approval` |
| `full_*_report.txt` | `audit_candidate` | `docs/archive/reports` later | `audit_report` | `archive_later_with_approval` |
| `history_track_*` | `audit_candidate` | `docs/archive/history_track` later | `audit_report` | `archive_later_with_approval` |
| `EXTERNAL_BACKENDS/**` | `vendor_candidate` | `EXTERNAL_BACKENDS` | `external_vendor` | `keep_vendor_sandboxed` |
| unknown root file | `unknown_candidate` | manual review | `candidate_for_correction_pass` | `migration_pass_required` |

## Correction-pass requirement

Any path marked as:

- `wrong_location`
- `legacy_location`
- `candidate_for_correction_pass`
- `backup`
- `audit_report`

must not be moved during normal development.

It may only be changed through a separate correction/archive/migration pass.

## Dashboard-safe interpretation

Future dashboard panels may display:

- location status
- expected location
- allowed action
- risk level
- approval required
- reason codes

Future dashboard panels must not execute:

- move
- delete
- archive
- cleanup
- git stage
- git commit

## Source of truth

The source of truth for classification logic is:

- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/root_surface_inventory_models.py`
- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/artifact_classification_models.py`
- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/artifact_location_policy.py`
- `MAKSIMAR_CORE_LIB/root_artifact_hygiene/root_artifact_report_builder.py`

This document describes the policy. The Python contracts enforce the machine-readable form.
