// Download buttons: fill in the latest version from the signed update feed.
// Without JavaScript, or if the feed cannot be read, the buttons keep their
// href to https://get.twincatmcp.qubernetic.com/download/, which forwards to
// the latest MSI.
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

  function info(el, f) {
    el.textContent = "";
    el.appendChild(document.createTextNode("Version " + f.version + ". SHA-256: "));
    var code = document.createElement("code");
    code.textContent = f.sha256;
    el.appendChild(code);
    if (typeof f.releaseNotes === "string" && f.releaseNotes.indexOf(RELEASE_PREFIX) === 0) {
      el.appendChild(document.createTextNode(". "));
      var a = document.createElement("a");
      a.href = f.releaseNotes;
      a.textContent = "Release notes";
      el.appendChild(a);
    }
  }

  function render() {
    var buttons = document.querySelectorAll("a.tcmcp-download");
    var infos = document.querySelectorAll(".tcmcp-download-info");
    if (!buttons.length && !infos.length) return;
    load().then(function (f) {
      if (!valid(f)) return;
      buttons.forEach(function (a) {
        a.href = f.url;
        a.textContent = "Download TwinCat-MCP " + f.version;
      });
      infos.forEach(function (el) { info(el, f); });
    }).catch(function () { /* keep the /download/ fallback */ });
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(render);   // Material instant navigation
  } else {
    document.addEventListener("DOMContentLoaded", render);
  }
})();
