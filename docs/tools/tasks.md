# Tasks

### create_task

Creates a real-time task **and** its PLC task reference, so programs can be assigned
to it.

| Parameter | Description |
|-----------|-------------|
| `name` | Task name (unique). |
| `plcProjectPath` | PLC project for the task reference, e.g. `TIPC^Plc^Plc Project`. |
| `subType` | `0` = with process image (default), `1` = without. |

### read_task_config

Reads a task's configuration (cycle time, priority, …) as XML.

| Parameter | Description |
|-----------|-------------|
| `taskPath` | e.g. `TIRT^PlcTask`. |

### write_task_config

Writes a task's configuration from XML.

| Parameter | Description |
|-----------|-------------|
| `taskPath` | e.g. `TIRT^PlcTask`. |
| `xml` | XML configuration. |

### assign_program

Assigns a program to a task. **Build the project first** so the program is registered.

| Parameter | Description |
|-----------|-------------|
| `instanceTaskPath` | The PLC task reference — not the `TIRT` task — e.g. `TIPC^Plc^Plc Project^App_TaskRef`. Find it with `scan_plc_project` or `list_tree_items`. |
| `programName` | An existing `PROGRAM`. |

### remove_program

Removes a program from a task reference. Same parameters as `assign_program`.
