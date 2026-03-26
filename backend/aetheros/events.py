from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class AssistantState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    ACTING = "acting"
    DONE = "done"
    ERROR = "error"


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TimelineLevel(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class WSIncoming(BaseModel):
    type: Literal["user.command"]
    command: str = Field(min_length=1)


class EventBase(BaseModel):
    type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StatusPayload(BaseModel):
    state: AssistantState
    label: str
    detail: Optional[str] = None


class ChatPayload(BaseModel):
    role: ChatRole
    text: str


class TimelinePayload(BaseModel):
    id: str
    title: str
    detail: str
    level: TimelineLevel = TimelineLevel.INFO
    progress: int = Field(ge=0, le=100)
    meta: Dict[str, Any] = Field(default_factory=dict)


class ActivityPayload(BaseModel):
    action: str
    target: str
    summary: str
    visible: bool = True


class OutgoingEvent(EventBase):
    payload: Dict[str, Any]


class PlannedStep(BaseModel):
    id: str
    title: str
    detail: str
    progress_start: int
    progress_end: int
    delay_ms: int = 550
    activity_action: str
    activity_target: str
    level: TimelineLevel = TimelineLevel.INFO


class ExecutionPlan(BaseModel):
    command: str
    assistant_reply: str
    steps: List[PlannedStep]
