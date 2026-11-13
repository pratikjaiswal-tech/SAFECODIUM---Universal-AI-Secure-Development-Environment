"""SAFECODIUM — End-to-End IDE, AI & Verification Integration Tests."""

import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.db.session import init_db
from backend.app.ai_engine.privacy_guard import privacy_manager, PrivacyMode, PrivacyAuthorizationError
from backend.app.services.language_adapters.registry import language_registry
from backend.app.services.autopilot.engine import AutoPilotEngine


@pytest.mark.asyncio
async def test_e2e_language_diagnostics_endpoint():
    """Verify IDE frontend diagnostics API with multi-language payloads."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test Python payload
        py_res = await client.post(
            "/api/v1/languages/diagnostics",
            json={"filename": "handler.py", "code": "def run(cmd):\n    eval(cmd)\n"},
        )
        assert py_res.status_code == 200
        py_data = py_res.json()
        assert py_data["language_id"] == "python"
        assert len(py_data["diagnostics"]) > 0

        # 2. Test Capabilities listing
        cap_res = await client.get("/api/v1/languages/capabilities")
        assert cap_res.status_code == 200
        assert cap_res.json()["total_languages"] >= 6


@pytest.mark.asyncio
async def test_e2e_privacy_mode_enforcement():
    """Verify backend enforces privacy modes and prevents accidental cloud leakage."""
    # Set to LOCAL_ONLY
    privacy_manager.set_mode(PrivacyMode.LOCAL_ONLY)
    assert privacy_manager.mode == PrivacyMode.LOCAL_ONLY

    # Ensure cloud calls raise immediate error
    with pytest.raises(PrivacyAuthorizationError):
        privacy_manager.assert_provider_permitted("gemini")

    # Reset back to HYBRID
    privacy_manager.set_mode(PrivacyMode.HYBRID)


@pytest.mark.asyncio
async def test_e2e_autopilot_execution_gate_workflow():
    """Verify AutoPilot structured plan and execution security gates."""
    plan = AutoPilotEngine.generate_plan("Remediate buffer overflow", "proj-meter-12")
    assert plan.status == "plan_generated"
    assert len(plan.steps) == 5

    # Check gated steps
    gated_steps = [s for s in plan.steps if s.requires_approval]
    assert len(gated_steps) == 3  # modify, verify, commit require approval

