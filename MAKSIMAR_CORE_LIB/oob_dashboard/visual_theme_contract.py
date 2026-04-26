from __future__ import annotations

from dataclasses import dataclass


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualThemeContract:
    theme_id: str
    theme_family: str
    glow_enabled: bool
    depth_enabled: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.theme_id, "theme_id")
        _require_non_empty(self.theme_family, "theme_family")
        _require_non_empty(self.description, "description")

        if not self.glow_enabled:
            raise ValueError(
                "glow_enabled must remain true for canonical visual theme contract."
            )
        if not self.depth_enabled:
            raise ValueError(
                "depth_enabled must remain true for canonical visual theme contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual theme contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual theme contract."
            )


def build_visual_theme_contract() -> VisualThemeContract:
    return VisualThemeContract(
        theme_id="visual_theme_operator_hud_001",
        theme_family="operator_hud_theme",
        glow_enabled=True,
        depth_enabled=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual HUD theme contract.",
    )
