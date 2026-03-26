const ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`);

const statusPill = document.getElementById("statusPill");
const statusLabel = document.getElementById("statusLabel");
const assistantMode = document.getElementById("assistantMode");
const chatLog = document.getElementById("chatLog");
const timeline = document.getElementById("timeline");
const activityLog = document.getElementById("activityLog");
const commandInput = document.getElementById("commandInput");
const sendBtn = document.getElementById("sendCommand");
const launcher = document.getElementById("launcher");
const launcherToggle = document.getElementById("launcherToggle");
const appSearch = document.getElementById("appSearch");
const appList = document.getElementById("appList");
const dock = document.getElementById("dock");
const sheetHandle = document.getElementById("sheetHandle");
const bottomSheet = document.getElementById("bottomSheet");
const assistantCursor = document.getElementById("assistantCursor");

const apps = [
  "Browser",
  "Console",
  "Files",
  "Terminal",
  "Design Board",
  "Settings",
  "Voice Studio",
  "AI Monitor",
  "Calendar",
];

const openApps = ["Browser", "AI", "Files", "Notes", "Terminal"];

function setStatus(state, label) {
  statusLabel.textContent = label;
  statusPill.querySelector(".dot").className = `dot ${state}`;
  assistantMode.className = `assistant-mode ${state}`;
  assistantMode.textContent = state;
}

function addBubble(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role === "user" ? "user" : "assistant"}`;
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function addTimelineCard({ title, detail, progress, level }) {
  const card = document.createElement("article");
  card.className = "timeline-card";
  if (level === "success") card.style.borderColor = "rgba(101, 211, 164, .35)";
  if (level === "warning") card.style.borderColor = "rgba(233, 191, 104, .38)";
  if (level === "error") card.style.borderColor = "rgba(239, 124, 137, .45)";

  card.innerHTML = `
    <div class="t-head"><strong>${title}</strong><span>${progress}%</span></div>
    <div class="t-detail">${detail}</div>
    <div class="progress"><span style="width:${progress}%"></span></div>
  `;

  timeline.prepend(card);
}

function addActivity({ action, target, summary }) {
  const row = document.createElement("li");
  row.innerHTML = `<strong>${action}</strong><span>${target} — ${summary}</span>`;
  activityLog.prepend(row);
}

function populateDock() {
  dock.innerHTML = "";
  openApps.forEach((name) => {
    const el = document.createElement("div");
    el.className = "dock-app";
    el.textContent = name;
    dock.appendChild(el);
  });
}

function populateLauncher(filter = "") {
  const q = filter.trim().toLowerCase();
  const filtered = apps.filter((app) => app.toLowerCase().includes(q));
  appList.innerHTML = "";

  if (filtered.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No matching app";
    empty.style.opacity = "0.75";
    appList.appendChild(empty);
    return;
  }

  filtered.forEach((app) => {
    const li = document.createElement("li");
    li.textContent = app;
    li.onclick = () => addActivity({ action: "Open", target: app, summary: "Launched from app launcher." });
    appList.appendChild(li);
  });
}

function sendCommand() {
  const command = commandInput.value.trim();
  if (!command || ws.readyState !== WebSocket.OPEN) return;

  ws.send(JSON.stringify({ type: "user.command", command }));
  commandInput.value = "";
}

ws.addEventListener("message", (msg) => {
  const event = JSON.parse(msg.data);
  const payload = event.payload || {};

  if (event.type === "assistant.status") {
    setStatus(payload.state, payload.label || payload.state);
    if (payload.detail) {
      addActivity({ action: "Status", target: payload.label, summary: payload.detail });
    }
    return;
  }

  if (event.type === "assistant.chat") {
    addBubble(payload.role, payload.text);
    return;
  }

  if (event.type === "assistant.timeline") {
    addTimelineCard(payload);
    return;
  }

  if (event.type === "assistant.activity") {
    addActivity(payload);
  }
});

sendBtn.addEventListener("click", sendCommand);
commandInput.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter") sendCommand();
});

launcherToggle.addEventListener("click", () => {
  launcher.classList.toggle("hidden");
  if (!launcher.classList.contains("hidden")) appSearch.focus();
});
appSearch.addEventListener("input", () => populateLauncher(appSearch.value));

document.addEventListener("click", (ev) => {
  if (!launcher.contains(ev.target) && ev.target !== launcherToggle) {
    launcher.classList.add("hidden");
  }
});

sheetHandle.addEventListener("click", () => bottomSheet.classList.toggle("collapsed"));

const cursorState = { x: innerWidth / 2, y: innerHeight / 2, tx: innerWidth / 2, ty: innerHeight / 2 };
document.addEventListener("mousemove", (e) => {
  cursorState.tx = e.clientX;
  cursorState.ty = e.clientY;
});

function animateCursor() {
  cursorState.x += (cursorState.tx - cursorState.x) * 0.2;
  cursorState.y += (cursorState.ty - cursorState.y) * 0.2;
  assistantCursor.style.left = `${cursorState.x}px`;
  assistantCursor.style.top = `${cursorState.y}px`;
  requestAnimationFrame(animateCursor);
}

populateLauncher();
populateDock();
bottomSheet.classList.add("collapsed");
addBubble("assistant", "AetherOS ready. All actions will remain visible in this interface.");
animateCursor();
