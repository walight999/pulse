// Perplexity web session capture (count searches + answers).

(() => {
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const resp = await origFetch.apply(this, args);
    try {
      const url = typeof args[0] === "string" ? args[0] : args[0]?.url;
      if (url && url.includes("/rest/sse/perplexity_ask")) {
        chrome.runtime.sendMessage({
          type: "pulse:capture",
          event: {
            provider: "perplexity",
            model: "perplexity-web",
            timestamp: new Date().toISOString(),
          },
        });
      }
    } catch {}
    return resp;
  };
})();
