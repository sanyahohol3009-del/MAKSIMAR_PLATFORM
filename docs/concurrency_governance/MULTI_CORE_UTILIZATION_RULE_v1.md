# MULTI CORE UTILIZATION RULE v1

Status: active canonical multi-core utilization rule
Scope: CPU-bound and mixed workloads
Rule: the platform must scale across available CPU resources without hardcoding for a single machine size

---

## 1. Purpose

This document defines how the platform should think about CPU scaling.

It exists to prevent:
- one-core bias
- fixed thread assumptions
- architecture tied to weak hardware only
- architecture tied to one premium workstation only

---

## 2. Hardware-Scale Neutral Principle

The platform must remain valid across:

- low-power nodes
- developer desktops
- high-core servers
- workstation-class CPUs
- 64/96/128/256+ core systems

The platform must not hardcode:
- fixed core counts
- fixed worker counts
- fixed process counts
- fixed thread counts

---

## 3. Required Model

CPU utilization must be driven by:
- node capability profile
- workload class
- concurrency budget
- pressure state
- policy constraints
- thermal / degraded state if exposed

---

## 4. Required Behavior

The platform must support:
- conservative mode on weak hardware
- moderate parallelism on general desktops
- high parallelism on workstation/server hardware
- policy-limited scaling on very large machines

---

## 5. What Is Forbidden

The following remain forbidden:
- assuming “8 threads forever”
- assuming “all cores always”
- hardcoding worker counts into core contracts
- oversubscription by default
- treating hardware abundance as permission to ignore policy

---

## 6. Final Rule

The system must scale with hardware capability,
but hardware capability never overrides governance, policy, or safety.

---

## 7. Status

This document is the active canonical multi-core utilization rule until replaced by a stricter hardware scheduling standard.
