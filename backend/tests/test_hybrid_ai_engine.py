"""SAFECODIUM — Tests for Hybrid AI Engine and Privacy Guard."""

import pytest
from backend.app.ai_engine.privacy_guard import (
    PrivacyPolicyManager,
    PrivacyMode,
    PrivacyAuthorizationError,
)
from backend.app.ai_engine.langgraph_orchestrator import LangGraphWorkflowCoordinator


def test_privacy_guard_local_only():
    """Verify that in LOCAL_ONLY mode, cloud providers (Gemini, OpenAI) are strictly blocked."""
    guard = PrivacyPolicyManager(mode=PrivacyMode.LOCAL_ONLY)

    # Local provider should be allowed
    guard.assert_provider_permitted("ollama")

    # Cloud providers must raise PrivacyAuthorizationError
    with pytest.raises(PrivacyAuthorizationError):
        guard.assert_provider_permitted("gemini")

    with pytest.raises(PrivacyAuthorizationError):
        guard.assert_provider_permitted("openai")


def test_privacy_guard_hybrid_with_consent():
    """Verify that in HYBRID mode, cloud providers require explicit user consent."""
    guard = PrivacyPolicyManager(mode=PrivacyMode.HYBRID)

    # Without consent: should raise PrivacyAuthorizationError
    with pytest.raises(PrivacyAuthorizationError):
        guard.assert_provider_permitted("gemini", has_explicit_consent=False)

    # With consent: should pass
    guard.assert_provider_permitted("gemini", has_explicit_consent=True)


@pytest.mark.asyncio
async def test_langgraph_workflow_execution():
    """Verify state transitions and trace recording across LangGraph agents."""
    coordinator = LangGraphWorkflowCoordinator()
    
    state = await coordinator.run_full_security_workflow(
        project_id="test-proj-01",
        source_code="char buf[16]; strcpy(buf, input);",
        file_path="main.c",
        language="c_cpp",
        provider_name="ollama",  # Local Ollama allowed without cloud consent
        user_cloud_consent=False,
    )

    assert state.current_agent == "SecurityReportingAgent"
    assert len(state.execution_trace) == 6
    assert "CodeIntelligenceAgent" in state.execution_trace[0]
    assert "SecurityReportingAgent" in state.execution_trace[-1]

