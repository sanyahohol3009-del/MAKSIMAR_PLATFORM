import pytest

from MAKSIMAR_CORE_LIB.mobile_screen_observer.mobile_screen_consent_contract import (
    MobileScreenConsentContract,
)


def test_mobile_screen_consent_contract_smoke() -> None:
    consent = MobileScreenConsentContract(
        consent_id="screen_consent_001",
        session_id="screen_session_001",
        owner_identity_id="owner_001",
        device_id="android_device_001",
        consent_state="granted",
        consent_epoch_ms=1000,
        expires_epoch_ms=2000,
        explicit_owner_consent_required=True,
        visible_on_device_required=True,
        audit_event_required=True,
        revocation_supported=True,
        remote_assistance_enabled_by_default=False,
        dashboard_bypass_allowed=False,
        runtime_mutation_allowed=False,
        core_write_allowed=False,
    )

    assert consent.explicit_owner_consent_required is True
    assert consent.remote_assistance_enabled_by_default is False


def test_mobile_screen_consent_rejects_remote_assistance_default() -> None:
    with pytest.raises(ValueError, match="remote_assistance_enabled_by_default must be False"):
        MobileScreenConsentContract(
            consent_id="screen_consent_bad",
            session_id="screen_session_001",
            owner_identity_id="owner_001",
            device_id="android_device_001",
            consent_state="requested",
            consent_epoch_ms=1000,
            expires_epoch_ms=0,
            explicit_owner_consent_required=True,
            visible_on_device_required=True,
            audit_event_required=True,
            revocation_supported=True,
            remote_assistance_enabled_by_default=True,
            dashboard_bypass_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )


def test_mobile_screen_consent_rejects_dashboard_bypass() -> None:
    with pytest.raises(ValueError, match="dashboard_bypass_allowed must be False"):
        MobileScreenConsentContract(
            consent_id="screen_consent_bypass_bad",
            session_id="screen_session_001",
            owner_identity_id="owner_001",
            device_id="ios_device_001",
            consent_state="requested",
            consent_epoch_ms=1000,
            expires_epoch_ms=0,
            explicit_owner_consent_required=True,
            visible_on_device_required=True,
            audit_event_required=True,
            revocation_supported=True,
            remote_assistance_enabled_by_default=False,
            dashboard_bypass_allowed=True,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )
