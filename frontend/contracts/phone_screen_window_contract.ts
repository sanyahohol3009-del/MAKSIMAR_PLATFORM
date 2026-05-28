export type PhoneScreenPlatform = "android" | "ios";

export type PhoneScreenObserverState =
  | "not_connected"
  | "consent_required"
  | "observing_metadata"
  | "paused"
  | "blocked";

export type PhoneScreenConsentState =
  | "consent_required"
  | "consent_granted"
  | "consent_revoked"
  | "blocked";

export type PhoneScreenRemoteAssistanceState =
  | "disabled"
  | "approval_required"
  | "approved_intent_pending"
  | "rejected";

export interface PhoneScreenWindowReadModelContract {
  window_id: string;
  panel_id: string;
  device_id: string;
  owner_identity_id: string;
  platform: PhoneScreenPlatform;
  dashboard_section: "Phone Window";
  observer_state: PhoneScreenObserverState;
  consent_state: PhoneScreenConsentState;
  frame_ref: string;
  frame_reference_only: true;
  read_only: true;
  remote_assistance_state: PhoneScreenRemoteAssistanceState;
  remote_assistance_requires_approval: true;
  dashboard_control_allowed: false;
  direct_execution_allowed: false;
  child_control_surface: false;
  family_children_surface_required: true;
  audit_visible: true;
  runtime_mutation_allowed: false;
  core_write_allowed: false;
  source_of_truth_override_allowed: false;
}

export interface PhoneScreenWindowPanelContract {
  panel_id: string;
  panel_kind: "phone_screen_window";
  dashboard_section: "Phone Window";
  source_binding: "mobile_screen_observer";
  read_model_binding: "PhoneScreenWindowReadModel";
  read_only_default: true;
  can_show_frame_reference: true;
  can_show_consent_state: true;
  can_show_remote_assistance_intent: true;
  can_show_audit_state: true;
  dashboard_direct_execution_allowed: false;
  device_control_execution_allowed: false;
  child_control_allowed: false;
  family_children_surface_allowed: false;
  runtime_mutation_allowed: false;
  core_write_allowed: false;
  source_of_truth_override_allowed: false;
}

export interface PhoneScreenButtonIntentContract {
  intent_id: string;
  panel_id: string;
  device_id: string;
  owner_identity_id: string;
  button_id:
    | "refresh_frame_reference"
    | "request_remote_assistance"
    | "revoke_screen_consent"
    | "open_family_children_section";
  intent_type:
    | "read_model_refresh"
    | "remote_assistance_request"
    | "consent_revoke_request"
    | "navigation_request";
  approval_required: true;
  audit_required: true;
  read_only_intent: true;
  dashboard_direct_execution_allowed: false;
  device_control_execution_allowed: false;
  remote_assistance_requires_approval: true;
  child_control_intent_allowed: false;
  runtime_mutation_allowed: false;
  core_write_allowed: false;
  source_of_truth_override_allowed: false;
}
