# Configuration

Shared settings live at `%ProgramData%\TwinCat-MCP\settings.json` and can be
edited from the TwinCat-MCP toolbar **Options** button (gear icon) — a dockable,
tabbed window with **General**, **Safety & Target**, **Connection**, and
**UserMode Runtime** pages (plus **Licensing**).

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ServiceHttpPort` | `3001` | HTTP port for the MCP endpoint. **Requires a Service restart** to take effect. |
| `ServicePipeName` | `twincat-mcp-service` | Named pipe used by the plugin to register with the Service. |
| `HeartbeatIntervalSeconds` | `30` | Plugin → Service keep-alive interval. |
| `RequireConfirmation` | `true` | Prompt before dangerous operations on real hardware. |
| `PreferUmr` | `false` | Automatically use the UserMode Runtime for dangerous tools, even without an explicit `useUmr` flag. |
| `CustomInstructions` | `""` | Custom prompt text sent to AI agents on connect. |

!!! note "Changing the port"
    If you change `ServiceHttpPort`, restart the Service and update your agent's
    endpoint URL (see [Agent Connection](agent-connection.md)) to match the new
    port.
