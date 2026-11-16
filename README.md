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
fails. You can still open a pull request with content changes: CI builds the
site and checks it. On a pull request from a fork only the workflow rules run,
because forks get no access to the theme, and a maintainer builds the change.

The submodule is set to `update = none`, so `git clone --recurse-submodules`
succeeds and leaves `brand/` empty. With access to the brand repository, fetch
it explicitly:

```bash
git clone https://github.com/qubernetic/TwinCat-MCP-Docs.git
cd TwinCat-MCP-Docs
git submodule update --init --checkout brand
```

Then serve or build the site with [uv](https://docs.astral.sh/uv/):

```bash
uv run --with-requirements requirements.txt mkdocs serve           # live preview at http://127.0.0.1:8000
uv run --with-requirements requirements.txt mkdocs build --strict  # the CI build; must pass
```

Or in a virtual environment:

```bash
python -m venv .venv
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
├── CNAME                      # custom domain (docs.twincatmcp.qubernetic.com)
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
- Keep `mkdocs build --strict` green — broken links and nav fail the build (and the deploy).

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
