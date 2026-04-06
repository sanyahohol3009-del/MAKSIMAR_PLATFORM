# 06 REGISTRY USED BY FIELD BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline semantics for the used_by field in the document registry
Rule: downstream usage metadata must remain explicit so important documents can be understood in terms of future operational relevance rather than static storage only

---

## 1. Purpose

This document defines the registry-used-by-field baseline of the platform.

It exists to preserve:
- readable downstream relevance
- lower ambiguity around future use surfaces
- better linkage between documents and future platform layers
- a stable base for self-reading and codegen-aware navigation

---

## 2. Used-By Principle

The used_by field should remain understandable in terms of:
- what future systems may rely on the package
- what implementation or governance surfaces consume it
- what later packages may build on it
- what operational relevance it has beyond archival storage

---

## 3. Required Rule

The used_by field should remain:
- explicit
- forward-looking
- lightweight
- meaningful
- compatible with future doc-to-code/test/runbook linkage

---

## 4. What Is Forbidden

The following remain forbidden:
- documents with no declared downstream meaning once that meaning is known
- used_by lists filled with vague hype instead of concrete relevance
- treating documentation as storage only rather than operational memory
- future-facing semantics preserved only in chat memory

---

## 5. Final Rule

A mature document registry records not only what a package depends on, but what may depend on it next.

---

## 6. Status

This document is the active canonical registry-used-by-field baseline until replaced by a stricter downstream-usage reference.
