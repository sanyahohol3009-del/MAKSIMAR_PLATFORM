# Root Artifact Hygiene Archival Policy v1

## Status

Canonical policy document for PHASE 0 / BATCH 0.4.

## Layer

`ROOT_ARTIFACT_HYGIENE`

## Purpose

This policy defines how root-level artifacts, generated reports, backups, audit bundles, vendor outputs, and temporary files are classified for future archival review.

The policy is read-only. It does not move, delete, rewrite, normalize, or auto-fix any file.

## Non-negotiable rules

1. No automatic deletion.
2. No automatic move.
3. No runtime mutation.
4. No canonical write.
5. No dashboard mutation.
6. No archive action without explicit correction/archive pass.
7. No source relocation without separate migration approval.
8. No vendor source movement from `EXTERNAL_BACKENDS` through this layer.
9. No hidden cleanup during tests.
10. No path traversal and no absolute project-external path handling.

## Allowed actions

| Action | Meaning | Mutation |
|---|---|---|
| `use_in_place` | Artifact is in an acceptable location. | No |
| `review_only` | Artifact must be shown to operator for review. | No |
| `archive_later_with_approval` | Candidate for later archive pass. | No |
| `migration_pass_required` | Candidate needs explicit migration/correction pass. | No |
| `ignore_generated` | Generated/runtime artifact should not be committed as source. | No |
| `keep_vendor_sandboxed` | External vendor artifact must remain sandboxed. | No |

## Forbidden actions

| Forbidden action | Reason |
|---|---|
| auto-delete | Too risky; can destroy project evidence or working state. |
| auto-move | Can cause import drift and test discovery drift. |
| auto-fix | Can hide architectural drift. |
| dashboard cleanup button | Dashboard is read-only. |
| runtime cleanup mutation | Runtime is not canonical file organizer. |

## Artifact classes

| Class | Meaning |
|---|---|
| `source_candidate` | Possible source/config/test/doc project artifact. |
| `generated_candidate` | Generated runtime, cache, report, or build-like artifact. |
| `backup_candidate` | Backup file such as `.bak*`. |
| `audit_candidate` | Audit, pytest, coverage, history, or report artifact. |
| `vendor_candidate` | External backend/vendor output. |
| `unknown_candidate` | Unknown root surface requiring manual review. |

## Archive destinations

| Candidate kind | Expected archive destination |
|---|---|
| audit reports | `docs/archive/audits` or `docs/archive/reports` |
| history track files | `docs/archive/history_track` |
| backups | `docs/archive/backups` |
| generated runtime files | not archived automatically |
| external vendor reports | remain under vendor security gate unless separately approved |

## Dashboard fields

Dashboard-safe read models may expose:

- total item count
- source count
- generated count
- backup count
- audit/report count
- vendor count
- unknown count
- archive candidate count
- correction required count
- approval required count
- delete allowed
- move allowed
- scan read-only
- next action

Dashboard must not expose mutation controls.

## Batch Done criteria

PHASE 0 / BATCH 0.4 is acceptable only when:

1. Preview tools exist.
2. Policy documents exist.
3. Preview tools are read-only.
4. Preview tools provide machine-readable JSON output.
5. Preview tools provide terminal human output.
6. Roadmap CI for BATCH 0.4 passes with `--require-files`.
7. Architecture Guard passes.
8. X-Ray reports zero AST parse errors.
9. Full auto pytest passes with `./.venv/bin/python -m pytest -q -n auto`.
