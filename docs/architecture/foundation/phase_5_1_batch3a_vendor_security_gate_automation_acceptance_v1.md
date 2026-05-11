# PHASE 5.1 Batch 3A — Vendor Security Gate Automation Acceptance v1

## Статус

PHASE 5.1 Batch 3A принят.

## Purpose

Batch 3A replaces one-off vendor security Bash blocks with a reusable versioned project tool.

## Tool

- tools/vendor_security_gate.py

## Accepted state

Vendor gate tool:

- reusable for external backend / adapter / cube validation
- verifies official remote
- verifies pinned commit or version lock
- captures tree sha
- captures archive sha256
- checks non-empty project
- checks required files
- checks external source / venv / sandbox_data are not committed
- scans risky Python AST patterns
- scans forbidden CORE_ROOT / RUNTIME / SUPERVISOR / EXECUTION_CONTROL coupling
- runs optional scanner integrations when available

MemPalace validation:

- vendor_name: MemPalace
- official_remote_verified: True
- commit_seen_in_remote_refs: True through remote ref or version lock fallback
- commit_matches_version_lock: True
- non_empty_project: True
- external_code_not_committed: True
- canonical_memory_access: False
- runtime_mutation_allowed: False
- hard_gate_passed: True
- manual_security_review_required: True

## Optional scanner model

The tool detects and records scanner status for:

- bandit
- pip-audit
- clamscan
- detect-secrets
- semgrep
- gitleaks
- trufflehog
- osv-scanner
- syft
- grype

Unavailable scanners are reported as skipped and require manual review where relevant.

## Hard blockers

- official_remote_verified=False
- commit_seen_in_remote_refs=False
- non_empty_project=False
- external_code_not_committed=False
- canonical_memory_access=True
- runtime_mutation_allowed=True
- forbidden MAKSIMAR core/runtime coupling

## Manual review triggers

- risky static findings
- skipped optional scanners
- scanner non-zero return
- possible secrets
- dependency vulnerabilities
- malware scanner unavailable

## Жёсткие правила

Vendor source remains untrusted until hard gate passes.

Manual review required does not automatically fail the hard gate.

Manual review required prevents real backend enablement.

Vendor source / venv / sandbox_data are never committed.

Vendor code is validated only through explicit vendor smoke/security tests.

After Batch 3A, future external downloads must use tools/vendor_security_gate.py instead of manual one-off Bash blocks.

## Проверки

- local tests: 3 passed
- related pack: 159 passed
- full auto parallel with monitor active: 2035 passed
