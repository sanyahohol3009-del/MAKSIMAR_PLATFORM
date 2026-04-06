# 08 VALIDATION COMMAND REFERENCE BASELINE v1

Status: active canonical validation-command-reference baseline
Scope: current canonical command reference for full-suite validation
Rule: important validation commands must remain written down so whole-suite operation does not depend on memory

---

## 1. Purpose

This document defines the current validation-command-reference baseline of the platform.

It exists to preserve:
- readable full-suite command references
- operator continuity
- reduced restart cost after context loss
- a stable base for later automation and Makefile/CI linkage

---

## 2. Current Command Reference

Confirmed current commands include:

### Environment checks
- `which python`
- `which pytest`
- `python -c "import sys, os; print(os.getcwd()); print(sys.executable); print(sys.path[:10])"`

### Import checks
- `python -c "import MAKSIMAR_CORE_LIB; print('MAKSIMAR_CORE_LIB OK')"`
- `python -c "import MAKSIMAR_SERVER; print('MAKSIMAR_SERVER OK')"`
- `python -c "import tools; print('tools OK')"`

### Whole-suite validation
- `python -m pytest -q`
- `PYTHONPATH="$PWD" pytest -q`
- `PYTHONPATH="$PWD" pytest -q -n auto`

---

## 3. Required Rule

This command reference should remain:
- explicit
- current
- operationally useful
- tied to confirmed behavior
- replaceable only by stricter references later

---

## 4. Final Rule

A serious platform writes down the commands it actually trusts.

---

## 5. Status

This document is the active canonical validation-command-reference baseline until replaced by a stricter operations reference.
