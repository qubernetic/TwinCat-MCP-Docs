# Agent Connection

TwinCat-MCP speaks the Model Context Protocol over **Streamable HTTP**. Point any
MCP-capable agent at the Service endpoint:

```
http://localhost:3001/mcp
```

Make sure the [Service is installed and running](installation.md) first.

## Claude Code

Install Claude Code if you haven't already:

```bash
npm install -g @anthropic-ai/claude-code
```

Add the MCP server:

```bash
claude mcp add --transport http twincat-mcp-service http://localhost:3001/mcp
```

Then start Claude Code in your TwinCAT project directory:

```bash
cd C:\MyProjects\PlcProject
claude
```

## GitHub Copilot CLI

Install the Copilot CLI via winget:

```
winget install GitHub.Copilot
```

!!! note
    Requires a GitHub Copilot subscription (Individual, Business, or Enterprise).
    Open a new terminal after installation for `copilot` to be available.

Create or edit `%USERPROFILE%\.copilot\mcp-config.json`:

```json
{
  "mcpServers": {
    "twincat-mcp-service": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

Verify with `/mcp show` inside the Copilot CLI session. Project-level
configuration is also possible at `.copilot/mcp-config.json` in the project root
(same format).

## Cursor

Open Cursor Settings (`Ctrl+Shift+J`) → **MCP** section and add a new server:

- **Name:** `twincat-mcp-service`
- **Type:** `http`
- **URL:** `http://localhost:3001/mcp`

Alternatively, add it to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "twincat-mcp-service": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

## Next

Once connected, your agent lists every available tool with its description. See
the [Tools Overview](../tools/overview.md) for what's on offer, and
[Licensing](../licensing/requesting-and-installing.md) to activate them.
