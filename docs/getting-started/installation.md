# Installation

TwinCat-MCP is installed with one MSI package that contains two features:

- **MCP Service**: the `TwinCatMcp` Windows Service. It hosts the MCP endpoint
  your AI agent connects to, at `http://localhost:3001/mcp`. It starts
  automatically with Windows and needs no separate .NET runtime.
- **TcXaeShell Plugin**: an extension installed into the TwinCAT XAE Shell
  (TcXaeShell). The Service uses it to work with your TwinCAT projects.

## Prerequisites

- 64-bit Windows 10 or 11, and administrator rights for the installation.
- TwinCAT 3.1 Build 4020 or later with TcXaeShell, for the Plugin. A
  Service-only installation does not need TcXaeShell.

## Download

[Download TwinCat-MCP](https://get.twincatmcp.qubernetic.com/download/){ .md-button .md-button--primary .tcmcp-download }
<span class="tcmcp-download-info"></span>

The button always gets the latest MSI. Older versions and the
`TwinCatMcp-<version>.msi.sha256` checksum files are on the
[TwinCat-MCP releases](https://github.com/qubernetic/TwinCat-MCP-Dist/releases) page.

!!! warning "Beta builds are not code-signed"
    The 0.2.0 beta MSI is not Authenticode-signed yet. Windows SmartScreen may
    show "Windows protected your PC"; choose **More info**, then **Run anyway**.
    Before you do, check that the download is intact. In PowerShell:

    ```powershell
    (Get-FileHash .\TwinCatMcp-0.2.0-beta.1.msi -Algorithm SHA256).Hash
    Get-Content .\TwinCatMcp-0.2.0-beta.1.msi.sha256
    ```

    The two hashes must be the same. If they differ, do not run the file.

## Install

Run the MSI. The setup wizard shows the
[license agreement](../legal/standard-license-agreement.md), then lets you
choose the features (both are selected by default).

The Plugin cannot be installed while TcXaeShell is open. If it runs, setup
shows a **TcXaeShell is running** dialog:

- **Close TcXaeShell** closes it for you. TcXaeShell asks you to save unsaved
  changes, and setup waits up to 60 seconds.
- Or close TcXaeShell yourself and click **Retry**.

If TcXaeShell runs with administrator rights, setup cannot close it; close it
yourself and click **Retry**.

When the installation finishes, the Service is running. Open TcXaeShell to load
the Plugin, then [install a license](../licensing/requesting-and-installing.md):
until then only the licensing tools work.

## Unattended install

```
msiexec /i TwinCatMcp-<version>.msi /qn
```

| Property | Effect |
|---|---|
| `ADDLOCAL=ServiceFeature` | Install only the Service (no TcXaeShell needed). |
| `CLOSETCXAESHELL=1` | Close a running TcXaeShell during an unattended install. Without it, the install stops while TcXaeShell runs. |

For example, Service only, with a log file:

```
msiexec /i TwinCatMcp-<version>.msi /qn ADDLOCAL=ServiceFeature /l*v install.log
```

A silent install skips the license page. Installing the software still means
that you accept the
[TwinCat-MCP Standard License Agreement](../legal/standard-license-agreement.md).

## Where things are

| What | Where |
|---|---|
| Service program files, `THIRD-PARTY-NOTICES.txt` | `C:\Program Files\TwinCat-MCP` |
| Plugin | `Extensions\TwinCatMcp` in the TcXaeShell installation folder |
| Settings | `%ProgramData%\TwinCat-MCP\settings.json` (see [Configuration](configuration.md)) |
| License files | `%ProgramData%\TwinCat-MCP\license` (see [Licensing](../licensing/requesting-and-installing.md)) |

## Port 3001 in use

If another program already listens on port 3001, setup still installs and starts
the Service and tells you which program holds the port. The Service starts
listening on the configured port as soon as it is free. To use another port, set
`ServiceHttpPort` in the Options window (TcXaeShell: **Tools > Options >
TwinCat-MCP**, or the gear button on the TwinCat-MCP toolbar), restart the
Service, and update your agent's endpoint URL.

## Upgrade

Run the MSI of the newer version. It replaces the installed version in place
and keeps your settings and license. An older MSI cannot replace a newer
installed version: setup stops with "A newer version of TwinCat-MCP is already
installed."

## Uninstall

Uninstall **TwinCat-MCP** from **Settings > Apps**, or run:

```
msiexec /x TwinCatMcp-<version>.msi
```

As with the installation, close TcXaeShell first or let setup close it.

By default the data folder `%ProgramData%\TwinCat-MCP` stays on the machine, so
your settings and license are still there if you install again. To remove it as
well, uninstall from the command line with `PURGEDATA=1`:

```
msiexec /x TwinCatMcp-<version>.msi PURGEDATA=1
```

## Verifying the install

The Service exposes the MCP endpoint on the local machine:

```
http://localhost:3001/mcp
```

Connect your agent (see [Agent Connection](agent-connection.md)) and list the
available tools. If the agent sees the TwinCat-MCP tools, the Service is
working. With TcXaeShell open, `list_instances` shows it.
