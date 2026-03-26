from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


NodeRuntimeSplitEntryId = Literal[
    "noderuntimesplit_dev_001",
    "noderuntimesplit_home_001",
    "noderuntimesplit_mobile_001",
]

NodeId = Literal[
    "dev_001",
    "home_001",
    "mobile_001",
]

NodeType = Literal[
    "DEV_NODE",
    "HOME_NODE",
    "MOBILE_NODE",
]

StaticCapacityClass = Literal[
    "medium",
    "heavy",
    "light",
]

RuntimeState = Literal[
    "open",
    "throttled",
]

PressureLevel = Literal[
    "normal",
    "elevated",
]

SplitValidity = Literal[
    "split_valid",
]


_ENTRY_ID_PATTERN = re.compile(r"^noderuntimesplit_[a-z][a-z0-9_]*$")
_NODE_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{3}$")


@dataclass(frozen=True, slots=True)
class NodeRuntimeSplitEntry:
    """Canonical node runtime split entry.

    Static contract only.
    No live runtime discovery or hardware detection is allowed here.
    """

    entry_id: NodeRuntimeSplitEntryId
    node_id: NodeId
    node_type: NodeType
    static_capacity_class: StaticCapacityClass
    heavy_execution_allowed: bool
    runtime_state: RuntimeState
    pressure_level: PressureLevel
    health_score: int
    queue_depth: int
    split_validity: SplitValidity
    split_valid: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical node runtime split invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.entry_id):
            raise ValueError(f"Invalid entry_id: {self.entry_id}")

        if not _NODE_ID_PATTERN.fullmatch(self.node_id):
            raise ValueError(f"Invalid node_id: {self.node_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.entry_id}")

        if not 0 <= self.health_score <= 100:
            raise ValueError(f"health_score must be between 0 and 100: {self.entry_id}")

        if self.queue_depth < 0:
            raise ValueError(f"queue_depth must be >= 0: {self.entry_id}")

        if self.split_validity != "split_valid":
            raise ValueError(
                f"split_validity must be split_valid: {self.entry_id}"
            )

        if self.split_valid is not True:
            raise ValueError(f"split_valid must be True: {self.entry_id}")

        if self.entry_id == "noderuntimesplit_dev_001":
            if self.node_id != "dev_001":
                raise ValueError("noderuntimesplit_dev_001 must use dev_001")
            if self.node_type != "DEV_NODE":
                raise ValueError("noderuntimesplit_dev_001 must use DEV_NODE")
            if self.static_capacity_class != "medium":
                raise ValueError(
                    "noderuntimesplit_dev_001 must use static_capacity_class=medium"
                )
            if self.heavy_execution_allowed:
                raise ValueError(
                    "noderuntimesplit_dev_001 must not allow heavy execution"
                )
            if self.runtime_state != "open":
                raise ValueError(
                    "noderuntimesplit_dev_001 must use runtime_state=open"
                )
            if self.pressure_level != "normal":
                raise ValueError(
                    "noderuntimesplit_dev_001 must use pressure_level=normal"
                )

        if self.entry_id == "noderuntimesplit_home_001":
            if self.node_id != "home_001":
                raise ValueError("noderuntimesplit_home_001 must use home_001")
            if self.node_type != "HOME_NODE":
                raise ValueError("noderuntimesplit_home_001 must use HOME_NODE")
            if self.static_capacity_class != "heavy":
                raise ValueError(
                    "noderuntimesplit_home_001 must use static_capacity_class=heavy"
                )
            if not self.heavy_execution_allowed:
                raise ValueError(
                    "noderuntimesplit_home_001 must allow heavy execution"
                )
            if self.runtime_state != "throttled":
                raise ValueError(
                    "noderuntimesplit_home_001 must use runtime_state=throttled"
                )
            if self.pressure_level != "elevated":
                raise ValueError(
                    "noderuntimesplit_home_001 must use pressure_level=elevated"
                )

        if self.entry_id == "noderuntimesplit_mobile_001":
            if self.node_id != "mobile_001":
                raise ValueError("noderuntimesplit_mobile_001 must use mobile_001")
            if self.node_type != "MOBILE_NODE":
                raise ValueError("noderuntimesplit_mobile_001 must use MOBILE_NODE")
            if self.static_capacity_class != "light":
                raise ValueError(
                    "noderuntimesplit_mobile_001 must use static_capacity_class=light"
                )
            if self.heavy_execution_allowed:
                raise ValueError(
                    "noderuntimesplit_mobile_001 must not allow heavy execution"
                )
            if self.runtime_state != "open":
                raise ValueError(
                    "noderuntimesplit_mobile_001 must use runtime_state=open"
                )
            if self.pressure_level != "normal":
                raise ValueError(
                    "noderuntimesplit_mobile_001 must use pressure_level=normal"
                )


@dataclass(frozen=True, slots=True)
class NodeRuntimeSplitContract:
    """Canonical node runtime split contract."""

    total_entries: int
    heavy_execution_nodes: int
    throttled_runtime_nodes: int
    split_valid_entries: int
    entries: tuple[NodeRuntimeSplitEntry, ...]

    def __post_init__(self) -> None:
        """Validate aggregate node runtime split contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        heavy_execution_nodes = sum(
            1 for entry in self.entries if entry.heavy_execution_allowed
        )
        throttled_runtime_nodes = sum(
            1 for entry in self.entries if entry.runtime_state == "throttled"
        )
        split_valid_entries = sum(
            1 for entry in self.entries if entry.split_validity == "split_valid"
        )

        if self.heavy_execution_nodes != heavy_execution_nodes:
            raise ValueError("heavy_execution_nodes must match computed count")

        if self.throttled_runtime_nodes != throttled_runtime_nodes:
            raise ValueError("throttled_runtime_nodes must match computed count")

        if self.split_valid_entries != split_valid_entries:
            raise ValueError("split_valid_entries must match computed count")

        entry_ids = tuple(entry.entry_id for entry in self.entries)
        node_ids = tuple(entry.node_id for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate entry_id values detected")

        if len(set(node_ids)) != len(node_ids):
            raise ValueError("Duplicate node_id values detected")


def build_node_runtime_split_contract() -> NodeRuntimeSplitContract:
    """Build canonical node runtime split contract."""
    entries = (
        NodeRuntimeSplitEntry(
            entry_id="noderuntimesplit_dev_001",
            node_id="dev_001",
            node_type="DEV_NODE",
            static_capacity_class="medium",
            heavy_execution_allowed=False,
            runtime_state="open",
            pressure_level="normal",
            health_score=92,
            queue_depth=1,
            split_validity="split_valid",
            split_valid=True,
            description="Canonical DEV node runtime split entry.",
        ),
        NodeRuntimeSplitEntry(
            entry_id="noderuntimesplit_home_001",
            node_id="home_001",
            node_type="HOME_NODE",
            static_capacity_class="heavy",
            heavy_execution_allowed=True,
            runtime_state="throttled",
            pressure_level="elevated",
            health_score=78,
            queue_depth=4,
            split_validity="split_valid",
            split_valid=True,
            description="Canonical HOME node runtime split entry.",
        ),
        NodeRuntimeSplitEntry(
            entry_id="noderuntimesplit_mobile_001",
            node_id="mobile_001",
            node_type="MOBILE_NODE",
            static_capacity_class="light",
            heavy_execution_allowed=False,
            runtime_state="open",
            pressure_level="normal",
            health_score=88,
            queue_depth=0,
            split_validity="split_valid",
            split_valid=True,
            description="Canonical MOBILE node runtime split entry.",
        ),
    )

    return NodeRuntimeSplitContract(
        total_entries=len(entries),
        heavy_execution_nodes=sum(
            1 for entry in entries if entry.heavy_execution_allowed
        ),
        throttled_runtime_nodes=sum(
            1 for entry in entries if entry.runtime_state == "throttled"
        ),
        split_valid_entries=sum(
            1 for entry in entries if entry.split_validity == "split_valid"
        ),
        entries=entries,
    )
