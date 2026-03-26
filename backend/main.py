from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from aetheros.events import ChatPayload, WSIncoming
from aetheros.executor import run_plan
from aetheros.planner import build_plan

app = FastAPI(title="AetherOS Prototype API")

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


@app.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.websocket("/ws")
async def ws_assistant(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_json()
            incoming = WSIncoming.model_validate(raw)
            await websocket.send_json(
                {
                    "type": "assistant.chat",
                    "payload": ChatPayload(role="user", text=incoming.command).model_dump(),
                }
            )
            plan = build_plan(incoming.command)
            async for event in run_plan(plan):
                await websocket.send_json(event.model_dump())
    except WebSocketDisconnect:
        return
    except Exception as exc:  # keeps socket resilient in prototype mode
        await websocket.send_json(
            {
                "type": "assistant.status",
                "payload": {
                    "state": "error",
                    "label": "Error",
                    "detail": f"Unexpected server issue: {exc}",
                },
            }
        )
        await websocket.close()
