# TwinCat-MCP — Documentation

[![Deploy docs](https://github.com/qubernetic/TwinCat-MCP-Docs/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/qubernetic/TwinCat-MCP-Docs/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-live-22A8E0)](https://docs.twincatmcp.qubernetic.com)
[![License](https://img.shields.io/badge/license-proprietary-lightgrey)](LICENSE)

Source for the **public user documentation** of [TwinCat-MCP](https://docs.twincatmcp.qubernetic.com) — an MCP server for TwinCAT 3 PLC development that lets AI coding agents (Claude Code, GitHub Copilot CLI, Cursor) build, configure, deploy, and debug TwinCAT PLC projects through a standard tool interface.

> 📖 **Live site: [docs.twincatmcp.qubernetic.com](https://docs.twincatmcp.qubernetic.com)**

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). This repository holds the documentation content only; the product itself lives in a separate private repository.

## Local development

Requires Python 3.x. Use a virtual environment to match the pinned build:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

mkdocs serve                       # live preview at http://127.0.0.1:8000
mkdocs build --strict              # production build (must pass — CI gate)
```

> The social-card plugin needs the Cairo graphics libraries. On Debian/Ubuntu:
> `sudo apt-get install libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev`

## Repository layout

```
mkdocs.yml                     # site config: theme, nav, plugins, brand
requirements.txt               # pinned mkdocs-material + plugins
docs/
├── index.md                   # landing / showcase
├── CNAME                      # custom domain (docs.twincatmcp.qubernetic.com)
├── assets/                    # logo (light/dark), favicon
├── stylesheets/extra.css      # brand accent + dark-mode logo swap
├── getting-started/           # installation, agent connection, configuration
├── licensing/                 # user-facing licensing how-to
├── tools/overview.md          # tools overview
└── changelog.md               # public changelog
.github/workflows/deploy-docs.yml   # build + deploy to GitHub Pages
SECURITY.md · CODE_OF_CONDUCT.md · LICENSE
```

## How it deploys

Every push to `main` runs the [deploy workflow](.github/workflows/deploy-docs.yml):
it builds the site with `mkdocs gh-deploy --force` (strict mode) and publishes to
the `gh-pages` branch, which GitHub Pages serves at the custom domain. The
`docs/CNAME` file preserves `docs.twincatmcp.qubernetic.com` across deploys.

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
