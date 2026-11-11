# Libraries

`plcProjectPath` is the PLC project path, e.g. `TIPC^Plc^Plc Project`.

### list_libraries

Lists the library references of a PLC project.

### search_libraries

Searches the local library repository — use it after `install_library` to find the
exact name, version and distributor for `add_library`.

| Parameter | Description |
|-----------|-------------|
| `namePattern` | Wildcards allowed, e.g. `*TcoCore*`. |
| `distributor` | Exact distributor name. |

### add_library

Adds a library reference to a PLC project.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | PLC project path. |
| `name` | e.g. `Tc2_Standard`. |
| `version` | e.g. `3.3.3.0`. |
| `distributor` | e.g. `Beckhoff Automation GmbH`. |

### remove_library

Removes a library reference.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | PLC project path. |
| `name` | Library name. |

### install_library

Installs a `.library` file into the library repository.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | PLC project path. |
| `filePath` | Absolute path to the `.library` file. |
| `overwrite` | Overwrite if already installed (default `false`). |
| `category` | Repository category (default `System`). |

### uninstall_library

Removes a library from the repository.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | PLC project path. |
| `name`, `version`, `distributor` | Library identity; `version` may be `*`. |
| `category` | Repository category (default `System`). |
