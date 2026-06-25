# Installation

TwinCat-MCP ships as two components on your engineering machine: a **Windows
Service** that hosts the MCP endpoint your AI agent connects to, and a
**TcXaeShell plugin** that bridges the TwinCAT Automation Interface.

## Prerequisites

- **Windows 10/11** — the Service and plugin require a Windows session.
- **TwinCAT 3.1 Build 4020.0+** ([Beckhoff XAE Shell](https://www.beckhoff.com/en-en/products/automation/twincat/)) — the scripting API used for project manipulation.

## Installing

A signed **MSI installer** that deploys the Windows Service and the TcXaeShell
plugin together is on the way. It installs the Service as an auto-start Windows
service and registers the plugin inside TcXaeShell — no developer toolchain
required.

In the meantime, to get access to TwinCat-MCP for your team, contact
**[info@qubernetic.com](mailto:info@qubernetic.com)**.

!!! note "Licensing"
    TwinCat-MCP is proprietary software. A valid license is required to use the
    tools — see [Licensing](../licensing/requesting-and-installing.md) for how to
    request and install one.

## Verifying the install

Once the Service is running, it exposes the MCP endpoint on the local machine:

```
http://localhost:3001/mcp
```

A quick way to confirm the Service is up is to connect your agent (see
[Agent Connection](agent-connection.md)) and list the available tools. If the
agent sees the TwinCat-MCP tools, the Service and plugin are working.
