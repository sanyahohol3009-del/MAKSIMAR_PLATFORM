# 07 TEST COLLECTION FAILURE INTERPRETATION v1

Status: active canonical test-collection-failure interpretation model
Scope: interpretation of pytest collection failures during repository validation
Rule: collection failures must remain interpretable so bootstrap and import issues are not misread as domain implementation collapse

---

## 1. Purpose

This document defines the test-collection-failure interpretation model of the platform.

It exists to preserve:
- correct diagnosis of collection-stage failures
- distinction between bootstrap breakage and test logic failure
- bounded interpretation of red output
- a stable base for later validation runbooks

---

## 2. Interpretation Principle

Collection failure should remain understandable in terms of:
- import visibility
- package discovery
- entrypoint choice
- environment activation
- whether test execution has actually begun

A collection-stage red result is not the same as failing executed assertions.

---

## 3. Current Confirmed Lesson

A large red collection event may arise from one shared bootstrap cause rather than hundreds of independent code defects.

That pattern has now been explicitly observed in this repository.

---

## 4. What Is Forbidden

The following remain forbidden:
- treating collection failure counts as proof of equal numbers of domain defects
- panicking at red output without stage interpretation
- ignoring bootstrap diagnosis
- skipping import-path verification

---

## 5. Final Rule

A mature platform interprets where validation failed before it decides why.

---

## 6. Status

This document is the active canonical test-collection-failure interpretation model until replaced by a stricter validation interpretation reference.
