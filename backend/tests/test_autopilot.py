"""SAFECODIUM — Tests for SAFECODIUM AutoPilot and Permission Gates."""

import pytest
from backend.app.services.autopilot.engine import AutoPilotEngine, AutoPilotPlan


def test_autopilot_plan_generation():
    """Verify AutoPilot generates a 5-step gated plan with explicit approval requirements."""
    plan = AutoPilotEngine.generate_plan(
        user_request="Detect and repair memory buffer vulnerabilities in telemetry sensor",
        project_id="proj-smart-meter-01",
    )

    assert plan.plan_id != ""
    assert len(plan.steps) == 5
    assert plan.status == "plan_generated"

    # Read/Inspect step does not require approval
    step1 = plan.steps[0]
    assert step1.requires_approval is False

    # Modify and Verify steps must require approval
    modify_step = next(s for s in plan.steps if s.action_type == "modify_file")
    assert modify_step.requires_approval is True

    verify_step = next(s for s in plan.steps if s.action_type == "verify")
    assert verify_step.requires_approval is True


def test_autopilot_step_approval_gate():
    """Verify that sensitive steps transition to approved state upon explicit authorization."""
    plan = AutoPilotEngine.generate_plan("Audit project", "proj-01")
    step3 = plan.steps[2]
    assert step3.status == "pending"

    updated_plan = AutoPilotEngine.approve_step(plan, step_id=3)
    assert updated_plan.steps[2].status == "approved"

