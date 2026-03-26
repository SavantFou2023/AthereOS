from __future__ import annotations

import asyncio
from typing import AsyncIterator, Dict

from aetheros.events import (
    ActivityPayload,
    AssistantState,
    ChatPayload,
    ExecutionPlan,
    OutgoingEvent,
    StatusPayload,
    TimelinePayload,
)


def _event(event_type: str, payload: Dict) -> OutgoingEvent:
    return OutgoingEvent(type=event_type, payload=payload)


async def run_plan(plan: ExecutionPlan) -> AsyncIterator[OutgoingEvent]:
    yield _event(
        "assistant.status",
        StatusPayload(
            state=AssistantState.LISTENING,
            label="Listening",
            detail="Command captured from launcher input.",
        ).model_dump(),
    )

    await asyncio.sleep(0.25)
    yield _event(
        "assistant.chat",
        ChatPayload(role="assistant", text=plan.assistant_reply).model_dump(),
    )

    yield _event(
        "assistant.status",
        StatusPayload(
            state=AssistantState.THINKING,
            label="Thinking",
            detail="Building transparent execution plan.",
        ).model_dump(),
    )

    await asyncio.sleep(0.35)
    yield _event(
        "assistant.status",
        StatusPayload(
            state=AssistantState.ACTING,
            label="Acting",
            detail="Running visible step-by-step actions.",
        ).model_dump(),
    )

    for step in plan.steps:
        yield _event(
            "assistant.timeline",
            TimelinePayload(
                id=step.id,
                title=step.title,
                detail=step.detail,
                progress=step.progress_end,
                level=step.level,
                meta={"range": [step.progress_start, step.progress_end]},
            ).model_dump(),
        )
        yield _event(
            "assistant.activity",
            ActivityPayload(
                action=step.activity_action,
                target=step.activity_target,
                summary=step.detail,
                visible=True,
            ).model_dump(),
        )
        await asyncio.sleep(step.delay_ms / 1000)

    yield _event(
        "assistant.chat",
        ChatPayload(
            role="assistant",
            text=(
                "Visible execution complete. I shared each action on the timeline and activity log, "
                "and no hidden automation was performed."
            ),
        ).model_dump(),
    )
    yield _event(
        "assistant.status",
        StatusPayload(
            state=AssistantState.DONE,
            label="Done",
            detail="Execution finished and trace is available.",
        ).model_dump(),
    )

    await asyncio.sleep(0.7)
    yield _event(
        "assistant.status",
        StatusPayload(state=AssistantState.IDLE, label="Idle", detail="Ready for next command.").model_dump(),
    )
