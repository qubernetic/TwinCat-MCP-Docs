# ADS (live variables)

These tools talk to a running PLC over ADS. They don't need TcXaeShell — only a
running PLC and a reachable ADS route. Common parameters:

| Parameter | Description |
|-----------|-------------|
| `netId` | AMS NetId (default: current target). For the UMR use [`get_umr_netid`](system-runtime.md#get_umr_netid). |
| `port` | ADS port (default `851` = first PLC runtime). |

### browse_symbols

Lists the PLC's variables.

| Parameter | Description |
|-----------|-------------|
| `parentPath` | Browse the children of this symbol (omit for the root). |
| `maxDepth` | Max nesting depth (`0` = unlimited; `1` = top level only). |
| `leafOnly` | Flat list of leaf variables only. |

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
