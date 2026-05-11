// Claude.ai web session capture.
//
// Watches /api/organizations/.../chat_conversations/.../completion responses.
// Captures only model + approximate length, never message text.

(() => {
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const resp = await origFetch.apply(this, args);
    try {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
      if (url && url.includes("/api/organizations/") && url.includes("/completion")) {
        resp.clone().text().then((text) => {
          // SSE — parse final event for model name
          const modelMatch = text.match(/"model":"([^"]+)"/);
          chrome.runtime.sendMessage({
            type: "pulse:capture",
            event: {
              provider: "anthropic-web",
              model: modelMatch ? modelMatch[1] : "claude-unknown",
              approx_chars: text.length,
              timestamp: new Date().toISOString(),
            },
          });
        }).catch(() => {});
      }
    } catch {}
    return resp;
  };
})();
