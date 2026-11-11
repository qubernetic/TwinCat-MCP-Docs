# Troubleshooting

## Common problems

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| The agent doesn't see any TwinCat-MCP tools | Service not running, wrong URL, or the server was registered for another folder only | Make sure the `TwinCatMcp` Windows service is running, check the URL (`http://localhost:3001/mcp`). In Claude Code register with `--scope user` (see [Agent Connection](../getting-started/agent-connection.md)) and check `/mcp`. |
| Every tool returns a `LICENSE_*` error | No valid license | See [Licensing](../licensing/requesting-and-installing.md). |
| `NO_INSTANCE` / "No TcXaeShell instance connected" | No TcXaeShell with the plugin is connected | Let the agent call `launch_instance` with the solution path, or start TcXaeShell yourself. |
| No TwinCat-MCP toolbar in TcXaeShell | Plugin not loaded | Restart TcXaeShell. If that doesn't help, contact support. |
| `TIMEOUT` on a long operation | TcXaeShell is waiting on a dialog or is busy | Check the TcXaeShell window and close any open dialog. |
| `ADS_ERROR` | PLC not running, or wrong target | Check the PLC state; on the UMR use the NetId from `get_umr_netid`. |
| A confirmation dialog pops up on activation | The operation would go to a real target | For UMR work enable `PreferUmr` (see [Safety](safety.md)). |
| The agent edits `.TcPOU` / `.tsproj` files directly | Agents default to file-level work | Tell it to use the tools; add the instruction block from [Best Practices](best-practices.md). |

## Error codes

When a tool fails, the agent receives a structured error with a `code`:

| Code | Meaning |
|------|---------|
| `NOT_FOUND` | Path, item or file does not exist. |
| `INVALID_ARGUMENT` | A parameter is missing or invalid (e.g. a property without `returnType`). |
| `INVALID_OPERATION` | The operation is not possible in the current state. |
| `TIMEOUT` | TcXaeShell did not respond in time. |
| `ADS_ERROR` | ADS communication with the runtime failed. |
| `NO_INSTANCE` | No TcXaeShell instance is connected. |
| `ONLINE_GUARD` | The PLC is logged in (online); changes to code or the tree are blocked. Call `plc_logout` first. |
| `COM_EXCEPTION` | TwinCAT rejected the operation; the message has the details. |
| `INTERNAL_ERROR` | Unexpected error; please report it. |
| `LICENSE_*` | See [What Licensing Gates](../licensing/what-licensing-gates.md#license-error-codes). |

## Known limitations

TwinCat-MCP 0.2.0 is a beta release. We know about the following and are working on them:

- **Remote Desktop.** When you are logged in to the machine over RDP,
  `launch_instance` cannot start TcXaeShell (`WTSQueryUserToken failed`). Start
  TcXaeShell manually instead — the plugin connects by itself and every other tool works.
- **Long-running memory use.** In some situations (several TcXaeShell instances,
  repeated plugin reconnects, a crashed UMR) the Service's memory use can grow over
  time. If the machine slows down or `TwinCatMcp.Service` uses unusually much memory
  in Task Manager, restart the `TwinCatMcp` service and tell us when it happened.
- **TwinCAT trial-license dialog.** With a TwinCAT trial license, the license dialog
  shown on activation or UMR start can block the operation. Handle the dialog manually.
- **Missing parameters.** A tool call with a missing required parameter sometimes
  surfaces as a generic error instead of `INVALID_ARGUMENT`. Agents usually retry
  correctly by themselves.

Still stuck? Contact [info@qubernetic.com](mailto:info@qubernetic.com) — include the
time, what you asked the agent, and the error message.
