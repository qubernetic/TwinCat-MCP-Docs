# Changelog

All notable changes to the TwinCat-MCP documentation site are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/), and the site uses
[Semantic Versioning](https://semver.org/) independently of the product version.
The product's own changelog is published at [docs/changelog.md](docs/changelog.md).

## [1.2.2] - 2026-11-12

### Fixed
- Release notes under the Download button opens the docs changelog instead of the GitHub release page (#23)

## [1.2.1] - 2026-11-12

### Fixed
- Download block: the version, SHA-256 and links sit on their own lines under the button instead of next to it; the redundant paragraph is gone (#18)

## [1.2.0] - 2026-11-12

### Added
- Download button on the home and installation pages. It always gets the latest MSI through https://get.twincatmcp.qubernetic.com/download/ and shows the version, the SHA-256 and the release notes link from the update feed (#13)

## [1.1.0] - 2026-11-12

Documentation for TwinCat-MCP 0.2.0-beta.1.

### Added
- Installation: MSI download from TwinCat-MCP-Dist with the checksum check, features, the TcXaeShell dialog, unattended install, file locations, busy port, upgrade and uninstall (#8)
- Licensing: trial and full licenses, where the license files live (#8)
- Legal: overview page and the Standard License Agreement (#8)
- Release notes for 0.2.0-beta.1 (#8)
- Configuration: Memory & Limits page, `BrowseSymbolsMaxNodes` and `MaxPrivateMemoryMB`; bounded `browse_symbols` and limit notices in the tool reference and troubleshooting (#6)

### Fixed
- The license request path is in the `license` subfolder (#8)
- The installation page no longer promises a signed MSI; the beta is unsigned (#8)

## [1.0.0] - 2026-11-11

### Added
- Full tool reference: 55 tools in ten category pages with parameters and behaviour notes, shared conventions and resources (#1)
- Guides: How to Use, Best Practices, Safety, Troubleshooting (#1)
- Object-oriented code rules for `create_pou` (interface members, accessors, `implementsInterfaces`) (#1)

### Changed
- Agent Connection: register the Claude Code server with `--scope user` (#1)
- Landing page and navigation link the guides and the tool reference (#1)

### Initial site
- MkDocs Material site with getting started, licensing, tools overview stub and changelog, deployed to GitHub Pages
