# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0-beta.1] - 2026-11-12

TwinCat-MCP now runs as a **Windows Service** with a **TcXaeShell Plugin**,
installed from one MSI package. Agents connect over Streamable HTTP. The tool
set grows from 44 to 56 tools, and the software is licensed per machine.

!!! warning "Beta"
    The beta MSI is not code-signed yet. See
    [Installation](getting-started/installation.md#download) for how to check
    the download.

### Added
- MSI installer with two features, MCP Service and TcXaeShell Plugin: a setup wizard with the license agreement, prerequisite checks, an option to close a running TcXaeShell, and unattended installs (`ADDLOCAL`, `CLOSETCXAESHELL=1`). See [Installation](getting-started/installation.md).
- Upgrade in place that keeps settings and license; uninstall keeps `%ProgramData%\TwinCat-MCP` unless `PURGEDATA=1` is passed.
- Setup reports a taken HTTP port and the program that holds it; the Service starts on the port once it is free.
- Streamable HTTP transport: the MCP endpoint is served at `POST /mcp` on `localhost:3001` by a Windows Service. It replaces the previous stdio console app.
- TcXaeShell Plugin, to which the Service routes the project tools.
- `quit_instance`: close a TcXaeShell instance.
- `scan_io_devices`: scan I/O devices on the target.
- `scan_plc_project`: discover the PLC project tree with type labels.
- `read_item_xml` / `write_item_xml`: read and write the XML configuration of any tree node.
- `link_variables` / `unlink_variables`: create and remove I/O variable mappings.
- `get_umr_netid`: get the UserMode Runtime AMS NetId.
- `search`: fuzzy or regex search across POUs, DUTs, GVLs, symbols and hardware, including live ADS symbols.
- `project_digest`: a one-call project overview of POUs, DUTs, GVLs, libraries and tasks.
- `read_pou_batch`: read several POUs in one call.
- `check_objects`: validate configuration objects.
- `service_memory`: show the Service's memory use and limits, and release unused memory on request.
- MCP resources: `twincat://{instanceId}/tree`, `/pous`, `/libraries`.
- `dryRun` preview for the mutating tools `write_pou`, `write_item_xml`, `delete_item`, `rename_item`, `link_variables` and `unlink_variables`.
- Offline, machine-bound licensing with `get_license_status`, `generate_license_request` and `install_license`. See [Licensing](licensing/requesting-and-installing.md).
- Options window with tabbed pages: General, Safety, Connection, UMR, Licensing, Memory & Limits, Help and About, with recommended default instructions for agents.
- **Memory & Limits** page with a live memory bar, and the `BrowseSymbolsMaxNodes` and `MaxPrivateMemoryMB` settings. See [Configuration](getting-started/configuration.md#memory-limits).
- A memory guard and automatic memory release in the Service.
- Copy-reference context menu in the Plugin.
- [Standard License Agreement](legal/standard-license-agreement.md), shown by the installer, and a Trial License Agreement for evaluations.
- `THIRD-PARTY-NOTICES.txt`, installed with the software.

### Changed
- Architecture: the single console app (stdio) is replaced by a Windows Service (MCP and ADS) plus a TcXaeShell Plugin.
- The Service is self-contained; no separate .NET runtime is needed.
- Starting and stopping the UserMode Runtime moved into the Plugin: the six target-changing tools take `useUmr=true`, or need `confirmed=true` on other targets.
- Read tools gained parameters such as `fields` that limit the size of the output.
- Tool descriptions steer agents toward the `search` and file tools, which saves tokens.
- Structured, machine-readable error codes across tools.
- Reached limits are reported as notices ("Limit reached, not an error"), not as errors.

### Removed
- `attach` and `attach_by_process_id`: `launch_instance` reuses a running instance.
- `start_umr` and `stop_umr`: replaced by the `useUmr` parameter.

### Fixed
- `launch_instance` handles invalid solution paths, and starts TcXaeShell in the signed-in user's session.
- `create_pou` creates interface methods, properties and their accessors with the correct types.
- PLC compile errors are reported as errors and fail `build`.
- `browse_symbols` and symbol `search` no longer walk the whole symbol tree, which caused very high Service memory use. `maxDepth` now defaults to 2, with new `maxNodes` and `followPointers` parameters.
- Lower Service memory use under load.
- The Options window scrolls with the mouse wheel.

### Security
- The UserMode Runtime and all tools require a valid license; only the three licensing tools work without one.
- Only SYSTEM and administrators can change the license folder.

## [0.1.0-beta.1] - 2026-02-23

First beta release with 44 MCP tools covering the full TwinCAT PLC development lifecycle.

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
