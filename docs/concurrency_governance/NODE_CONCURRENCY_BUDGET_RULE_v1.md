# NODE CONCURRENCY BUDGET RULE v1

Status: active canonical node concurrency budget rule
Scope: per-node resource scheduling
Rule: every node must have a bounded concurrency budget derived from capabilities, policy, and pressure state

---

## 1. Purpose

This document defines the canonical concurrency budget rule per node.

It exists to prevent:
- one-size-fits-all execution assumptions
- weak nodes being overloaded
- strong nodes being underused by architecture
- uncontrolled scaling without policy

---

## 2. Budget Principle

Each node must have a concurrency budget based on:
- CPU capability
- RAM capability
- GPU capability if relevant
- node role
- workload class permissions
- pressure state
- policy restrictions

---

## 3. Required Behavior

The system must support:
- low budget on weak hardware
- higher budget on strong hardware
- dynamic lowering under pressure
- policy-based caps even on powerful systems

---

## 4. Hardware Neutrality

This rule must remain valid from:
- small mobile/device nodes
- modest desktops
- single workstation nodes
- high-core servers
- cluster-like future nodes

---

## 5. What Is Forbidden

The following remain forbidden:
- one global worker count for all nodes
- assuming one node class
- CPU-only budgeting where memory is the real bottleneck
- ignoring pressure state

---

## 6. Final Rule

Node capability defines possible parallelism.
Policy and pressure define allowed parallelism.

---

## 7. Status

This document is the active canonical node concurrency budget rule until replaced by a stricter scheduler standard.
