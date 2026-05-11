# PHASE 5.1 Batch 3 — MemPalace Vendor Acquisition Sandbox Acceptance v1

## Статус

PHASE 5.1 Batch 3 принят.

## Purpose

MemPalace acquired only inside isolated vendor sandbox.

## Accepted state

Vendor source:

- official_source_verified: True
- official_remote_verified: True
- commit_seen_in_remote_refs: True
- version_or_commit_pinned: True
- non_empty_project: True
- external_code_not_committed: True
- separate_venv: True
- sandbox_data_only: True

Security / integrity:

- required_files_present: README.md, pyproject.toml
- tracked_file_count: 291
- python_file_count: 141
- archive_sha256: present
- bandit_report: present
- pip_audit_report: present
- pip-audit: no known vulnerabilities found
- clamscan_report: present, skipped if clamscan not installed
- risky_static_findings_count: 98
- manual_security_review_required: True

Runtime / memory boundary:

- canonical_memory_access: False
- runtime_mutation_allowed: False
- external_code_not_committed: True
- EXTERNAL_BACKENDS excluded from general pytest collection
- vendor source validated only through explicit vendor acquisition smoke/security tests

## Жёсткие правила

MemPalace source and venv are not committed.

MemPalace external tests are not part of MAKSIMAR full pytest collection.

MemPalace remains sandbox-only.

MemPalace is not connected to routing/runtime yet.

MemPalace real backend is not enabled.

MemPalace cannot access canonical memory.

MemPalace cannot mutate runtime.

Risky static findings require manual review before any runtime enablement.

## Проверки

- local vendor tests: 6 passed
- related pack: 156 passed
- full auto parallel with monitor active: 2032 passed
