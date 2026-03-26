from __future__ import annotations

from aetheros.events import ExecutionPlan, PlannedStep, TimelineLevel


def _google_design_plan(command: str) -> ExecutionPlan:
    return ExecutionPlan(
        command=command,
        assistant_reply=(
            "Understood. I will run a transparent web research flow for futuristic OS design ideas "
            "and show each visible action in real time."
        ),
        steps=[
            PlannedStep(
                id="plan-01",
                title="Validate request",
                detail="Parsed intent and confirmed target: Google search for futuristic OS design ideas.",
                progress_start=4,
                progress_end=12,
                activity_action="Analyze",
                activity_target="Command",
                delay_ms=400,
            ),
            PlannedStep(
                id="plan-02",
                title="Prepare visible execution",
                detail="Creating an explicit on-screen action sequence with no hidden operations.",
                progress_start=12,
                progress_end=20,
                activity_action="Plan",
                activity_target="Execution timeline",
            ),
            PlannedStep(
                id="plan-03",
                title="Open browser surface",
                detail="Simulating browser launch in prototype mode and focusing search field.",
                progress_start=20,
                progress_end=34,
                activity_action="Open",
                activity_target="Browser",
                level=TimelineLevel.SUCCESS,
            ),
            PlannedStep(
                id="plan-04",
                title="Compose query",
                detail="Typing query: futuristic OS design ideas.",
                progress_start=34,
                progress_end=48,
                activity_action="Type",
                activity_target="Search field",
            ),
            PlannedStep(
                id="plan-05",
                title="Submit search",
                detail="Sending Enter and waiting for search results page render.",
                progress_start=48,
                progress_end=66,
                activity_action="Submit",
                activity_target="Google",
            ),
            PlannedStep(
                id="plan-06",
                title="Scan top design references",
                detail="Reviewing first result cluster for design inspiration themes and visual patterns.",
                progress_start=66,
                progress_end=82,
                activity_action="Inspect",
                activity_target="Top results",
                level=TimelineLevel.SUCCESS,
            ),
            PlannedStep(
                id="plan-07",
                title="Summarize findings",
                detail="Drafting visible summary: glass hierarchy, calm cyan accents, radial workflows, and transparent AI feedback.",
                progress_start=82,
                progress_end=100,
                activity_action="Summarize",
                activity_target="Assistant response",
                level=TimelineLevel.SUCCESS,
            ),
        ],
    )


def default_plan(command: str) -> ExecutionPlan:
    return ExecutionPlan(
        command=command,
        assistant_reply=(
            "I can execute that in prototype mode with full visible status and timeline updates."
        ),
        steps=[
            PlannedStep(
                id="generic-01",
                title="Interpret command",
                detail="Extracting intent and preparing action sequence.",
                progress_start=6,
                progress_end=28,
                activity_action="Analyze",
                activity_target="Command",
            ),
            PlannedStep(
                id="generic-02",
                title="Execute visible actions",
                detail="Running simulated steps with transparent progress updates.",
                progress_start=28,
                progress_end=78,
                activity_action="Act",
                activity_target="Prototype surface",
            ),
            PlannedStep(
                id="generic-03",
                title="Report completion",
                detail="Publishing results and returning assistant to ready state.",
                progress_start=78,
                progress_end=100,
                activity_action="Report",
                activity_target="Assistant panel",
                level=TimelineLevel.SUCCESS,
            ),
        ],
    )


def build_plan(command: str) -> ExecutionPlan:
    normalized = command.lower().strip()
    if "search google for futuristic os design ideas" in normalized:
        return _google_design_plan(command)
    return default_plan(command)
