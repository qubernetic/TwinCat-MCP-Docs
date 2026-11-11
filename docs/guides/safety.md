# Safety: UserMode Runtime vs Real Hardware

Six tools touch a running system:
[`activate_configuration`](../tools/system-runtime.md#activate_configuration),
[`start_restart_twincat`](../tools/system-runtime.md#start_restart_twincat),
[`plc_login`](../tools/system-runtime.md#plc_login),
[`plc_start`](../tools/system-runtime.md#plc_start),
[`plc_stop`](../tools/system-runtime.md#plc_stop) and
[`plc_logout`](../tools/system-runtime.md#plc_logout).
They can run against two kinds of target.

## UserMode Runtime (recommended)

The UserMode Runtime (UMR) is a TwinCAT runtime that runs on your engineering
machine, without physical I/O. When the agent calls these tools with
`useUmr=true`, TwinCat-MCP starts a UMR automatically (no console window) and points
TcXaeShell at it. The agent can activate, start and test freely — no real machine
moves.

Use [`get_umr_netid`](../tools/system-runtime.md#get_umr_netid) to get the UMR's AMS
NetId for the [ADS tools](../tools/ads.md). You can also start the UMR manually from
the TwinCat-MCP toolbar in TcXaeShell.

## Real target (default)

Without UMR, the behaviour depends on your [settings](../getting-started/configuration.md):

- If a UMR is already running, the operation goes there (it is the safe target).
- If **`PreferUmr`** is enabled, the UMR is used automatically, even without `useUmr=true`.
- If **`RequireConfirmation`** is enabled (default), a Windows dialog asks you to approve
  the operation before it reaches the real target.
- If both are disabled, the operation runs without confirmation.

!!! warning "Recommended settings"
    Enable **`PreferUmr`** and keep **`RequireConfirmation`** on. The agent then never
    touches a real controller by default, and if it ever would, you have to approve it.
    On a real machine with a live process, do not let the agent stop the PLC or
    activate a configuration.

## ADS writes

The ADS tools write to whatever target they are given.
[`write_symbol`](../tools/ads.md#write_symbol) on a UMR test is harmless; on a
controller that runs a machine, only write variables deliberately and under
supervision.
