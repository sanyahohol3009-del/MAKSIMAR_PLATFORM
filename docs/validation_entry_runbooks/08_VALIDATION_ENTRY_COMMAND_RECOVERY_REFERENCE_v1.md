# 08 VALIDATION ENTRY COMMAND RECOVERY REFERENCE v1

Status: active canonical validation-entry-command-recovery reference
Scope: trusted operator command references used during validation entry recovery
Rule: important recovery commands must remain written down so remediation does not depend on memory alone

---

## 1. Purpose

This document defines the validation-entry-command-recovery reference of the platform.

It exists to preserve:
- readable remediation commands
- operator continuity
- reduced restart cost after context loss
- a stable base for later wrapper and automation binding

---

## 2. Current Recovery Reference

Confirmed useful recovery commands include:

### Root and environment checks
- `pwd`
- `which python`
- `which pytest`
- `python -c "import sys, os; print(os.getcwd()); print(sys.executable); print(sys.path[:10])"`

### Import checks
- `python -c "import MAKSIMAR_CORE_LIB; print('MAKSIMAR_CORE_LIB OK')"`
- `python -c "import MAKSIMAR_SERVER; print('MAKSIMAR_SERVER OK')"`
- `python -c "import tools; print('tools OK')"`

### Trusted validation reruns
- `python -m pytest -q`
- `PYTHONPATH="$PWD" pytest -q`
- `PYTHONPATH="$PWD" pytest -q -n auto`

---

## 3. Required Rule

This command recovery reference should remain:
- explicit
- current
- operationally useful
- diagnostics-aligned
- replaceable only by stricter references later

---

## 4. Final Rule

A mature platform writes down the commands it trusts during recovery, not only during calm conditions.

---

## 5. Status

This document is the active canonical validation-entry-command-recovery reference until replaced by a stricter validation recovery operations reference.
