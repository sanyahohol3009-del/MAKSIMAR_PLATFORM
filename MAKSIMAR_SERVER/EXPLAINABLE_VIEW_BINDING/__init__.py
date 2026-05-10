from __future__ import annotations

from typing import Any

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_contract import (
    build_explainable_view_binding_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_models import (
    ExplainableViewBindingContract,
    ExplainableViewBindingEntry,
)

_LAZY_EXPORTS = {
    "build_explainable_phase_readiness": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_phase_readiness",
        "build_explainable_phase_readiness",
    ),
    "build_explainable_phase_preview": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_phase_readiness",
        "build_explainable_phase_preview",
    ),
    "ExplainablePhaseReadiness": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_phase_readiness",
        "ExplainablePhaseReadiness",
    ),
    "ExplainablePresentationBindingContract": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models",
        "ExplainablePresentationBindingContract",
    ),
    "ExplainablePresentationBindingEntry": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models",
        "ExplainablePresentationBindingEntry",
    ),
    "build_explainable_presentation_binding_contract": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models",
        "build_explainable_presentation_binding_contract",
    ),
    "build_explainable_presentation_summary": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_summary_builder",
        "build_explainable_presentation_summary",
    ),
    "build_explainable_presentation_preview": (
        "MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_preview_builder",
        "build_explainable_presentation_preview",
    ),
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attr_name = _LAZY_EXPORTS[name]

    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


__all__ = [
    "ExplainablePresentationBindingContract",
    "ExplainablePresentationBindingEntry",
    "ExplainableViewBindingContract",
    "ExplainableViewBindingEntry",
    "build_explainable_presentation_binding_contract",
    "build_explainable_presentation_preview",
    "build_explainable_presentation_summary",
    "build_explainable_view_binding_contract",
]
