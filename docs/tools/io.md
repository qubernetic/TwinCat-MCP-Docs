# I/O

### scan_io_devices

Scans the I/O tree and returns the hardware topology — EtherCAT master → couplers →
terminals — with device types, fieldbus addresses and descriptions. Use
`read_item_xml` on a device for channel-level detail.

| Parameter | Description |
|-----------|-------------|
| `devicePath` | e.g. `TIID^Device 1 (EtherCAT)`. Omit to scan all I/O. |

### link_variables

Links a PLC instance variable to an I/O channel. Find I/O paths with
`scan_io_devices` and PLC variable paths with `list_tree_items` on the
`{Name} Instance` node.

| Parameter | Description |
|-----------|-------------|
| `sourcePath` | PLC variable, e.g. `TIPC^Plc^Plc Instance^PlcTask Inputs^GVL_IO.bSensor`. |
| `targetPath` | I/O channel, e.g. `TIID^Device 1 (EtherCAT)^Term 3 (EL1809)^Channel 1^Input`. |
| `dryRun` | Preview the mapping without creating it. |

### unlink_variables

Removes a link created by `link_variables`. Same parameters; `dryRun` previews what
would be removed.
