# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Reworked into a **Service + Plugin** architecture with a Streamable HTTP
transport, an expanded tool set, and offline licensing.

### Added
- Streamable HTTP transport — the MCP endpoint is served at `POST /mcp` on `localhost:3001` by a Windows Service (replaces the previous stdio console app).
- TcXaeShell plugin that the Service routes project-manipulation tools to.
- `quit_instance` — close a TcXaeShell instance.
- `scan_io_devices` — scan I/O devices on the target.
- `create_twincat_project` — add a TwinCAT XAE project to the solution.
- `read_item_xml` / `write_item_xml` — read and write any tree node's XML configuration.
- `link_variables` / `unlink_variables` — create and remove I/O variable mappings.
- `get_umr_netid` — get the UserMode Runtime AMS NetId.
- `search` — unified fuzzy/regex search across POUs, DUTs, GVLs, symbols, and hardware, including live ADS symbol search.
- `project_digest` — one-call project overview: POUs, DUTs, GVLs, libraries, tasks.
- `read_pou_batch` — read multiple POUs in a single call.
- `check_objects` — validate configuration objects.
- `service_memory` — show the Service's memory use and limits, and release unused memory on request.
- Options → **Memory & Limits** page with a live memory bar, and the `BrowseSymbolsMaxNodes` and `MaxPrivateMemoryMB` settings.
- Memory guard and automatic memory release in the Service.
- MCP resources — `twincat://{instanceId}/tree`, `/pous`, `/libraries`.
- `dryRun` preview mode for mutating tools (`write_pou`, `write_item_xml`, `delete_item`, `rename_item`, `link_variables`/`unlink_variables`).
- Offline, machine-bound licensing — signed `TCMCP1.…` tokens; `get_license_status`, `generate_license_request`, `install_license`.
- Plugin Options window with tabbed pages, including a Licensing page.
- Copy-reference context menu in the plugin.

### Changed
- Architecture — single console app (stdio) → Windows Service (MCP + ADS) plus a TcXaeShell plugin; the tool set expanded accordingly.
- Read tools gained token-limiting parameters (`fields`, etc.) to reduce output size.
- Tool descriptions steer agents toward the `search` and file tools to cut token usage.
- Structured, machine-readable error codes across tools.

### Fixed
- `launch_instance` handling of invalid solution paths.
- `browse_symbols` and symbol `search` no longer walk the whole symbol tree; this caused very high Service memory use. `maxDepth` now defaults to 2, with new `maxNodes` and `followPointers` parameters.
- Reached limits are reported as notices ("Limit reached, not an error"), not as errors.
- The Options window scrolls with the mouse wheel.

### Security
- License enforcement — the UserMode Runtime and all tools require a valid license; only the three licensing tools are available without one.

## [0.1.0-beta.1] - 2026-02-23

First beta release with 43 MCP tools covering the full TwinCAT PLC development lifecycle.

### Added

#### Infrastructure
- `list_instances` — list running TcXaeShell and Visual Studio instances.
- `attach` — attach to a running instance by solution name.
- `attach_by_process_id` — attach to a running instance by PID.
- `launch_instance` — start TcXaeShell, open a solution, and attach (with instance reuse).

#### Tree Navigation
- `list_tree_items` — list child items of a configuration tree node.

#### POU Management
- `create_pou` — create any IEC 61131-3 POU type (Program, Function, FB, Method, Property, DUT, GVL, Interface).
- `read_pou` — read declaration and implementation, with a recursive mode for full FB/Interface trees.
- `write_pou` — write declaration and/or implementation in a single call.
- `delete_item` — delete a child item from the configuration tree.
- `rename_item` — rename an item in the configuration tree.

#### Organization
- `create_folder` — create a folder in the configuration tree.

#### Library Management
- `list_libraries`, `add_library`, `remove_library`, `install_library`, `search_libraries`, `uninstall_library` — manage PLC library references and the local library repository.

#### Build
- `build` — build the TwinCAT solution.
- `get_errors` — get build errors from the Error List with a severity filter.

#### Solution Management
- `save_solution`, `new_solution`, `create_twincat_project`, `create_plc_project`, `close_solution` — manage solutions and projects.

#### Task Management
- `create_task`, `read_task_config`, `write_task_config`, `assign_program`, `remove_program` — manage Real-Time Configuration tasks and program assignments.

#### System Management
- `activate_configuration`, `start_restart_twincat`, `get_system_state`, `set_target_netid`, `get_target_netid`, `plc_login`, `plc_start`, `plc_stop`, `plc_logout` — manage the TwinCAT runtime and target (dangerous operations are guarded).

#### UserMode Runtime
- `start_umr` — start a UserMode Runtime for safe local testing (with AMS route registration).
- `stop_umr` — stop the running UserMode Runtime.

#### ADS Runtime
- `read_symbol`, `write_symbol`, `browse_symbols`, `assert_symbol` — read, write, browse, and assert PLC variables at runtime via ADS.

#### Safety Features
- Online modification guard — blocks POU code changes while the PLC is online.
- Target safety guards — require confirmation for dangerous operations on non-UMR targets.
- UserMode Runtime vs remote target distinction — safe operations proceed automatically on a UMR.
