"""SAFECODIUM AutoPilot — Multi-Step Autonomous Security Agent.

Protocol:
1. Inspects the project workspace.
2. Formulates a structured execution plan.
3. Enforces an explicit Permission Gate before any file modification or compilation.
4. Executes isolated changes on shadow workspaces.
5. Verifies through deterministic compilers and sanitizers.
6. Demands developer confirmation before applying verified changes to production.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from backend.app.core.logging import logger


class AutoPilotStep(BaseModel):
    step_id: int
    title: str
    description: str
    action_type: str  # read, analyze, modify_file, compile, verify, commit
    requires_approval: bool
    status: str = "pending"  # pending, approved, executing, completed, failed, rejected
    evidence: Optional[str] = None


class AutoPilotPlan(BaseModel):
    plan_id: str
    user_request: str
    steps: List[AutoPilotStep]
    status: str = "awaiting_user_approval"
    approved_by_user: bool = False


class AutoPilotEngine:
    """Multi-step security synthesis and task automation engine."""

    @classmethod
    def generate_plan(cls, user_request: str, project_id: str) -> AutoPilotPlan:
        """Analyze user goal and generate an actionable, permission-gated execution plan."""
        import uuid

        steps = [
            AutoPilotStep(
                step_id=1,
                title="Inspect Project Workspace & Language Manifests",
                description="Scan directory tree and detect languages, build systems, and dependencies.",
                action_type="read",
                requires_approval=False,
            ),
            AutoPilotStep(
                step_id=2,
                title="Run Unified Security & AST Analysis",
                description="Execute AST scanner, Gitleaks, and OSV dependency checkers.",
                action_type="analyze",
                requires_approval=False,
            ),
            AutoPilotStep(
                step_id=3,
                title="Synthesize Defensive Patch in Shadow Workspace",
                description="Generate minimal unified diff addressing identified CWE vulnerabilities.",
                action_type="modify_file",
                requires_approval=True,  # Permission Gate
            ),
            AutoPilotStep(
                step_id=4,
                title="Deterministic Compilation & Sanitizer Verification",
                description="Run headless Clang/GCC compiler and evaluate ASan/UBSan memory traps.",
                action_type="verify",
                requires_approval=True,  # Permission Gate
            ),
            AutoPilotStep(
                step_id=5,
                title="Developer Final Review & Promotion",
                description="Review unified diff before merging shadow fixes into main workspace.",
                action_type="commit",
                requires_approval=True,  # Final Approval Gate
            ),
        ]

        return AutoPilotPlan(
            plan_id=str(uuid.uuid4()),
            user_request=user_request,
            steps=steps,
            status="plan_generated",
        )

    @classmethod
    def approve_step(cls, plan: AutoPilotPlan, step_id: int) -> AutoPilotPlan:
        """User confirms execution of a sensitive step."""
        for step in plan.steps:
            if step.step_id == step_id:
                step.status = "approved"
                logger.info(f"AutoPilot Step {step_id} approved by developer.")
                break
        return plan

