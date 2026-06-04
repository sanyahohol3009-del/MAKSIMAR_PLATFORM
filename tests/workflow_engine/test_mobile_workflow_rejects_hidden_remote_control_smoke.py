import pytest

from ANDROID_SHELL.workflow_adapter.android_local_workflow_intent_client import (
    AndroidLocalWorkflowIntentClient,
)
from ANDROID_SHELL.workflow_adapter.android_workflow_capability_limits import (
    AndroidWorkflowCapabilityLimits,
    build_android_workflow_capability_limits,
)
from ANDROID_SHELL.workflow_adapter.android_workflow_permission_bridge import (
    AndroidWorkflowPermissionBridge,
    build_android_workflow_permission_bridge,
)
from IOS_SHELL.workflow_adapter.ios_local_workflow_intent_client import (
    IOSLocalWorkflowIntentClient,
)
from IOS_SHELL.workflow_adapter.ios_workflow_capability_limits import (
    IOSWorkflowCapabilityLimits,
    build_ios_workflow_capability_limits,
)
from IOS_SHELL.workflow_adapter.ios_workflow_permission_bridge import (
    IOSWorkflowPermissionBridge,
    build_ios_workflow_permission_bridge,
)
from MAKSIMAR_CORE_LIB.workflow_engine.workflow_safety_policy_contract import (
    build_workflow_safety_policy_contract,
)


def test_mobile_workflow_rejects_hidden_remote_control_on_android_surfaces() -> None:
    with pytest.raises(ValueError):
        AndroidWorkflowCapabilityLimits(
            limits_id="android.hidden.remote.capability",
            allowed_capability_refs=("local_ai_workflow_proposal",),
            platform_capability_refs=("local_ai_workflow_proposal",),
            hidden_remote_control_allowed=True,
        )

    with pytest.raises(ValueError):
        AndroidWorkflowPermissionBridge(
            bridge_id="android.hidden.remote.bridge",
            capability_limits=build_android_workflow_capability_limits(),
            explicit_user_permission_granted=True,
            device_owner_confirmed=True,
            hidden_remote_control_allowed=True,
        )

    with pytest.raises(ValueError):
        AndroidLocalWorkflowIntentClient(
            client_id="android.hidden.remote.client",
            permission_bridge=build_android_workflow_permission_bridge(
                explicit_user_permission_granted=True,
                device_owner_confirmed=True,
            ),
            safety_policy=build_workflow_safety_policy_contract(),
            hidden_remote_control_allowed=True,
        )


def test_mobile_workflow_rejects_hidden_remote_control_on_ios_surfaces() -> None:
    with pytest.raises(ValueError):
        IOSWorkflowCapabilityLimits(
            limits_id="ios.hidden.remote.capability",
            allowed_capability_refs=("local_ai_workflow_proposal",),
            platform_capability_refs=("local_ai_workflow_proposal",),
            hidden_remote_control_allowed=True,
        )

    with pytest.raises(ValueError):
        IOSWorkflowPermissionBridge(
            bridge_id="ios.hidden.remote.bridge",
            capability_limits=build_ios_workflow_capability_limits(),
            explicit_user_permission_granted=True,
            device_owner_confirmed=True,
            hidden_remote_control_allowed=True,
        )

    with pytest.raises(ValueError):
        IOSLocalWorkflowIntentClient(
            client_id="ios.hidden.remote.client",
            permission_bridge=build_ios_workflow_permission_bridge(
                explicit_user_permission_granted=True,
                device_owner_confirmed=True,
            ),
            safety_policy=build_workflow_safety_policy_contract(),
            hidden_remote_control_allowed=True,
        )
