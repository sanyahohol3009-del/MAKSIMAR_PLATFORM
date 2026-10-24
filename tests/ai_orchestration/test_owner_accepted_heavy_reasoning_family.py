from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import build_jarvis_live_runtime_model_role_profiles

def test_owner_accepted_family_preserves_distinct_role_and_proposal_boundaries():
    profiles={p.role_id:p for p in build_jarvis_live_runtime_model_role_profiles()}
    heavy=profiles['heavy_reasoning_model']
    assert heavy.model_id=='jarvis-live:qwen14b'
    assert heavy.target_model_id=='qwen2.5-coder:14b'
    assert heavy.role=='heavy_reasoning'
    assert heavy.proposal_only and not heavy.agents_direct_access_allowed
    assert not heavy.pc_control_allowed and not heavy.model_download_allowed
    assert profiles['heavy_coder_model'].model_id=='jarvis:coder14b'
