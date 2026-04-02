# VISUAL CANONICAL SOURCE OF TRUTH v1

Status: active  
Scope: canonical truth ownership for the visual layer  
Rule: premium visual work may only polish the canonical visual chain, not alternate or legacy visual representations

---

## 1. Purpose

This document defines which visual contracts and artifacts are canonical for the current HUD/visual track.

It exists to prevent polishing the wrong layer.

---

## 2. Canonical Visual Contracts

The following are the canonical visual contracts for the current visual HUD chain:

- `visual_render_surface_contract`
- `visual_renderer_contract`
- `visual_theme_contract`
- `panel_to_visual_mapping_contract`
- `visual_signal_overlay_contract`
- `visual_topology_overlay_contract`
- `visual_explainability_sidebar_contract`
- `visual_status_bar_contract`
- `visual_bottom_ticker_contract`
- `visual_hud_composition_contract`
- `visual_hud_snapshot_contract`
- `visual_hud_preview_contract`
- `visual_hud_screen_contract`
- `visual_hud_render_result_contract`
- `visual_hud_preview_artifact_contract`
- `visual_hud_preview_state_contract`

---

## 3. Official Canonical Visual Artifacts / States

The following downstream states/artifacts are currently official for the visual track:

- HUD preview
- HUD screen
- HUD render result
- HUD preview artifact
- HUD preview state

These are the currently accepted downstream presentation-ready visual states.

---

## 4. Transitional / Legacy / Non-Canonical Visual Surfaces

The following are not to be treated as canonical polish targets unless explicitly promoted later:

- older diagnostic-only representations
- earlier/transitional read views that are not part of the canonical visual HUD chain
- legacy panel naming/style history
- non-promoted experimental visual representations
- any decorative/preview-only concept lacking canonical contract binding

---

## 5. Rule

Visual polish must target the canonical visual chain only.

It must not:
- silently polish alternate legacy views
- silently reinterpret older diagnostic layers as canonical HUD truth
- silently normalize historical panel ids/names as part of polish

---

## 6. Final Rule

The canonical visual source of truth is the current HUD chain through preview state.

Everything else is either downstream support, legacy context, or future work until explicitly promoted.
