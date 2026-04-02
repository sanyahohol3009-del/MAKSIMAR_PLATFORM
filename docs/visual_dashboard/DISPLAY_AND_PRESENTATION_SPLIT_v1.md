# DISPLAY AND PRESENTATION SPLIT v1

Status: active canonical display/presentation split
Scope: separation between what is shown and where/how it is shown
Rule: the platform must preserve a split between dashboard meaning and display placement so panels do not become display-authority blobs

---

## 1. Purpose

This document defines the current display and presentation split of the platform.

It exists to preserve clarity about:
- what the dashboard means
- what a panel means
- what display placement means
- why these should not collapse into one thing

---

## 2. Split Principle

The system should distinguish among:
- panel or view meaning
- presentation structure
- display placement or topology
- renderer or future visual realization

What is shown is not identical to where it is shown.

---

## 3. Required Rule

Panel semantics should remain downstream of system meaning.
Display logic should remain downstream of panel semantics.

A display decision must not silently become a truth or control decision.

---

## 4. What Is Forbidden

The following remain forbidden:
- panel identity determined only by display position
- display topology acting as system truth
- presentation logic silently becoming control logic
- collapsing view semantics into monitor placement

---

## 5. Final Rule

A mature dashboard system distinguishes semantic presentation from display placement.

---

## 6. Status

This document is the active canonical display/presentation split until replaced by a stricter display topology reference.
