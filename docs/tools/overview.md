# Tools Overview

TwinCat-MCP gives your agent **56 tools** and **3 resources**. The agent picks and
parameterises the tools itself — these pages show what is possible, so you know what
to ask for, and document the rules the tools follow.

| Category | Tools | |
|----------|------:|---|
| [Instances & Solutions](instances-and-solutions.md) | 8 | Start/quit TcXaeShell, create and close solutions and projects, Service memory |
| [Project Navigation](project-navigation.md) | 9 | Overview, search, tree browsing, XML configuration, folders, rename, delete |
| [POUs & Code](pou.md) | 4 | Create, read and write programs, FBs, methods, properties, interfaces, DUTs, GVLs |
| [Build](build.md) | 4 | Syntax check, build, error list, save |
| [Libraries](libraries.md) | 6 | References and the library repository |
| [Tasks](tasks.md) | 5 | Real-time tasks and program assignment |
| [I/O](io.md) | 3 | Hardware topology and variable links |
| [System & Runtime](system-runtime.md) | 10 | Activation, runtime, PLC login/start/stop, target NetId, UMR |
| [ADS (live variables)](ads.md) | 4 | Browse, read, write and assert PLC variables at runtime |
| [Licensing](licensing.md) | 3 | License status, request, install — always available |

## Conventions

### Instances

Most tools run inside TcXaeShell through the TwinCat-MCP plugin and need a connected
instance: call [`launch_instance`](instances-and-solutions.md#launch_instance) first
(or start TcXaeShell yourself). These tools accept an optional `instanceId`; with a
single connected instance it is resolved automatically. The [ADS tools](ads.md),
[`list_instances`](instances-and-solutions.md#list_instances),
`launch_instance` and the [licensing tools](licensing.md) work without an instance.

### Tree paths

Items are addressed by their path in the TwinCAT configuration tree, segments
separated by `^`. Language-independent prefixes:

| Prefix | Target |
|--------|--------|
| `TIPC` | PLC configuration |
| `TIID` | I/O devices |
| `TIRT` | Real-time tasks |
| `TIRC` | Real-time configuration |
| `TINC` | NC configuration |

A PLC project always looks like this; source code lives under `{Name} Project`:

```
TIPC
└── {Name}
    ├── {Name} Project      (POUs, DUTs, GVLs, …)
    └── {Name} Instance     (I/O mappings, task links)
```

Folder names such as `POUs` or `DUTs` vary per project — let the agent discover them
with [`scan_plc_project`](project-navigation.md#scan_plc_project) instead of guessing.

### Token efficiency

Read tools return everything by default. These parameters keep answers small on big
projects:

| Tool | Parameter |
|------|-----------|
| [`read_pou`](pou.md#read_pou) | `fields`: `declaration`, `implementation`, `structure` or `full` |
| [`list_tree_items`](project-navigation.md#list_tree_items) | `limit`, `compact`, `maxDepth` |
| [`browse_symbols`](ads.md#browse_symbols) | `maxDepth`, `maxNodes`, `followPointers`, `leafOnly` |
| [`get_errors`](build.md#get_errors) | `projectFilter`, `limit`, `severity` |
| [`read_item_xml`](project-navigation.md#read_item_xml) | `xpath`, `maxLength` |
| [`search`](project-navigation.md#search) | `limit` |

### Limits are not errors

When a limit is reached, the call still succeeds and the answer ends with a notice:

```json
{"_truncated": true, "_limit": "maxNodes",
 "_message": "Limit reached, not an error: the walk stopped after 1000 symbols ..."}
```

`_limit` names the limit, `_truncated` is set when items were left out, and the
message says how to get the rest (narrow the path or raise the named limit). The data
before the notice is valid. `read_item_xml` marks a cut at the end of the text with
`[limit reached, not an error: ...]`.

### Dry runs

Tools that change code or configuration —
[`write_pou`](pou.md#write_pou), [`write_item_xml`](project-navigation.md#write_item_xml),
[`link_variables`](io.md#link_variables), [`unlink_variables`](io.md#unlink_variables),
[`delete_item`](project-navigation.md#delete_item), [`rename_item`](project-navigation.md#rename_item)
— accept `dryRun=true` to preview the change without applying it.

### Online guard

While the PLC is logged in, changes to code and the project tree are blocked with
`ONLINE_GUARD`. Call [`plc_logout`](system-runtime.md#plc_logout) first.

### Errors

A failed call returns a structured error the agent can branch on:

```json
{ "error": { "code": "NOT_FOUND", "message": "...", "context": { ... } } }
```

See [Troubleshooting → Error codes](../guides/troubleshooting.md#error-codes).

## Resources

Besides tools, the agent can read three resources without a tool call:

| Resource | Content |
|----------|---------|
| `plc_project_tree` | Compact flat list of the PLC project's tree items (name, path, type) |
| `plc_pous` | POUs (programs, functions, FBs, interfaces): name, type, path — no source |
| `plc_libraries` | Referenced libraries (name, version) |
