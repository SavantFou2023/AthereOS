# AetherOS Prototype

AetherOS is a **Windows-first local prototype** of a futuristic desktop-like environment with a **fully visible AI assistant**.

## Principles

- Assistant actions are never hidden.
- Every command emits visible status updates (`idle`, `listening`, `thinking`, `acting`, `done`, `error`).
- Every execution appears in both a timeline and activity log.
- A visible assistant cursor is always present.

## Stack

- Frontend: HTML + CSS + vanilla JavaScript
- Backend: Python + FastAPI
- Realtime transport: WebSocket

## Features

- Premium glass UI with deep-blue/cyan palette.
- Top-left launcher dropdown with live app filtering.
- Central circular hub surface.
- Bottom-right quarter-circle dock for opened apps.
- Bottom sheet panel with animated collapse/expand.
- Right assistant panel with:
  - chat bubbles
  - status chips
  - execution timeline cards
  - activity log
- Detailed demo sequence for:
  - `Search Google for futuristic OS design ideas`

## Project structure

```text
AthereOS/
├── backend/
│   ├── aetheros/
│   │   ├── events.py
│   │   ├── executor.py
│   │   └── planner.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
└── README.md
```

## Run locally (Windows)

### 1) Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2) Frontend

No separate frontend server is required. Open:

- http://127.0.0.1:8000

The backend serves the static frontend and WebSocket endpoint.

## Quick demo flow

1. Open AetherOS in browser.
2. Run: `Search Google for futuristic OS design ideas`
3. Observe visible transitions:
   - status chip updates
   - chat explanation
   - timeline progress cards
   - activity log entries

## Extend next

- Hook planner/executor to real browser automation.
- Add Windows app launcher adapters.
- Add real voice input/output pipeline.
