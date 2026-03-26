from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.operations_deployment_backup_incidents import (
    build_operations_deployment_backup_incidents_contract,
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


ProductEntryId = Literal[
    "product_core_dashboard_001",
    "product_mobile_voice_001",
    "product_visual_ai_001",
]

ProductSurface = Literal[
    "dashboard_surface",
    "mobile_voice_surface",
    "visual_ai_surface",
]

OnboardingMode = Literal[
    "guided_read_only_onboarding",
    "guided_mobile_onboarding",
    "guided_visual_onboarding",
]

PackagingMode = Literal[
    "control_ready_package",
    "mobile_ready_package",
    "visual_ready_package",
]

HardeningClass = Literal[
    "baseline_hardened",
    "runtime_hardened",
]

ProductStatus = Literal[
    "defined",
]


_ENTRY_ID_PATTERN = re.compile(r"^product_[a-z][a-z0-9_]*$")
_OPS_ID_PATTERN = re.compile(r"^ops_[a-z][a-z0-9_]*$")
_CLIENT_ID_PATTERN = re.compile(r"^realclient_[a-z][a-z0-9_]*$")
_VOICE_ID_PATTERN = re.compile(r"^realvoice_[a-z][a-z0-9_]*$")
_AI_ID_PATTERN = re.compile(r"^aiservice_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ProductHardeningOnboardingPackagingEntry:
    """Canonical product hardening / onboarding / packaging entry."""

    product_entry_id: ProductEntryId
    product_surface: ProductSurface
    linked_ops_entry_id: str
    linked_real_client_entry_id: str
    linked_real_voice_entry_id: str | None
    linked_real_ai_service_entry_id: str | None
    onboarding_mode: OnboardingMode
    packaging_mode: PackagingMode
    hardening_class: HardeningClass
    read_only_onboarding_required: bool
    explainable_required: bool
    production_path_allowed: bool
    product_status: ProductStatus
    description: str

    def __post_init__(self) -> None:
        """Validate product hardening / onboarding / packaging invariants."""
        if not _ENTRY_ID_PATTERN.fullmatch(self.product_entry_id):
            raise ValueError(f"Invalid product_entry_id: {self.product_entry_id}")

        if not _OPS_ID_PATTERN.fullmatch(self.linked_ops_entry_id):
            raise ValueError(f"Invalid linked_ops_entry_id: {self.linked_ops_entry_id}")

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

        if not self.description.strip():
            raise ValueError(f"description must not be empty for {self.product_entry_id}")

        if not self.read_only_onboarding_required:
            raise ValueError(
                f"read_only_onboarding_required must be True: {self.product_entry_id}"
            )

        if not self.explainable_required:
            raise ValueError(
                f"explainable_required must be True: {self.product_entry_id}"
            )

        if not self.production_path_allowed:
            raise ValueError(
                f"production_path_allowed must be True: {self.product_entry_id}"
            )

        if self.product_status != "defined":
            raise ValueError(f"product_status must be defined: {self.product_entry_id}")

        if self.product_entry_id == "product_core_dashboard_001":
            if self.product_surface != "dashboard_surface":
                raise ValueError("product_core_dashboard_001 must use dashboard_surface")
            if self.linked_ops_entry_id != "ops_dev_control_001":
                raise ValueError("product_core_dashboard_001 must link ops_dev_control_001")
            if self.linked_real_client_entry_id != "realclient_dashboard_001":
                raise ValueError(
                    "product_core_dashboard_001 must link realclient_dashboard_001"
                )
            if self.linked_real_voice_entry_id != "realvoice_show_monitoring_001":
                raise ValueError(
                    "product_core_dashboard_001 must link realvoice_show_monitoring_001"
                )
            if self.linked_real_ai_service_entry_id is not None:
                raise ValueError(
                    "product_core_dashboard_001 must not link AI service directly"
                )
            if self.onboarding_mode != "guided_read_only_onboarding":
                raise ValueError(
                    "product_core_dashboard_001 must use guided_read_only_onboarding"
                )
            if self.packaging_mode != "control_ready_package":
                raise ValueError(
                    "product_core_dashboard_001 must use control_ready_package"
                )
            if self.hardening_class != "baseline_hardened":
                raise ValueError(
                    "product_core_dashboard_001 must use baseline_hardened"
                )

        if self.product_entry_id == "product_mobile_voice_001":
            if self.product_surface != "mobile_voice_surface":
                raise ValueError("product_mobile_voice_001 must use mobile_voice_surface")
            if self.linked_ops_entry_id != "ops_mobile_proxy_001":
                raise ValueError("product_mobile_voice_001 must link ops_mobile_proxy_001")
            if self.linked_real_client_entry_id != "realclient_mobile_001":
                raise ValueError(
                    "product_mobile_voice_001 must link realclient_mobile_001"
                )
            if self.linked_real_voice_entry_id != "realvoice_show_memory_001":
                raise ValueError(
                    "product_mobile_voice_001 must link realvoice_show_memory_001"
                )
            if self.linked_real_ai_service_entry_id != "aiservice_coding_001":
                raise ValueError(
                    "product_mobile_voice_001 must link aiservice_coding_001"
                )
            if self.onboarding_mode != "guided_mobile_onboarding":
                raise ValueError(
                    "product_mobile_voice_001 must use guided_mobile_onboarding"
                )
            if self.packaging_mode != "mobile_ready_package":
                raise ValueError(
                    "product_mobile_voice_001 must use mobile_ready_package"
                )
            if self.hardening_class != "runtime_hardened":
                raise ValueError(
                    "product_mobile_voice_001 must use runtime_hardened"
                )

        if self.product_entry_id == "product_visual_ai_001":
            if self.product_surface != "visual_ai_surface":
                raise ValueError("product_visual_ai_001 must use visual_ai_surface")
            if self.linked_ops_entry_id != "ops_home_execution_001":
                raise ValueError("product_visual_ai_001 must link ops_home_execution_001")
            if self.linked_real_client_entry_id != "realclient_ar_glasses_001":
                raise ValueError(
                    "product_visual_ai_001 must link realclient_ar_glasses_001"
                )
            if self.linked_real_voice_entry_id != "realvoice_show_monitoring_001":
                raise ValueError(
                    "product_visual_ai_001 must link realvoice_show_monitoring_001"
                )
            if self.linked_real_ai_service_entry_id != "aiservice_visual_001":
                raise ValueError(
                    "product_visual_ai_001 must link aiservice_visual_001"
                )
            if self.onboarding_mode != "guided_visual_onboarding":
                raise ValueError(
                    "product_visual_ai_001 must use guided_visual_onboarding"
                )
            if self.packaging_mode != "visual_ready_package":
                raise ValueError(
                    "product_visual_ai_001 must use visual_ready_package"
                )
            if self.hardening_class != "runtime_hardened":
                raise ValueError(
                    "product_visual_ai_001 must use runtime_hardened"
                )


@dataclass(frozen=True, slots=True)
class ProductHardeningOnboardingPackagingContract:
    """Unified product hardening / onboarding / packaging contract."""

    total_entries: int
    dashboard_surface_entries: int
    mobile_voice_entries: int
    visual_ai_entries: int
    defined_entries: int
    entries: tuple[ProductHardeningOnboardingPackagingEntry, ...]

    def __post_init__(self) -> None:
        """Validate product hardening / onboarding / packaging contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        dashboard_surface_entries = sum(
            1 for entry in self.entries if entry.product_surface == "dashboard_surface"
        )
        mobile_voice_entries = sum(
            1 for entry in self.entries if entry.product_surface == "mobile_voice_surface"
        )
        visual_ai_entries = sum(
            1 for entry in self.entries if entry.product_surface == "visual_ai_surface"
        )
        defined_entries = sum(
            1 for entry in self.entries if entry.product_status == "defined"
        )

        if self.dashboard_surface_entries != dashboard_surface_entries:
            raise ValueError("dashboard_surface_entries must match computed count")

        if self.mobile_voice_entries != mobile_voice_entries:
            raise ValueError("mobile_voice_entries must match computed count")

        if self.visual_ai_entries != visual_ai_entries:
            raise ValueError("visual_ai_entries must match computed count")

        if self.defined_entries != defined_entries:
            raise ValueError("defined_entries must match computed count")

        entry_ids = tuple(entry.product_entry_id for entry in self.entries)
        surfaces = tuple(entry.product_surface for entry in self.entries)

        if len(set(entry_ids)) != len(entry_ids):
            raise ValueError("Duplicate product_entry_id values detected")

        if len(set(surfaces)) != len(surfaces):
            raise ValueError("Duplicate product_surface values detected")


def build_product_hardening_onboarding_packaging_contract() -> ProductHardeningOnboardingPackagingContract:
    """Build canonical product hardening / onboarding / packaging contract."""
    ops = build_operations_deployment_backup_incidents_contract()
    clients = build_real_dashboard_clients_mobile_contract()
    voice = build_real_voice_runtime_contract()
    ai_services = build_real_ai_services_model_adapters_contract()

    ops_ids = {entry.ops_entry_id for entry in ops.entries}
    client_ids = {entry.real_client_entry_id for entry in clients.entries}
    voice_ids = {entry.real_voice_runtime_entry_id for entry in voice.entries}
    ai_service_ids = {entry.real_ai_service_entry_id for entry in ai_services.entries}

    required_ops_ids = {
        "ops_dev_control_001",
        "ops_mobile_proxy_001",
        "ops_home_execution_001",
    }
    required_client_ids = {
        "realclient_dashboard_001",
        "realclient_mobile_001",
        "realclient_ar_glasses_001",
    }
    required_voice_ids = {
        "realvoice_show_memory_001",
        "realvoice_show_monitoring_001",
    }
    required_ai_service_ids = {
        "aiservice_coding_001",
        "aiservice_visual_001",
    }

    for label, required, actual in (
        ("ops ids", required_ops_ids, ops_ids),
        ("client ids", required_client_ids, client_ids),
        ("voice ids", required_voice_ids, voice_ids),
        ("ai service ids", required_ai_service_ids, ai_service_ids),
    ):
        missing = required - actual
        if missing:
            raise ValueError(f"Missing {label}: {sorted(missing)}")

    entries = (
        ProductHardeningOnboardingPackagingEntry(
            product_entry_id="product_core_dashboard_001",
            product_surface="dashboard_surface",
            linked_ops_entry_id="ops_dev_control_001",
            linked_real_client_entry_id="realclient_dashboard_001",
            linked_real_voice_entry_id="realvoice_show_monitoring_001",
            linked_real_ai_service_entry_id=None,
            onboarding_mode="guided_read_only_onboarding",
            packaging_mode="control_ready_package",
            hardening_class="baseline_hardened",
            read_only_onboarding_required=True,
            explainable_required=True,
            production_path_allowed=True,
            product_status="defined",
            description="Canonical hardened package for core dashboard surface.",
        ),
        ProductHardeningOnboardingPackagingEntry(
            product_entry_id="product_mobile_voice_001",
            product_surface="mobile_voice_surface",
            linked_ops_entry_id="ops_mobile_proxy_001",
            linked_real_client_entry_id="realclient_mobile_001",
            linked_real_voice_entry_id="realvoice_show_memory_001",
            linked_real_ai_service_entry_id="aiservice_coding_001",
            onboarding_mode="guided_mobile_onboarding",
            packaging_mode="mobile_ready_package",
            hardening_class="runtime_hardened",
            read_only_onboarding_required=True,
            explainable_required=True,
            production_path_allowed=True,
            product_status="defined",
            description="Canonical hardened package for mobile voice surface.",
        ),
        ProductHardeningOnboardingPackagingEntry(
            product_entry_id="product_visual_ai_001",
            product_surface="visual_ai_surface",
            linked_ops_entry_id="ops_home_execution_001",
            linked_real_client_entry_id="realclient_ar_glasses_001",
            linked_real_voice_entry_id="realvoice_show_monitoring_001",
            linked_real_ai_service_entry_id="aiservice_visual_001",
            onboarding_mode="guided_visual_onboarding",
            packaging_mode="visual_ready_package",
            hardening_class="runtime_hardened",
            read_only_onboarding_required=True,
            explainable_required=True,
            production_path_allowed=True,
            product_status="defined",
            description="Canonical hardened package for visual AI surface.",
        ),
    )

    dashboard_surface_entries = sum(
        1 for entry in entries if entry.product_surface == "dashboard_surface"
    )
    mobile_voice_entries = sum(
        1 for entry in entries if entry.product_surface == "mobile_voice_surface"
    )
    visual_ai_entries = sum(
        1 for entry in entries if entry.product_surface == "visual_ai_surface"
    )
    defined_entries = sum(
        1 for entry in entries if entry.product_status == "defined"
    )

    return ProductHardeningOnboardingPackagingContract(
        total_entries=len(entries),
        dashboard_surface_entries=dashboard_surface_entries,
        mobile_voice_entries=mobile_voice_entries,
        visual_ai_entries=visual_ai_entries,
        defined_entries=defined_entries,
        entries=entries,
    )
