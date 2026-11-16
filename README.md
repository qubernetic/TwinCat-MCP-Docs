# TwinCat-MCP — Documentation

[![Deploy docs](https://github.com/qubernetic/TwinCat-MCP-Docs/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/qubernetic/TwinCat-MCP-Docs/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-live-22A8E0)](https://docs.twincatmcp.qubernetic.com)
[![License](https://img.shields.io/badge/license-proprietary-lightgrey)](LICENSE)

Source for the **public user documentation** of [TwinCat-MCP](https://docs.twincatmcp.qubernetic.com) — an MCP server for TwinCAT 3 PLC development that lets AI coding agents (Claude Code, GitHub Copilot CLI, Cursor) build, configure, deploy, and debug TwinCAT PLC projects through a standard tool interface.

> 📖 **Live site: [docs.twincatmcp.qubernetic.com](https://docs.twincatmcp.qubernetic.com)**

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). This repository holds the documentation content only; the product itself lives in a separate private repository.

## Local development

The theme, logo and fonts come from the Qubernetic brand package, a private
git submodule at `brand/`. Without access to it a local build of the site
fails. Content changes are still welcome as pull requests. CI builds and checks
a pull request from a branch of this repository. A pull request from a fork
runs only the workflow rules, because forks get no access to the theme, and a
maintainer builds it before merging.

The submodule is set to `update = none`, so `git clone --recurse-submodules`
succeeds and leaves `brand/` empty. With access to the brand repository, fetch
it explicitly:

```bash
git clone https://github.com/qubernetic/TwinCat-MCP-Docs.git
cd TwinCat-MCP-Docs
git submodule update --init --checkout brand
```

`update = none` applies to later updates as well. After the `brand` pin
changes (a pull, or switching branches), run
`git submodule update --checkout brand` again, or you keep building with the
old theme.

The lock targets Python 3.12. Serve or build the site with
[uv](https://docs.astral.sh/uv/):

```bash
uv run --python 3.12 --with-requirements requirements.txt mkdocs serve           # live preview at http://127.0.0.1:8000
uv run --python 3.12 --with-requirements requirements.txt mkdocs build --strict  # the CI build; must pass
```

Or in a virtual environment with Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --require-hashes -r requirements.txt
mkdocs serve
```

> The social-card plugin loads the Cairo library (`libcairo.so.2` on Linux).
> If your system lacks it, install it, for example `sudo apt-get install libcairo2` on Debian/Ubuntu.

## Repository layout

```
mkdocs.yml                     # site config: theme, nav, plugins
brand/                         # git submodule: Qubernetic brand package (theme in brand/mkdocs/material)
requirements.in                # direct dependencies: mkdocs-material at the theme's version + plugins
requirements.txt               # compiled from requirements.in, pinned by hash
tests/                         # rules of the deploy workflow (pytest), with their own locked requirements
docs/
├── index.md                   # landing / showcase
├── CNAME                      # the custom domain for reference; the Pages settings hold the live value
├── stylesheets/extra.css      # the download block's own styles
├── getting-started/           # installation, agent connection, configuration
├── licensing/                 # user-facing licensing how-to
├── tools/overview.md          # tools overview
└── changelog.md               # public changelog
.github/workflows/deploy-docs.yml   # rules, build and deploy to GitHub Pages
SECURITY.md · CODE_OF_CONDUCT.md · LICENSE
```

## How it deploys

The [deploy workflow](.github/workflows/deploy-docs.yml) has three jobs:

- `rules` checks the workflow itself with `tests/test_docs_workflow.py`.
- `build` fetches the brand theme at the pinned commit with a read-only deploy
  key (the repository secret `BRAND_DEPLOY_KEY`) and runs `mkdocs build --strict`.
  On `main` it uploads the site for GitHub Pages; on pull requests and manual
  runs from other branches it uploads it as the `docs-site` artifact, which you
  can download and inspect.
- `deploy` publishes the Pages artifact, from `main` only.

`rules` and `build` run on every pull request and on every push to `main`; pull
requests from forks run `rules` only. The custom domain
`docs.twincatmcp.qubernetic.com` is set in the repository's Pages settings.

After changing `requirements.in`, regenerate the lock:

```bash
uv pip compile --generate-hashes --python-version 3.12 --python-platform x86_64-unknown-linux-gnu requirements.in -o requirements.txt
```

`mkdocs-material` stays at the version the brand theme is built for; it moves
only together with the `brand` pin.

## Contributing

- **Branching:** Gitflow — work on `feature/*`, PR into `develop`; `main` is the published site.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (`docs:`, `feat:`, `fix:`, `chore:`, …).
- CI runs `mkdocs build --strict`. A broken link or nav entry fails the build, and on `main` a failed build stops the deploy. Without access to the theme you can still run the workflow rules: `uv run --with-requirements tests/requirements.txt pytest -q tests`.

## ⚠️ This is a public repository

Only **curated, user-facing** content belongs here. Never add:

- how licensing is enforced under the hood (token issuance/validation, machine binding, replay protection);
- TwinCAT Automation-Interface implementation details or internal type names;
- internal source, samples, or planning documents;
- the name of any prior employer or third party.

When in doubt, leave it out — this content is world-readable.

## License

© 2026 Csaba Biró (Qubernetic). All rights reserved. See [LICENSE](LICENSE).
Documentation is published for use with the TwinCat-MCP product; redistribution
or derivative works require permission.

---

<sub>A <a href="https://qubernetic.com">Qubernetic</a> product — *we build the future*.</sub>
