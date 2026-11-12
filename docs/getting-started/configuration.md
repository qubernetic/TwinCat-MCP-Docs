# Configuration

Shared settings live at `%ProgramData%\TwinCat-MCP\settings.json` and can be
edited from the TwinCat-MCP toolbar **Options** button (gear icon) — a dockable,
tabbed window with **General**, **Safety & Target**, **Connection**,
**UserMode Runtime** and **Memory & Limits** pages (plus **Licensing**).

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `ServiceHttpPort` | `3001` | HTTP port for the MCP endpoint. **Requires a Service restart** to take effect. |
| `ServicePipeName` | `twincat-mcp-service` | Named pipe used by the plugin to register with the Service. |
| `HeartbeatIntervalSeconds` | `30` | Plugin → Service keep-alive interval. |
| `RequireConfirmation` | `true` | Prompt before dangerous operations on real hardware. |
| `PreferUmr` | `false` | Automatically use the UserMode Runtime for dangerous tools, even without an explicit `useUmr` flag. |
| `CustomInstructions` | `""` | Custom prompt text sent to AI agents on connect. |
| `BrowseSymbolsMaxNodes` | `5000` | Hard limit for one `browse_symbols` answer (100–20000). See [Memory & Limits](#memory-limits). |
| `MaxPrivateMemoryMB` | `4096` | Memory guard: above this the Service restarts itself. `0` = off, otherwise at least 512. |

!!! note "Changing the port"
    If you change `ServiceHttpPort`, restart the Service and update your agent's
    endpoint URL (see [Agent Connection](agent-connection.md)) to match the new
    port.

## Memory & Limits

The **Memory & Limits** page shows the Service's memory live, like a usage meter:
the bar is scaled to the memory guard, and a marker shows the estimated peak for your
`browse_symbols` limit. It turns amber above the estimate and red near the guard.
**Release memory now** frees unused memory immediately.

- **Browse limit** (`BrowseSymbolsMaxNodes`): the most symbols one `browse_symbols`
  answer may contain. Agents get 1000 unless they ask for more, and they can browse
  deeper parts with `parentPath`. A higher limit allows larger answers but raises the
  Service's peak memory. The page shows the estimated worst case for the value you
  enter (about 475 MB at 5000, about 1.75 GB at 20000).
- **Memory guard** (`MaxPrivateMemoryMB`): if the Service ever uses more than this, it
  logs a critical event and restarts itself (Windows restarts it within seconds; calls
  running at that moment fail once). This protects the workstation. The page warns
  you if the guard is below the estimated peak.

Both settings apply immediately, without a Service restart.

