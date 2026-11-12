# TwinCat-MCP

> **MCP server for TwinCAT 3 PLC development.** Let AI coding agents — Claude Code, GitHub Copilot CLI, Cursor — build, configure, deploy, and debug TwinCAT PLC projects through a standard tool interface.

<div class="tcmcp-download" markdown>

[Download TwinCat-MCP](https://get.twincatmcp.qubernetic.com/download/){ .md-button .md-button--primary .tcmcp-download-button }
[Get started](getting-started/installation.md){ .md-button }
[Connect your agent](getting-started/agent-connection.md){ .md-button }

<div class="tcmcp-download-meta">Windows installer (MSI) &middot; <a href="https://github.com/qubernetic/TwinCat-MCP-Dist/releases">All versions</a></div>

</div>

## What it does

TwinCat-MCP runs as a Windows Service exposing a Streamable HTTP MCP endpoint. A TcXaeShell plugin bridges the TwinCAT Automation Interface, so an agent can create POUs, manage libraries, build, activate configurations, and read/write PLC variables over ADS — all programmatically.

## Highlights

- **56 MCP tools** across project, build, system, and runtime operations.
- **Works with your agent** — Claude Code, GitHub Copilot CLI, Cursor.
- **Live PLC interaction** — read/write symbols and browse the running PLC via ADS.
- **Safe by default** — UserMode Runtime and guarded operations for risky actions.

## Next steps

- [Installation](getting-started/installation.md)
- [Agent Connection](getting-started/agent-connection.md)
- [Licensing](licensing/requesting-and-installing.md)
- [How to Use](guides/how-to-use.md) and [Best Practices](guides/best-practices.md)
- [Tool reference](tools/overview.md)
