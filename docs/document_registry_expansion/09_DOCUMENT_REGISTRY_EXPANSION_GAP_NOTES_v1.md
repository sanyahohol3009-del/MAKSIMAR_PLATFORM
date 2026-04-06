# 09 DOCUMENT REGISTRY EXPANSION GAP NOTES v1

Status: active_canonical
Document Type: audit_closure
Authority Level: reference
Interpretation Priority: medium
Scope: limitations of the current document-registry-expansion pass
Rule: the registry-expansion pass must remain explicit about what is still incomplete beyond the current baseline

---

## 1. Purpose

This document records the current limitations of the document-registry-expansion pass.

It exists to keep the pass honest and bounded.

---

## 2. Current Gap Notes

### Gap 1
The current pass establishes registry-expansion rules, not yet full registry coverage.

### Gap 2
Most older documentation families are still not represented in `document_registry.yaml`.

### Gap 3
Dependency and used_by metadata are still lightweight and not yet a hardened graph.

### Gap 4
Future deeper work is still needed for:
- wider package coverage
- retroactive normalization
- stronger dependency mapping
- supersession tracking
- package manifests
- code/test/runbook linkage expansion

---

## 3. Final Rule

A registry-expansion baseline may start before full coverage if the remaining gaps are explicit.

---

## 4. Status

This document is the active canonical document-registry-expansion gap note set until replaced by a stricter registry audit.
