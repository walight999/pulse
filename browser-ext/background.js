// Pulse browser extension — background service worker
//
// Receives session-capture events from content scripts on chat.openai.com,
// claude.ai, gemini, perplexity. Buffers locally then POSTs to Pulse local
// API (http://localhost:8000/v1/token_usage/ingest) when desktop is running.
//
// Privacy: content scripts only capture metadata (message count, model name,
// approximate token count from char-length / 4, timestamp). Never message text.

const INGEST_URL = "http://localhost:8000/v1/ingest/web-session";
const BUFFER_KEY = "pulse_pending_events";
const SYNC_INTERVAL_MIN = 5;

chrome.runtime.onInstalled.addListener(async () => {
  await chrome.alarms.create("pulse-sync", {
    delayInMinutes: 1,
    periodInMinutes: SYNC_INTERVAL_MIN,
  });
});

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
  const { [BUFFER_KEY]: buffer = [] } = await chrome.storage.local.get(BUFFER_KEY);
  buffer.push({
    ...event,
    captured_at: new Date().toISOString(),
  });
  // Cap buffer at 1000 events to avoid runaway memory if desktop offline
  if (buffer.length > 1000) buffer.splice(0, buffer.length - 1000);
  await chrome.storage.local.set({ [BUFFER_KEY]: buffer });
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
