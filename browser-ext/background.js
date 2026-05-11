// Pulse browser extension — background service worker
//
// Receives session-capture events from content scripts on chat.openai.com,
// claude.ai, gemini, perplexity. Buffers locally then POSTs to Pulse local
// API (http://localhost:8000/v1/token_usage/ingest) when desktop is running.
//
// Privacy: content scripts only capture metadata (message count, model name,
// approximate token count from char-length / 4, timestamp). Never message text.

const INGEST_URL = "http://localhost:8000/v1/ingest/web-session";
const WS_URL = "ws://localhost:8000/v1/ws/ingest";
const BUFFER_KEY = "pulse_pending_events";
const SYNC_INTERVAL_MIN = 5;

// Persistent WebSocket — re-connect on failure with exponential backoff
let ws = null;
let wsReconnectMs = 1000;
const wsReconnectMax = 60000;

function tryConnectWs() {
  if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
    return;
  }
  try {
    ws = new WebSocket(WS_URL);
    ws.onopen = () => {
      wsReconnectMs = 1000;  // reset backoff on successful connect
      flushBufferOverWs();   // drain any HTTP-bound buffer immediately
    };
    ws.onmessage = (e) => {
      // Server echoed an ingest receipt — could surface in popup
    };
    ws.onclose = () => {
      ws = null;
      setTimeout(tryConnectWs, wsReconnectMs);
      wsReconnectMs = Math.min(wsReconnectMs * 2, wsReconnectMax);
    };
    ws.onerror = () => { /* will trigger onclose */ };
  } catch (e) {
    // Desktop not running — silently retry later via alarm
  }
}

async function flushBufferOverWs() {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  const { [BUFFER_KEY]: buffer = [] } = await chrome.storage.local.get(BUFFER_KEY);
  if (!buffer.length) return;
  try {
    ws.send(JSON.stringify({ events: buffer }));
    await chrome.storage.local.set({ [BUFFER_KEY]: [] });
  } catch {}
}

chrome.runtime.onInstalled.addListener(async () => {
  await chrome.alarms.create("pulse-sync", {
    delayInMinutes: 1,
    periodInMinutes: SYNC_INTERVAL_MIN,
  });
  // Kick off WebSocket connection attempt right away
  tryConnectWs();
});
chrome.runtime.onStartup?.addListener(tryConnectWs);

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === "pulse:capture") {
    enqueueEvent(msg.event).then(() => sendResponse({ ok: true }));
    return true;  // async
  }
  if (msg?.type === "pulse:flush") {
    flushBuffer().then((r) => sendResponse(r));
    return true;
  }
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "pulse-sync") flushBuffer();
});

async function enqueueEvent(event) {
  const enriched = { ...event, captured_at: new Date().toISOString() };

  // Try WebSocket real-time push first
  if (ws && ws.readyState === WebSocket.OPEN) {
    try {
      ws.send(JSON.stringify({ events: [enriched] }));
      return;   // success — no need to buffer
    } catch {}
  }

  // Fallback: append to HTTP buffer (flushed every 5min by alarm)
  const { [BUFFER_KEY]: buffer = [] } = await chrome.storage.local.get(BUFFER_KEY);
  buffer.push(enriched);
  if (buffer.length > 1000) buffer.splice(0, buffer.length - 1000);
  await chrome.storage.local.set({ [BUFFER_KEY]: buffer });

  // Trigger reconnect attempt in case desktop just came back online
  tryConnectWs();
}

async function flushBuffer() {
  const { [BUFFER_KEY]: buffer = [] } = await chrome.storage.local.get(BUFFER_KEY);
  if (!buffer.length) return { ok: true, sent: 0 };
  try {
    const resp = await fetch(INGEST_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ events: buffer, source: "browser-ext-v0.1" }),
    });
    if (!resp.ok) throw new Error(`status ${resp.status}`);
    await chrome.storage.local.set({ [BUFFER_KEY]: [] });
    return { ok: true, sent: buffer.length };
  } catch (e) {
    // Desktop not running — keep buffer, try again next interval
    return { ok: false, error: e.message, buffered: buffer.length };
  }
}
