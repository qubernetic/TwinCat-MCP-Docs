# How to Use

TwinCat-MCP is not something you operate directly. You **talk to your AI agent**
in plain language, and the agent decides which TwinCat-MCP tools to call. Your job
is to state the goal and review the result; the agent does the clicking in
TcXaeShell for you.

## What it is good at

- Mapping and explaining an existing PLC project: which FBs, DUTs and GVLs exist and what they do.
- Creating function blocks, methods, properties, interfaces and data types from a description.
- Refactoring code, then building and fixing compile errors in a loop.
- Mapping the I/O topology and linking PLC variables to I/O channels.
- Creating and configuring tasks, assigning programs.
- Testing on the UserMode Runtime: activate, start the PLC, read, write and assert variables.

## A typical session

You don't need to tell the agent these steps, but it helps to know what happens
under the hood:

1. **Start an instance** — [`launch_instance`](../tools/instances-and-solutions.md#launch_instance)
   starts TcXaeShell (or reuses a running one), opens the solution and waits for the
   plugin to connect. Every TcXaeShell-based tool needs this first.
2. **Get oriented** — [`project_digest`](../tools/project-navigation.md#project_digest) or
   [`scan_plc_project`](../tools/project-navigation.md#scan_plc_project) maps the PLC project
   in one call; [`search`](../tools/project-navigation.md#search) finds things by name or content.
3. **Read and edit** — [`read_pou`](../tools/pou.md#read_pou) and [`write_pou`](../tools/pou.md#write_pou)
   for declarations and code, [`create_pou`](../tools/pou.md#create_pou) for new items.
4. **Check** — [`check_objects`](../tools/build.md#check_objects) for a fast syntax check,
   [`build`](../tools/build.md#build) + [`get_errors`](../tools/build.md#get_errors) for a full build;
   fix and repeat.
5. **Run and test** — activate and start the PLC on the
   [UserMode Runtime](safety.md), then [`read_symbol`](../tools/ads.md#read_symbol),
   [`write_symbol`](../tools/ads.md#write_symbol), [`assert_symbol`](../tools/ads.md#assert_symbol).
6. **Save** — [`save_solution`](../tools/build.md#save_solution).

## Example prompts

Good first requests to try:

> Open `C:\Projects\Machine1\Machine1.sln` and give me an overview of the PLC
> project: which programs, function blocks and data types exist, and what each is for.

> Explain how the state machine in `FB_Conveyor` works, and check whether there is a
> branch where the motor output can stay on after a fault.

> Create an `FB_Debounce` function block that filters a BOOL input for a given TIME.
> Write it, build it, and fix errors until the build is clean.

> Create an interface `I_Motor` with a `Speed : LREAL` property (Get and Set) and a
> `Start` method, then an `FB_Motor` that implements it. Build and fix errors.

> Start it on the UserMode Runtime, activate the configuration, start the PLC and
> verify that `MAIN.nCounter` is increasing.

> Map the EtherCAT topology and link `GVL_IO.bStartButton` to channel 1 of the
> first digital input terminal. Show me a dry run first.

!!! tip "Before your first real task"
    Read [Best Practices](best-practices.md) — especially the part about telling the
    agent to work through the TwinCat-MCP tools instead of editing project files.
