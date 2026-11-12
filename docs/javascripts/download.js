// Download block: fill in the latest version from the signed update feed.
// Without JavaScript, or if the feed cannot be read, the button keeps its
// href to https://get.twincatmcp.qubernetic.com/download/, which forwards to
// the latest MSI, and the static "All versions" link stays.
(function () {
  var FEED = "https://get.twincatmcp.qubernetic.com/latest.json";
  var ASSET_PREFIX = "https://github.com/qubernetic/TwinCat-MCP-Dist/releases/download/";
  var RELEASE_PREFIX = "https://github.com/qubernetic/TwinCat-MCP-Dist/releases/";
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

  function link(href, text) {
    var a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    return a;
  }

  // "Windows installer (MSI) · Release notes · All versions"
  function addReleaseNotes(meta, f) {
    if (meta.querySelector("a.tcmcp-release-notes")) return;
    if (typeof f.releaseNotes !== "string" || f.releaseNotes.indexOf(RELEASE_PREFIX) !== 0) return;
    var a = link(f.releaseNotes, "Release notes");
    a.className = "tcmcp-release-notes";
    var all = meta.querySelector("a");   // the static "All versions" link
    meta.insertBefore(a, all);
    meta.insertBefore(document.createTextNode(" · "), all);
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
        var meta = block.querySelector(".tcmcp-download-meta");
        if (meta) addReleaseNotes(meta, f);
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
