# 06 PACKAGE USED BY DECLARATION BASELINE v1

Status: active_canonical
Document Type: canonical
Authority Level: operational
Interpretation Priority: high
Scope: baseline rules for package-level downstream usage declaration in manifests
Rule: package downstream usage should remain explicit so the documentation system can be read as a living dependency surface rather than static storage

---

## 1. Purpose

This document defines the package-used-by-declaration baseline of the platform.

It exists to preserve:
- readable downstream meaning
- lower ambiguity about future package reliance
- gradual graph expansion in both directions
- a stable base for future self-reading and planning behavior

---

## 2. Downstream Principle

Package used_by declaration should remain understandable in terms of:
- what future package or layer may rely on the current one
- what interpretive downstream relevance exists
- how the package participates in broader documentation structure
- what future implementation or governance surfaces may depend on it

---

## 3. Required Rule

Package used_by declaration should remain:
- explicit
- selective
- future-aware
- non-bloated
- meaningful

---

## 4. What Is Forbidden

The following remain forbidden:
- package meaning treated as purely local
- downstream usage recorded only in chat memory
- decorative future references with no interpretive value
- giant speculative used_by lists that reduce readability

---

## 5. Final Rule

A mature documentation system records not only where a package came from, but where its meaning is expected to travel next.

---

## 6. Status

This document is the active canonical package-used-by-declaration baseline until replaced by a stricter downstream package reference.
