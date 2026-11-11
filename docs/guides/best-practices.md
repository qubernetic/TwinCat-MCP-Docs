# Best Practices

## Tell the agent to use TwinCat-MCP, not the project files

This is the single most important rule. AI agents are file-oriented by default: when
they start in a TwinCAT project folder they tend to read the `.TcPOU`, `.TcDUT`,
`.TcGVL`, `.tsproj` and `.plcproj` files directly, grep through them, or even edit
them as text. It looks like it works, but it is the wrong path:

- **Safety.** TcXaeShell keeps the open project in memory. It does not notice an XML
  file changed underneath it, may overwrite the change on the next save, or end up
  in an inconsistent state (missing GUIDs, broken references, lost I/O links). The
  TwinCat-MCP tools change the project the same way the TcXaeShell UI does, so it
  always stays consistent.
- **Token efficiency.** TwinCAT project files are verbose XML; a single function
  block file is many times larger than the Structured Text inside it. The tools
  return only what matters (declaration, code, structure, compact search hits), so
  the agent can work with a much larger project in the same context — faster and
  cheaper.
- **Accuracy.** The tools return TwinCAT's own model: real paths, types, compile
  errors, runtime values. From files, the agent would have to guess.

The Service tells the agent to prefer its tools when it connects, but in practice
agents still drift back to file-level work. **State it explicitly**, on two levels:

1. **As a standing instruction** in the project's instruction file — Claude Code:
   `CLAUDE.md` in the project folder; GitHub Copilot: `.github/copilot-instructions.md`;
   Cursor: `.cursor/rules` — or centrally in the TwinCat-MCP
   [`CustomInstructions`](../getting-started/configuration.md) setting.
2. **In the request**, whenever you see the agent start reading or writing files:
   *"Don't work on the files, use the TwinCat-MCP tools."*

A copy-paste instruction block (extend it with your own rules):

```markdown
## TwinCAT working rules

- Work on the TwinCAT project ONLY through the twincat-mcp-service MCP tools.
  Do not read, search or edit .TcPOU, .TcDUT, .TcGVL, .TcTTO, .tsproj,
  .plcproj or .xti files directly.
- Start: launch_instance with the solution path, then project_digest or
  scan_plc_project. Use the search tool to find things, not the file system.
- Reading code: read_pou (fields=declaration or structure when you don't
  need the full code). Writing: write_pou, with dryRun=true first.
- Checking: check_objects, then build and get_errors.
- Activation, runtime and PLC operations ONLY with useUmr=true.
  Never activate or start/stop a PLC on a real target.
- Before a larger change, describe the plan and wait for approval.
- If a tool returns an error, fix it based on the error code; do not fall
  back to editing files.
```

## More tips

- **Small steps.** One request, one well-defined task. For bigger work ask for a plan
  first and only let the agent write after you approve it.
- **Use dry runs.** [`write_pou`](../tools/pou.md#write_pou),
  [`write_item_xml`](../tools/project-navigation.md#write_item_xml),
  [`link_variables`](../tools/io.md#link_variables),
  [`unlink_variables`](../tools/io.md#unlink_variables),
  [`delete_item`](../tools/project-navigation.md#delete_item) and
  [`rename_item`](../tools/project-navigation.md#rename_item) support `dryRun` to preview the change.
- **Fast feedback loop.** While editing, [`check_objects`](../tools/build.md#check_objects)
  is faster than a full build; ask for `build` before activation.
- **Test on the UMR, verify over ADS.** Ask the agent to start the PLC on the
  [UserMode Runtime](safety.md) after a change and prove the expected behaviour with
  [`assert_symbol`](../tools/ads.md#assert_symbol). "It compiles" becomes "it works".
- **Review the result.** Read the generated code in TcXaeShell before it goes near a
  real machine. A clean build does not mean the logic is right.
- **Version control.** If the project is in Git, start each agent session with a clean
  working tree so changes are reviewable and reversible. Git operations by the agent
  (commit, diff) are fine — they don't conflict with the file rule above.
- **Narrow reads on big projects.** Ask the agent to read only declarations, only one
  project's errors, or with a depth limit. See
  [Token efficiency](../tools/overview.md#token-efficiency).
- **One solution, one TcXaeShell.** Don't open the same solution in two instances
  (yourself and the agent). With several instances running, the agent must pass
  `instanceId`.
- **OOP code.** Interfaces, properties and accessors follow a few specific rules —
  see [Object-oriented code](../tools/pou.md#object-oriented-code).
