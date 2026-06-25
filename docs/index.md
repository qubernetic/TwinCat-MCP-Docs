# TwinCat-MCP

> **MCP server for TwinCAT 3 PLC development.** Let AI coding agents — Claude Code, GitHub Copilot CLI, Cursor — build, configure, deploy, and debug TwinCAT PLC projects through a standard tool interface.

[Get started](getting-started/installation.md){ .md-button .md-button--primary }
[Connect your agent](getting-started/agent-connection.md){ .md-button }

## What it does

TwinCat-MCP runs as a Windows Service exposing a Streamable HTTP MCP endpoint. A TcXaeShell plugin bridges the TwinCAT Automation Interface, so an agent can create POUs, manage libraries, build, activate configurations, and read/write PLC variables over ADS — all programmatically.

## Highlights

- **50+ MCP tools** across project, build, system, and runtime operations.
- **Works with your agent** — Claude Code, GitHub Copilot CLI, Cursor.
- **Live PLC interaction** — read/write symbols and browse the running PLC via ADS.
- **Safe by default** — UserMode Runtime and guarded operations for risky actions.

## Next steps

- [Installation](getting-started/installation.md)
- [Agent Connection](getting-started/agent-connection.md)
- [Licensing](licensing/requesting-and-installing.md)
