async function refresh() {
  const { pulse_pending_events: buf = [] } = await chrome.storage.local.get("pulse_pending_events");
  document.getElementById("stats").innerHTML = `
    <div class="row"><span>Buffered events</span><strong>${buf.length}</strong></div>
    <div class="row"><span>Providers</span><strong>${countProviders(buf)}</strong></div>
  `;
}

function countProviders(buf) {
  const s = new Set(buf.map((e) => e.provider));
  return s.size;
}

document.getElementById("flush").addEventListener("click", async () => {
  document.getElementById("status").textContent = "Syncing...";
  const r = await chrome.runtime.sendMessage({ type: "pulse:flush" });
  if (r.ok) {
    document.getElementById("status").innerHTML = `<span class="ok">Sent ${r.sent} events</span>`;
  } else {
    document.getElementById("status").innerHTML = `<span class="err">Desktop offline — kept ${r.buffered} buffered</span>`;
  }
  refresh();
});

refresh();
