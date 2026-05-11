// Gemini / Google AI Studio web session capture.
//
// Watches StreamGenerateContent endpoint. Metadata only.

(() => {
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const resp = await origFetch.apply(this, args);
    try {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
      if (url && (url.includes("StreamGenerate") || url.includes("generateContent"))) {
        chrome.runtime.sendMessage({
          type: "pulse:capture",
          event: {
            provider: "google-gemini-web",
            model: "gemini-web",
            timestamp: new Date().toISOString(),
          },
        });
      }
    } catch {}
    return resp;
  };
})();
