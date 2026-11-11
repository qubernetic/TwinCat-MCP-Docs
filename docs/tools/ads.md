# ADS (live variables)

These tools talk to a running PLC over ADS. They don't need TcXaeShell — only a
running PLC and a reachable ADS route. Common parameters:

| Parameter | Description |
|-----------|-------------|
| `netId` | AMS NetId (default: current target). For the UMR use [`get_umr_netid`](system-runtime.md#get_umr_netid). |
| `port` | ADS port (default `851` = first PLC runtime). |

### browse_symbols

Lists the PLC's variables. The walk is always bounded, so even a large object graph
(for example a TcOpen context) answers quickly.

| Parameter | Description |
|-----------|-------------|
| `parentPath` | Browse the children of this symbol (omit for the root). |
| `maxDepth` | Max nesting depth, default `2` (`1` = only the symbols at `parentPath`; `0` = the hard limit of 30). |
| `maxNodes` | Max symbols in the answer, default `1000` (`0` = the hard limit). The hard limit is the [`BrowseSymbolsMaxNodes`](../getting-started/configuration.md#memory-limits) setting, default 5000. |
| `followPointers` | Follow `POINTER TO` / `REFERENCE TO` symbols (default `false`). |
| `leafOnly` | Flat list of leaf variables only (respects `maxDepth`). |

Symbols marked `hasMore: true` have children that were not expanded. Browse them with
`parentPath` rather than raising the limits. When a limit is reached, the answer ends
with a [limit notice](overview.md#limits-are-not-errors). A value above a hard limit
returns `INVALID_ARGUMENT` with the allowed range.

### read_symbol

Reads a variable's current value.

| Parameter | Description |
|-----------|-------------|
| `symbolPath` | e.g. `MAIN.bMotorRunning`, `GVL.nCounter`. |

### write_symbol

Writes a variable at runtime. The value is converted to the target type.

| Parameter | Description |
|-----------|-------------|
| `symbolPath` | e.g. `MAIN.nSetpoint`. |
| `value` | Value as string. |

!!! warning
    On a controller that runs a machine, write only deliberately and under
    supervision. See [Safety](../guides/safety.md#ads-writes).

### assert_symbol

Checks that a variable equals an expected value — the building block for automated
tests on the UserMode Runtime.

| Parameter | Description |
|-----------|-------------|
| `symbolPath` | Variable to check. |
| `expectedValue` | Expected value as string. |
