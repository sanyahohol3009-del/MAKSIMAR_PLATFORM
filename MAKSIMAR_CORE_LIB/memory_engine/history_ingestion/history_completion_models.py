from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryCompletionState:
    full_history_import_ready: bool
    project_history_graph_ready: bool
    project_history_panel_ready: bool
    project_history_filter_ready: bool
    project_history_readable_by_jarvis: bool
    incremental_reimport_safe: bool
    completion_ready: bool

    def __post_init__(self) -> None:
        if not self.full_history_import_ready:
            raise ValueError("full_history_import_ready must be True")
        if not self.project_history_graph_ready:
            raise ValueError("project_history_graph_ready must be True")
        if not self.project_history_panel_ready:
            raise ValueError("project_history_panel_ready must be True")
        if not self.project_history_filter_ready:
            raise ValueError("project_history_filter_ready must be True")
        if not self.project_history_readable_by_jarvis:
            raise ValueError("project_history_readable_by_jarvis must be True")
        if not self.incremental_reimport_safe:
            raise ValueError("incremental_reimport_safe must be True")
        if not self.completion_ready:
            raise ValueError("completion_ready must be True")
