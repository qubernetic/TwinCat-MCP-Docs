# Build

### check_objects

Runs the IEC syntax check on a PLC project without a full build — much faster, ideal
for the edit-check loop while writing ST code. Returns errors and warnings like
`get_errors`. Use `build` before activation.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | e.g. `TIPC^Plc`. Auto-discovered if omitted. |
| `severity` | `Error`, `Warning` or `Message`. |
| `limit` | Max messages. |

### build

Builds the TwinCAT solution.

### get_errors

Returns the Error List after a build.

| Parameter | Description |
|-----------|-------------|
| `severity` | `Error`, `Warning` or `Message`. |
| `projectFilter` | Keep only entries whose project name contains this text. |
| `limit` | Max entries. |

### save_solution

Saves the solution.
