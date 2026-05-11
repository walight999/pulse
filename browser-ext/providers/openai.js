// OpenAI / ChatGPT web session capture.
//
// Watches network responses for /backend-api/conversation requests and
// extracts metadata (model, token count, timestamp). Never reads message text.

(() => {
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const resp = await origFetch.apply(this, args);
    try {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
      if (url && url.includes("/backend-api/conversation")) {
        // Don't await body — clone + handle async
        resp.clone().json().then((data) => {
          if (data?.message?.metadata) {
            chrome.runtime.sendMessage({
              type: "pulse:capture",
              event: {
                provider: "openai",
                model: data.message.metadata.model_slug || "unknown",
                conversation_id: data.conversation_id || null,
                message_id: data.message.id || null,
                // Approximate from response text length (no actual content stored)
                approx_chars: (data.message.content?.parts || []).join("").length,
                timestamp: new Date().toISOString(),
              },
            });
          }
        }).catch(() => {});
      }
    } catch {}
    return resp;
  };
})();
