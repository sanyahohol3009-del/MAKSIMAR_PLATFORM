from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.end_to_end_orchestration_runtime import (
    build_end_to_end_orchestration_runtime_contract,
)
from MAKSIMAR_CORE_LIB.real_ai_services_model_adapters import (
    build_real_ai_services_model_adapters_contract,
)
from MAKSIMAR_CORE_LIB.real_dashboard_clients_mobile import (
    build_real_dashboard_clients_mobile_contract,
)
from MAKSIMAR_CORE_LIB.real_voice_runtime import (
    build_real_voice_runtime_contract,
)
from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


FullTestEntryId = Literal[
    "fulltest_orchestration_001",
    "fulltest_clients_voice_001",
    "fulltest_ai_transport_001",
]

TestDomain = Literal[
    "orchestration_domain",
    "clients_voice_domain",
    "ai_transport_domain",
]

TestCoverageClass = Literal[
    "critical_path_coverage",
]

TestExecutionMode = Literal[
    "contract_and_runtime_smoke",
]

FullTestStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^fulltest_[a-z][a-z0-9_]*$")
_ORCH_ID_PATTERN = re.compile(r"^orchestration_[a-z][a-z0-9_]*$")
_CLIENT_ID_PATTERN = re.compile(r"^realclient_[a-z][a-z0-9_]*$")
_VOICE_ID_PATTERN = re.compile(r"^realvoice_[a-z][a-z0-9_]*$")
_AI_ID_PATTERN = re.compile(r"^aiservice_[a-z][a-z0-9_]*$")
_TRANSPORT_ID_PATTERN = re.compile(r"^transport_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class FullTestSuiteEntry:
    """Canonical full test suite entry."""

    full_test_entry_id: FullTestEntryId
    test_domain: TestDomain
    linked_orchestration_entry_id: str | None
    linked_real_client_entry_id: str | None
    linked_real_voice_entry_id: str | None
    linked_real_ai_service_entry_id: str | None
    linked_transport_entry_id: str | None
    test_coverage_class: TestCoverageClass
    test_execution_mode: TestExecutionMode
    compile_pass_required: bool
    smoke_output_required: bool
    explainable_required: bool
    production_path_allowed: bool
    full_test_status: FullTestStatus
    description: str

    def __post_init__(self) -> None:
        """Validate full test suite invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.full_test_entry_id):
            raise ValueError(
                f"Invalid full_test_entry_id: {self.full_test_entry_id}"
            )

        if self.linked_orchestration_entry_id is not None:
            if not _ORCH_ID_PATTERN.fullmatch(self.linked_orchestration_entry_id):
                raise ValueError(
                    f"Invalid linked_orchestration_entry_id: {self.linked_orchestration_entry_id}"
                )

        if self.linked_real_client_entry_id is not None:
            if not _CLIENT_ID_PATTERN.fullmatch(self.linked_real_client_entry_id):
                raise ValueError(
                    f"Invalid linked_real_client_entry_id: {self.linked_real_client_entry_id}"
                )

        if self.linked_real_voice_entry_id is not None:
            if not _VOICE_ID_PATTERN.fullmatch(self.linked_real_voice_entry_id):
                raise ValueError(
                    f"Invalid linked_real_voice_entry_id: {self.linked_real_voice_entry_id}"
                )

        if self.linked_real_ai_service_entry_id is not None:
            if not _AI_ID_PATTERN.fullmatch(self.linked_real_ai_service_entry_id):
                raise ValueError(
                    f"Invalid linked_real_ai_service_entry_id: {self.linked_real_ai_service_entry_id}"
                )

        if self.linked_transport_entry_id is not None:
            if not _TRANSPORT_ID_PATTERN.fullmatch(self.linked_transport_entry_id):
                raise ValueError(
                    f"Invalid linked_transport_entry_id: {self.linked_transport_entry_id}"
                )

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.full_test_entry_id}"
            )

        if self.test_coverage_class != "critical_path_coverage":
            raise ValueError(
                f"test_coverage_class must be critical_path_coverage: {self.full_test_entry_id}"
            )

        if self.test_execution_mode != "contract_and_runtime_smoke":
            raise ValueError(
                f"test_execution_mode must be contract_and_runtime_smoke: {self.full_test_entry_id}"
            )

        if not self.compile_pass_required:
            raise ValueError(
                f"compile_pass_required must be True: {self.full_test_entry_id}"
            )

        if not self.smoke_output_required:
            raise ValueError(
                f"smoke_output_required must be True: {self.full_test_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.full_test_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.full_test_entry_id}"
            )

        if self.full_test_status != "defined":
            raise ValueError(
                f"full_test_status must be defined: {self.full_test_entry_id}"
            )

        if self.full_test_entry_id == "fulltest_orchestration_001":
            if self.test_domain != "orchestration_domain":
                raise ValueError(
                    "fulltest_orchestration_001 must use orchestration_domain"
                )
            if self.linked_orchestration_entry_id != "orchestration_heavy_execution_001":
                raise ValueError(
                    "fulltest_orchestration_001 must link orchestration_heavy_execution_001"
                )
            if self.linked_real_client_entry_id is not None:
                raise ValueError(
                    "fulltest_orchestration_001 must not link client entry"
                )
            if self.linked_real_voice_entry_id is not None:
                raise ValueError(
                    "fulltest_orchestration_001 must not link voice entry"
                )
            if self.linked_real_ai_service_entry_id is not None:
                raise ValueError(
                    "fulltest_orchestration_001 must not link ai service entry"
                )
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError(
                    "fulltest_orchestration_001 must link transport_dev_home_001"
                )

        if self.full_test_entry_id == "fulltest_clients_voice_001":
            if self.test_domain != "clients_voice_domain":
                raise ValueError(
                    "fulltest_clients_voice_001 must use clients_voice_domain"
                )
            if self.linked_orchestration_entry_id is not None:
                raise ValueError(
                    "fulltest_clients_voice_001 must not link orchestration entry"
                )
            if self.linked_real_client_entry_id != "realclient_mobile_001":
                raise ValueError(
                    "fulltest_clients_voice_001 must link realclient_mobile_001"
                )
            if self.linked_real_voice_entry_id != "realvoice_show_memory_001":
                raise ValueError(
                    "fulltest_clients_voice_001 must link realvoice_show_memory_001"
                )
            if self.linked_real_ai_service_entry_id is not None:
                raise ValueError(
                    "fulltest_clients_voice_001 must not link ai service entry"
                )
            if self.linked_transport_entry_id != "transport_mobile_local_001":
                raise ValueError(
                    "fulltest_clients_voice_001 must link transport_mobile_local_001"
                )

        if self.full_test_entry_id == "fulltest_ai_transport_001":
            if self.test_domain != "ai_transport_domain":
                raise ValueError(
                    "fulltest_ai_transport_001 must use ai_transport_domain"
                )
            if self.linked_orchestration_entry_id is not None:
                raise ValueError(
                    "fulltest_ai_transport_001 must not link orchestration entry"
                )
            if self.linked_real_client_entry_id is not None:
                raise ValueError(
                    "fulltest_ai_transport_001 must not link client entry"
                )
            if self.linked_real_voice_entry_id != "realvoice_show_monitoring_001":
                raise ValueError(
                    "fulltest_ai_transport_001 must link realvoice_show_monitoring_001"
                )
            if self.linked_real_ai_service_entry_id != "aiservice_visual_001":
                raise ValueError(
                    "fulltest_ai_transport_001 must link aiservice_visual_001"
                )
            if self.linked_transport_entry_id != "transport_dev_home_001":
                raise ValueError(
                    "fulltest_ai_transport_001 must link transport_dev_home_001"
                )


@dataclass(frozen=True, slots=True)
class FullTestSuiteContract:
    """Unified full test suite contract."""

    total_entries: int
    orchestration_domain_entries: int
    clients_voice_domain_entries: int
    ai_transport_domain_entries: int
    defined_entries: int
    entries: tuple[FullTestSuiteEntry, ...]

    def __post_init__(self) -> None:
        """Validate full test suite contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        orchestration_domain_entries = sum(
            1 for entry in self.entries if entry.test_domain == "orchestration_domain"
        )
        clients_voice_domain_entries = sum(
            1 for entry in self.entries if entry.test_domain == "clients_voice_domain"
        )
        ai_transport_domain_entries = sum(
            1 for entry in self.entries if entry.test_domain == "ai_transport_domain"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.full_test_status == "defined"
        )

        if self.orchestration_domain_entries != orchestration_domain_entries:
            raise ValueError(
                "orchestration_domain_entries must match computed count"
            )

        if self.clients_voice_domain_entries != clients_voice_domain_entries:
            raise ValueError(
                "clients_voice_domain_entries must match computed count"
            )

        if self.ai_transport_domain_entries != ai_transport_domain_entries:
            raise ValueError(
                "ai_transport_domain_entries must match computed count"
            )

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.full_test_entry_id for entry in self.entries)
        domains = tuple(entry.test_domain for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate full_test_entry_id values detected")

        if len(set(domains)) != len(domains):
            raise ValueError("Duplicate test_domain values detected")


def build_full_test_suite_contract() -> FullTestSuiteContract:
    """Build canonical full test suite contract."""
    orchestration = build_end_to_end_orchestration_runtime_contract()
    clients = build_real_dashboard_clients_mobile_contract()
    voice = build_real_voice_runtime_contract()
    ai_services = build_real_ai_services_model_adapters_contract()
    transport = build_secure_sync_update_transport_contract()

    orchestration_ids = {entry.orchestration_entry_id for entry in orchestration.entries}
    client_ids = {entry.real_client_entry_id for entry in clients.entries}
    voice_ids = {entry.real_voice_runtime_entry_id for entry in voice.entries}
    ai_service_ids = {entry.real_ai_service_entry_id for entry in ai_services.entries}
    transport_ids = {entry.secure_transport_entry_id for entry in transport.entries}

    required_orchestration_ids = {"orchestration_heavy_execution_001"}
    required_client_ids = {"realclient_mobile_001"}
    required_voice_ids = {
        "realvoice_show_memory_001",
        "realvoice_show_monitoring_001",
    }
    required_ai_service_ids = {"aiservice_visual_001"}
    required_transport_ids = {
        "transport_dev_home_001",
        "transport_mobile_local_001",
    }

    for label, required, actual in (
        ("orchestration ids", required_orchestration_ids, orchestration_ids),
        ("client ids", required_client_ids, client_ids),
        ("voice ids", required_voice_ids, voice_ids),
        ("ai service ids", required_ai_service_ids, ai_service_ids),
        ("transport ids", required_transport_ids, transport_ids),
    ):
        missing = required - actual
        if missing:
            raise ValueError(f"Missing {label}: {sorted(missing)}")

    entries = (
        FullTestSuiteEntry(
            full_test_entry_id="fulltest_orchestration_001",
            test_domain="orchestration_domain",
            linked_orchestration_entry_id="orchestration_heavy_execution_001",
            linked_real_client_entry_id=None,
            linked_real_voice_entry_id=None,
            linked_real_ai_service_entry_id=None,
            linked_transport_entry_id="transport_dev_home_001",
            test_coverage_class="critical_path_coverage",
            test_execution_mode="contract_and_runtime_smoke",
            compile_pass_required=True,
            smoke_output_required=True,
            explainable_required=True,
            production_path_allowed=True,
            full_test_status="defined",
            description="Canonical full test coverage entry for orchestration domain.",
        ),
        FullTestSuiteEntry(
            full_test_entry_id="fulltest_clients_voice_001",
            test_domain="clients_voice_domain",
            linked_orchestration_entry_id=None,
            linked_real_client_entry_id="realclient_mobile_001",
            linked_real_voice_entry_id="realvoice_show_memory_001",
            linked_real_ai_service_entry_id=None,
            linked_transport_entry_id="transport_mobile_local_001",
            test_coverage_class="critical_path_coverage",
            test_execution_mode="contract_and_runtime_smoke",
            compile_pass_required=True,
            smoke_output_required=True,
            explainable_required=True,
            production_path_allowed=True,
            full_test_status="defined",
            description="Canonical full test coverage entry for clients and voice domain.",
        ),
        FullTestSuiteEntry(
            full_test_entry_id="fulltest_ai_transport_001",
            test_domain="ai_transport_domain",
            linked_orchestration_entry_id=None,
            linked_real_client_entry_id=None,
            linked_real_voice_entry_id="realvoice_show_monitoring_001",
            linked_real_ai_service_entry_id="aiservice_visual_001",
            linked_transport_entry_id="transport_dev_home_001",
            test_coverage_class="critical_path_coverage",
            test_execution_mode="contract_and_runtime_smoke",
            compile_pass_required=True,
            smoke_output_required=True,
            explainable_required=True,
            production_path_allowed=True,
            full_test_status="defined",
            description="Canonical full test coverage entry for AI and transport domain.",
        ),
    )

    orchestration_domain_entries = sum(
        1 for entry in entries if entry.test_domain == "orchestration_domain"
    )
    clients_voice_domain_entries = sum(
        1 for entry in entries if entry.test_domain == "clients_voice_domain"
    )
    ai_transport_domain_entries = sum(
        1 for entry in entries if entry.test_domain == "ai_transport_domain"
    )
    defined_entries = sum(
        1 for entry in entries if entry.full_test_status == "defined"
    )

    return FullTestSuiteContract(
        total_entries=len(entries),
        orchestration_domain_entries=orchestration_domain_entries,
        clients_voice_domain_entries=clients_voice_domain_entries,
        ai_transport_domain_entries=ai_transport_domain_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
