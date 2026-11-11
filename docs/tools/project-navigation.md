# Project Navigation

## Overview and search

### project_digest

One-call compact overview of a PLC project: POUs with their member names, DUTs, GVLs,
referenced libraries and tasks — names, types and counts only, no source code. The
best starting point for getting oriented; follow up with `read_pou` or `search`.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | e.g. `TIPC^Plc`. Auto-discovers the first PLC project if omitted. |

### scan_plc_project

Maps the whole PLC project structure in one call: all folders, POUs, DUTs, GVLs and
interfaces with their paths and types. Use it before navigating the tree — folder
names vary per project.

| Parameter | Description |
|-----------|-------------|
| `plcProjectPath` | e.g. `TIPC^Plc`. Auto-discovers the first PLC project if omitted. |

### search

Searches the PLC project by name or content and returns compact hits (path, kind,
optional line and snippet) — never full source. Prefer it over browsing the tree or
reading files when looking for something.

| Parameter | Description |
|-----------|-------------|
| `query` | Search text; case-insensitive substring by default. |
| `kind` | `pou`, `dut`, `gvl`, `method`, `hardware`, `code`, `symbol` or `any` (default). |
| `fuzzy` | Subsequence match, e.g. `fbmot` matches `FB_Motor`. |
| `regex` | Treat `query` as a regular expression (case-insensitive). |
| `plcProjectPath` | Auto-discovered if omitted. |
| `limit` | Max hits (default 50). |
| `netId`, `port` | Only for `kind=symbol` (searches live symbols over ADS). |

## Tree

### list_tree_items

Lists the children of a configuration tree node, optionally the whole subtree.

| Parameter | Description |
|-----------|-------------|
| `path` | e.g. `TIPC` or `TIPC^Plc^Plc Project^POUs`. |
| `recursive` | Include all descendants. |
| `maxDepth` | Recursion depth (default 10, `-1` unlimited). |
| `limit` | Max total nodes; excess is truncated with a marker. |
| `compact` | Omit `childCount` from each node. |

Each node includes its `itemType` (see [POU type codes](pou.md#type-codes)).

### read_item_xml

Reads any tree item's configuration as XML — I/O devices (`TIID`), tasks (`TIRT`), NC
axes (`TINC`), PLC nodes (`TIPC`).

| Parameter | Description |
|-----------|-------------|
| `path` | e.g. `TIID^Device 1 (EtherCAT)^Term 1 (EK1100)` or `TIRT^PlcTask`. |
| `xpath` | Return only matching elements, e.g. `//CycleTime`. |
| `maxLength` | Max characters. |

### write_item_xml

Writes partial XML configuration to a tree item. Only the elements present in the XML
are applied; everything else is preserved. Read with `read_item_xml` first.

| Parameter | Description |
|-----------|-------------|
| `path` | Tree item path. |
| `xml` | Partial XML. |
| `dryRun` | Preview current vs proposed XML without writing. |

## Structure

### create_folder

Creates a folder in the project tree.

| Parameter | Description |
|-----------|-------------|
| `parentPath` | e.g. `TIPC^Plc^Plc Project^POUs`. |
| `name` | Folder name. |

### rename_item

Renames a tree item.

| Parameter | Description |
|-----------|-------------|
| `path` | Item to rename. |
| `newName` | New name. |
| `dryRun` | Preview only. |

### delete_item

Deletes a child item from the tree.

| Parameter | Description |
|-----------|-------------|
| `parentPath` | Parent containing the item. |
| `childName` | Name of the item to delete. |
| `dryRun` | Preview what would be removed. |
