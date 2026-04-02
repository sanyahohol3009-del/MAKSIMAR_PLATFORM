# DOCUMENTATION FAMILIES MATRIX v1

Status: active canonical documentation families matrix
Scope: full-project documentation coverage
Rule: the project must maintain required documentation families across all major domains

---

## 1. Purpose

This document defines the required families of documentation across the project.

It exists to prevent:
- one-sided documentation
- architecture-only documentation with no runbooks
- code growth without operator guidance
- validation without written rules
- product and integration drift

---

## 2. Required Documentation Families

The project should maintain explicit documentation for:

### 2.1 Architecture
- architecture maps
- boundary rules
- contracts
- invariants
- layering principles

### 2.2 Security and Governance
- trust boundaries
- approval rules
- immutable core rules
- validation/governance rules
- compliance and threat-related material

### 2.3 Runtime and Operations
- lifecycle rules
- boot/shutdown behavior
- degraded modes
- process/service relationships
- recovery behavior

### 2.4 Observability and Diagnostics
- metrics meaning
- health models
- incident interpretation
- trace/diagnostic expectations
- truth-consistency logic

### 2.5 Testing and Validation
- test tiers
- full-platform validation rules
- CI/CD validation rules
- failure classification
- automated trigger logic

### 2.6 Visual and Dashboard
- panel semantics
- view vocabulary
- display split
- renderer/view rules
- operator dashboard logic

### 2.7 Mobile / Bridge / Accelerator
- app shell rules
- AI bridge contracts
- backend modes
- discovery/handshake
- thermal/power behavior
- accelerator product logic

### 2.8 AI / Memory / Self-Awareness
- memory model
- archive ingestion
- provenance/truth resolution
- self-awareness behavior
- documentation-aware reasoning rules

### 2.9 Agent / Swarm
- concurrency rules
- capability rules
- approval boundaries
- coordination logic
- evidence requirements

### 2.10 Runbooks and Operator Procedures
- how to run
- how to test
- how to recover
- how to inspect
- how to rollback

### 2.11 Release and Change
- release notes
- migration notes
- change summaries
- compatibility notes
- rollback notes

---

## 3. Coverage Principle

A mature platform requires all of these families over time.

The project must not assume that “architecture docs only” are enough.

---

## 4. Final Rule

If a domain is important enough to engineer, it is important enough to document in its own family.

---

## 5. Status

This document is the active canonical documentation families matrix until replaced by a stricter project documentation coverage standard.
