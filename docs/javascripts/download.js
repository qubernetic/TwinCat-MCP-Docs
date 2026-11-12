// Download block: fill in the latest version from the signed update feed.
// Without JavaScript, or if the feed cannot be read, the button keeps its
// href to https://get.twincatmcp.qubernetic.com/download/, which forwards to
// the latest MSI. The links under the button are static.
(function () {
  var FEED = "https://get.twincatmcp.qubernetic.com/latest.json";
  var ASSET_PREFIX = "https://github.com/qubernetic/TwinCat-MCP-Dist/releases/download/";
  var pending = null;

  function load() {
    if (!pending) {
      pending = fetch(FEED, { cache: "no-cache" }).then(function (r) {
        if (!r.ok) throw new Error("feed " + r.status);
        return r.json();
      });
      pending.catch(function () { pending = null; });
    }
    return pending;
  }

  function valid(f) {
    return f && typeof f.version === "string" && /^[0-9A-Za-z.+-]{1,40}$/.test(f.version) &&
      typeof f.url === "string" && f.url.indexOf(ASSET_PREFIX) === 0 &&
      typeof f.sha256 === "string" && /^[0-9a-f]{64}$/.test(f.sha256);
  }

  function render() {
    var blocks = document.querySelectorAll(".tcmcp-download");
    if (!blocks.length) return;
    load().then(function (f) {
      if (!valid(f)) return;
      blocks.forEach(function (block) {
        var button = block.querySelector("a.tcmcp-download-button");
        if (button) {
          button.href = f.url;
          button.textContent = "Download TwinCat-MCP " + f.version;
        }
        var sha = block.querySelector(".tcmcp-download-sha");
        if (sha) {
          sha.textContent = "SHA-256 ";
          var code = document.createElement("code");
          code.textContent = f.sha256;
          sha.appendChild(code);
        }
      });
    }).catch(function () { /* keep the /download/ fallback */ });
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(render);   // Material instant navigation
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
