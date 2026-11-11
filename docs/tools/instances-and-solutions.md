# Instances & Solutions

## Instances

### list_instances

Lists running TcXaeShell and Visual Studio instances with their plugin connection
status. Always available.

### launch_instance

Starts TcXaeShell (or reuses a running one), optionally opens a solution, and waits
until the plugin has connected. **Call this before any TcXaeShell-based tool.**
Always available.

| Parameter | Description |
|-----------|-------------|
| `solutionPath` | Full path to the `.sln` file. Omit to start an empty instance. |
| `visible` | Show the TcXaeShell window (default `true`). |

!!! note
    The solution path must be visible to the TwinCat-MCP Windows service — use a
    local path, not a drive letter mapped only in your user session. Over Remote
    Desktop, see [Known limitations](../guides/troubleshooting.md#known-limitations).

### quit_instance

Gracefully closes a TcXaeShell instance.

| Parameter | Description |
|-----------|-------------|
| `save` | Save the solution before quitting (default `true`). |

## Solutions and projects

### new_solution

Creates a new, empty TwinCAT solution.

| Parameter | Description |
|-----------|-------------|
| `solutionDir` | Directory for the new solution. |
| `solutionName` | Solution name, without `.sln`. |

### create_twincat_project

Adds a TwinCAT XAE project to the current solution.

| Parameter | Description |
|-----------|-------------|
| `name` | TwinCAT project name. |

### create_plc_project

Adds a PLC project to the current solution.

| Parameter | Description |
|-----------|-------------|
| `name` | PLC project name. |
| `template` | PLC template (default `Standard PLC Template`). |

### close_solution

Closes the current solution.

| Parameter | Description |
|-----------|-------------|
| `save` | Save before closing (default `true`). |
