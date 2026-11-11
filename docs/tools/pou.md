# POUs & Code

Programs, functions, function blocks, methods, properties, interfaces, DUTs and GVLs
are all created, read and written with four tools. Always edit code through these
tools — never by editing `.TcPOU` and similar files (see
[Best Practices](../guides/best-practices.md)).

### create_pou

Creates a new item in the PLC project tree.

| Parameter | Description |
|-----------|-------------|
| `parentPath` | A folder for top-level items (`…^POUs`); the owning POU for members (`…^POUs^I_Motor`); the property for accessors (`…^POUs^FB_Motor^Speed`). |
| `name` | Name of the new item. Ignored for accessors, which are always named `Get` / `Set`. |
| `subType` | Type code, see [below](#type-codes). |
| `language` | `ST` (default), `IL`, `FBD`, `LD`, `SFC`, `CFC`. |
| `returnType` | For functions, methods and properties, e.g. `BOOL`, `LREAL`, `ST_Data`. **Required for properties.** |
| `accessModifier` | `PUBLIC`, `PRIVATE`, `PROTECTED` or `INTERNAL` (methods, properties, accessors). |
| `extends` | Base type (FB, program, interface). |
| `implementsInterfaces` | Comma-separated interfaces, e.g. `I_Motor, I_Diag` (FB, program). |
| `declarationText` | Initial declaration (DUTs, GVLs). |

### read_pou

Reads the declaration and implementation of a POU. With `recursive=true` it includes
all methods, properties and accessors in one call.

| Parameter | Description |
|-----------|-------------|
| `path` | e.g. `TIPC^Plc^Plc Project^POUs^FB_Motor`. |
| `recursive` | Include all children. |
| `fields` | `full` (default), `declaration`, `implementation` or `structure` (names/paths only). |

### read_pou_batch

Reads several POUs in one call; results are keyed by path, and a failure on one path
does not abort the others. Same `recursive` and `fields` options as `read_pou`.

| Parameter | Description |
|-----------|-------------|
| `paths` | List of POU paths. |

### write_pou

Writes the declaration and/or implementation of a POU in one call.

| Parameter | Description |
|-----------|-------------|
| `path` | POU path. |
| `declaration` | Full declaration text (header + VAR blocks). Omit to keep. |
| `implementation` | Full implementation (ST body). Omit to keep. |
| `dryRun` | Return current vs proposed content without writing. |

## Type codes

| Code | Type | Code | Type |
|-----:|------|-----:|------|
| 602 | Program | 615 | GVL |
| 603 | Function | 616 | Transition |
| 604 | Function Block | 618 | Interface |
| 605 | DUT Enum | 610 | Interface Method |
| 606 | DUT Struct | 612 | Interface Property |
| 607 | DUT Union | 654 | Interface Property Get |
| 623 | DUT Alias | 655 | Interface Property Set |
| 608 | Action | 613 | Property Get |
| 609 | Method | 614 | Property Set |
| 611 | Property | | |

## Object-oriented code

TwinCAT has separate type codes for interface members. `create_pou` maps the common
codes automatically based on the parent, so the agent can use the familiar ones:

| Parent | Requested | Created as |
|--------|-----------|------------|
| Interface | Method `609` | Interface Method `610` |
| Interface | Property `611` | Interface Property `612` |
| Interface Property | Get `613` / Set `614` | Interface Property Get `654` / Set `655` |
| Function Block | Property `611`, Get `613`, Set `614` | unchanged |

Rules worth knowing:

- **Properties are created without accessors.** Add a Get (`613`) and/or Set (`614`)
  with the property as `parentPath`. This applies to interface properties too: an
  interface property with no accessor builds, but the syntax check warns
  *"The property defines neither a get nor a set accessor"*.
- **A property needs a type.** `returnType` is required for `611`/`612`; without it the
  call fails with `INVALID_ARGUMENT`.
- **`implementsInterfaces` only writes `IMPLEMENTS`** into the declaration. The
  interface's methods and properties are not generated — create each of them in the
  FB.
- **Accessor names are fixed** to `Get` and `Set`; the `name` parameter is ignored.

A complete interface + implementation, as the agent would do it:

```text
create_pou  parentPath=…^POUs           name=I_Motor   subType=618
create_pou  parentPath=…^POUs^I_Motor   name=Speed     subType=611  returnType=LREAL
create_pou  parentPath=…^I_Motor^Speed  name=Get       subType=613
create_pou  parentPath=…^POUs^I_Motor   name=Start     subType=609  returnType=BOOL

create_pou  parentPath=…^POUs           name=FB_Motor  subType=604  implementsInterfaces=I_Motor
create_pou  parentPath=…^POUs^FB_Motor  name=Speed     subType=611  returnType=LREAL
create_pou  parentPath=…^FB_Motor^Speed name=Get       subType=613
create_pou  parentPath=…^POUs^FB_Motor  name=Start     subType=609  returnType=BOOL  accessModifier=PUBLIC
write_pou   …  (implementations)
check_objects
```
