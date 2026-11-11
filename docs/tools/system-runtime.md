# System & Runtime

Tools marked :material-shield-alert: touch a running system and follow the
[safety rules](../guides/safety.md): they accept `useUmr=true` to run on the
UserMode Runtime (started automatically if needed).

## Target and state

### get_system_state

Returns the TwinCAT system state (running status) and the target AMS NetId.

### get_target_netid

Returns the current target AMS NetId.

### set_target_netid

Sets the target AMS NetId.

| Parameter | Description |
|-----------|-------------|
| `netId` | e.g. `127.0.0.1.1.1`. |

### get_umr_netid

Returns the AMS NetId of the running UserMode Runtime — use it as `netId` for the
[ADS tools](ads.md).

## Configuration and runtime

### activate_configuration

:material-shield-alert: Activates the TwinCAT configuration.

| Parameter | Description |
|-----------|-------------|
| `useUmr` | Run on the UserMode Runtime. |

### start_restart_twincat

:material-shield-alert: Starts or restarts the TwinCAT runtime.

| Parameter | Description |
|-----------|-------------|
| `useUmr` | Run on the UserMode Runtime. |

## PLC

`plcProjectPath` is the PLC project, e.g. `TIPC^Plc`.

### plc_login

:material-shield-alert: Logs in to the PLC runtime. While logged in, code and tree changes are blocked (`ONLINE_GUARD`).

### plc_start

:material-shield-alert: Starts the PLC program.

### plc_stop

:material-shield-alert: Stops the PLC program.

### plc_logout

:material-shield-alert: Logs out from the PLC runtime.

All four take `plcProjectPath` and `useUmr`.
